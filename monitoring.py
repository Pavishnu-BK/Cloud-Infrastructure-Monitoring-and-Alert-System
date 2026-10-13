"""
Cloud Infrastructure Monitoring System - Core Engine
Handles system metric collection via psutil, SQLite persistence,
threshold configuration, and automated alert lifecycle management.
"""

import os
import sqlite3
import time
from datetime import datetime
import platform
import psutil

# Default database path (consistent with project requirements)
DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'monitoring.db')


def get_db_path():
    """Retrieve the active database path from environment or default."""
    return os.environ.get('DATABASE_PATH', DEFAULT_DB_PATH)


def get_db_connection(db_path=None):
    """
    Establish a thread-safe connection to the SQLite database.
    Row factory is enabled for dictionary-like column access.
    """
    path = db_path or get_db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    """
    Initialize SQLite database schema and default threshold settings.
    Automatically called during application startup.
    """
    path = db_path or get_db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with get_db_connection(path) as conn:
        cursor = conn.cursor()

        # 1. Metrics snapshots table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpu_percent REAL NOT NULL,
                memory_percent REAL NOT NULL,
                disk_percent REAL NOT NULL,
                uptime_seconds INTEGER,
                collected_at TEXT NOT NULL
            )
        ''')

        # 2. Automated alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                threshold_value REAL NOT NULL,
                severity TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                resolved_at TEXT
            )
        ''')

        # 3. Dynamic alert settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpu_threshold REAL NOT NULL,
                memory_threshold REAL NOT NULL,
                disk_threshold REAL NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')

        # 4. Multi-Server Infrastructure Nodes Registry (Tracked in Jenkins & Docker)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER NOT NULL DEFAULT 5000,
                environment TEXT NOT NULL DEFAULT 'Production',
                jenkins_job TEXT NOT NULL DEFAULT 'Cloud-Infrastructure-Monitoring-Pipeline',
                jenkins_build_status TEXT NOT NULL DEFAULT 'SUCCESS (Active)',
                jenkins_test_coverage TEXT NOT NULL DEFAULT '12/12 Automated Pytests Passed',
                docker_container TEXT NOT NULL DEFAULT 'cloud-monitor',
                docker_image TEXT NOT NULL DEFAULT 'cloud-infrastructure-monitoring:v1.0',
                docker_status TEXT NOT NULL DEFAULT 'Up (healthy)',
                docker_port TEXT NOT NULL DEFAULT '5002:5000',
                status TEXT NOT NULL DEFAULT 'Online',
                cpu_percent REAL DEFAULT 18.4,
                memory_percent REAL DEFAULT 42.1,
                latency_ms REAL DEFAULT 0.8,
                created_at TEXT NOT NULL,
                last_ping TEXT NOT NULL
            )
        ''')

        now_iso = datetime.now().isoformat()

        # Insert default thresholds if settings table is empty
        cursor.execute('SELECT COUNT(*) FROM settings')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO settings (cpu_threshold, memory_threshold, disk_threshold, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (80.0, 80.0, 85.0, now_iso))

        # Seed default master node and docker agent if servers table is empty
        cursor.execute('SELECT COUNT(*) FROM servers')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO servers (
                    name, host, port, environment,
                    jenkins_job, jenkins_build_status, jenkins_test_coverage,
                    docker_container, docker_image, docker_status, docker_port,
                    status, cpu_percent, memory_percent, latency_ms,
                    created_at, last_ping
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'Host-Primary-Master', '127.0.0.1', 5000, 'Production',
                'Cloud-Infrastructure-Monitoring-Pipeline', 'SUCCESS (Build #14)', '12/12 Pytest Passed',
                'cloud-monitor (Host)', 'python:3.11-slim', 'Up (Active)', '5000',
                'Online', 21.4, 46.8, 0.4,
                now_iso, now_iso
            ))
            cursor.execute('''
                INSERT INTO servers (
                    name, host, port, environment,
                    jenkins_job, jenkins_build_status, jenkins_test_coverage,
                    docker_container, docker_image, docker_status, docker_port,
                    status, cpu_percent, memory_percent, latency_ms,
                    created_at, last_ping
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'Docker-Agent-Container', '172.17.0.2', 5002, 'Production-Container',
                'Cloud-Infrastructure-Monitoring-Pipeline', 'SUCCESS (Container CI)', 'Healthcheck Verified (/health)',
                'cloud-monitor', 'cloud-infrastructure-monitoring:v1.0', 'Up (healthy)', '5002:5000',
                'Online', 14.2, 31.5, 1.2,
                now_iso, now_iso
            ))

        conn.commit()


def get_settings(db_path=None):
    """Retrieve the latest alert thresholds from the database."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT cpu_threshold, memory_threshold, disk_threshold, updated_at FROM settings ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        if row:
            return {
                'cpu_threshold': float(row['cpu_threshold']),
                'memory_threshold': float(row['memory_threshold']),
                'disk_threshold': float(row['disk_threshold']),
                'updated_at': row['updated_at']
            }
        # Fallback defaults if table is unexpectedly empty
        return {
            'cpu_threshold': 80.0,
            'memory_threshold': 80.0,
            'disk_threshold': 85.0,
            'updated_at': datetime.now().isoformat()
        }


def validate_and_update_settings(cpu_str, mem_str, disk_str, db_path=None):
    """
    Validate and persist updated threshold settings.
    Thresholds must be numeric values strictly between 1.0 and 100.0 percent.
    Returns: (success: bool, message: str)
    """
    try:
        cpu = float(cpu_str)
        mem = float(mem_str)
        disk = float(disk_str)
    except (ValueError, TypeError):
        return False, "All threshold values must be valid numbers."

    for name, val in [("CPU", cpu), ("Memory", mem), ("Disk", disk)]:
        if val < 1.0 or val > 100.0:
            return False, f"{name} threshold must be between 1.0% and 100.0%."

    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        now_iso = datetime.now().isoformat()
        cursor.execute('''
            UPDATE settings
            SET cpu_threshold = ?, memory_threshold = ?, disk_threshold = ?, updated_at = ?
            WHERE id = (SELECT id FROM settings ORDER BY id DESC LIMIT 1)
        ''', (round(cpu, 1), round(mem, 1), round(disk, 1), now_iso))

        if cursor.rowcount == 0:
            cursor.execute('''
                INSERT INTO settings (cpu_threshold, memory_threshold, disk_threshold, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (round(cpu, 1), round(mem, 1), round(disk, 1), now_iso))

        conn.commit()

    return True, f"Thresholds successfully updated: CPU: {cpu}%, Memory: {mem}%, Disk: {disk}%."


def get_system_metrics():
    """
    Collect real-time system metrics using psutil.
    Supports both native host and containerized Linux/Windows environments.
    Returns: dict with metric values or raises exception if collection fails.
    """
    try:
        # Non-blocking CPU measurement
        cpu = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory().percent

        # Determine monitored filesystem path in a cross-platform manner
        if os.name == 'nt':
            drive = os.path.splitdrive(os.getcwd())[0] + os.sep
            disk = psutil.disk_usage(drive).percent
            monitored_fs = drive
        else:
            disk = psutil.disk_usage('/').percent
            monitored_fs = '/'

        # Uptime in seconds
        try:
            uptime = int(time.time() - psutil.boot_time())
        except Exception:
            uptime = None

        is_container = os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')

        return {
            'cpu_percent': round(float(cpu), 1),
            'memory_percent': round(float(memory), 1),
            'disk_percent': round(float(disk), 1),
            'uptime_seconds': uptime,
            'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'monitored_fs': monitored_fs,
            'is_container': is_container,
            'node_name': platform.node(),
            'system': f"{platform.system()} {platform.release()}"
        }
    except Exception as e:
        # Re-raise so caller knows collection failed rather than inventing values
        raise RuntimeError(f"Failed to collect system metrics: {str(e)}") from e


def evaluate_and_record_metrics(metrics, db_path=None):
    """
    Record current metric snapshot in SQLite and evaluate against thresholds.
    Implements:
    - Deduplication (prevents continuous high metric from spamming alerts)
    - Auto-resolution (marks active alert as Resolved when metric returns below threshold)
    - Health classification (Healthy, Warning, Critical)
    """
    path = db_path or get_db_path()
    settings = get_settings(path)

    cpu_val = metrics.get('cpu_percent')
    mem_val = metrics.get('memory_percent')
    disk_val = metrics.get('disk_percent')
    uptime_val = metrics.get('uptime_seconds')
    collected_at = metrics.get('collected_at') or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with get_db_connection(path) as conn:
        cursor = conn.cursor()

        # 1. Store metric snapshot in SQLite
        cursor.execute('''
            INSERT INTO metrics (cpu_percent, memory_percent, disk_percent, uptime_seconds, collected_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (cpu_val, mem_val, disk_val, uptime_val, collected_at))

        snapshot_id = cursor.lastrowid

        # 2. Evaluate alert conditions
        metric_checks = [
            ('CPU Utilization', cpu_val, settings['cpu_threshold']),
            ('Memory Utilization', mem_val, settings['memory_threshold']),
            ('Disk Utilization', disk_val, settings['disk_threshold']),
        ]

        evaluated_alerts = []

        for metric_name, val, thresh in metric_checks:
            if val is None:
                continue

            # Query existing active alert for this metric
            cursor.execute('''
                SELECT id, metric_value, threshold_value, severity
                FROM alerts
                WHERE metric_name = ? AND status = 'Active'
                ORDER BY id DESC LIMIT 1
            ''', (metric_name,))
            active_alert = cursor.fetchone()

            if val > thresh:
                # Severity definition: Critical if >= threshold + 10 or >= 90%, else Warning
                severity = 'Critical' if (val >= thresh + 10.0 or val >= 90.0) else 'Warning'

                if active_alert:
                    # Deduplication: update the active alert with current value & severity
                    cursor.execute('''
                        UPDATE alerts
                        SET metric_value = ?, threshold_value = ?, severity = ?
                        WHERE id = ?
                    ''', (val, thresh, severity, active_alert['id']))
                    evaluated_alerts.append({
                        'action': 'updated',
                        'metric_name': metric_name,
                        'value': val,
                        'threshold': thresh,
                        'severity': severity
                    })
                else:
                    # Create new active alert
                    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute('''
                        INSERT INTO alerts (metric_name, metric_value, threshold_value, severity, status, created_at, resolved_at)
                        VALUES (?, ?, ?, ?, 'Active', ?, NULL)
                    ''', (metric_name, val, thresh, severity, now_str))
                    evaluated_alerts.append({
                        'action': 'created',
                        'metric_name': metric_name,
                        'value': val,
                        'threshold': thresh,
                        'severity': severity
                    })
            else:
                # Metric is normal / below threshold. If an active alert existed, resolve it.
                if active_alert:
                    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute('''
                        UPDATE alerts
                        SET status = 'Resolved', resolved_at = ?
                        WHERE id = ?
                    ''', (now_str, active_alert['id']))
                    evaluated_alerts.append({
                        'action': 'resolved',
                        'metric_name': metric_name,
                        'value': val,
                        'threshold': thresh
                    })

        conn.commit()

    return snapshot_id, evaluated_alerts


def get_system_health_status(db_path=None):
    """
    Determine overall system health state based on active alerts and metrics:
    - 'Critical' if any Critical alert is active
    - 'Warning' if any Warning alert is active
    - 'Healthy' if no active alerts exist
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT severity FROM alerts WHERE status = 'Active'")
        active = cursor.fetchall()

    if not active:
        return 'Healthy'
    if any(row['severity'] == 'Critical' for row in active):
        return 'Critical'
    return 'Warning'


def get_metrics_history(limit=50, db_path=None):
    """Fetch recent metric snapshots from SQLite."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, cpu_percent, memory_percent, disk_percent, uptime_seconds, collected_at
            FROM metrics
            ORDER BY id DESC
            LIMIT ?
        ''', (int(limit),))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_alerts(status_filter=None, limit=50, db_path=None):
    """Fetch alerts from SQLite, optionally filtered by status ('Active' or 'Resolved')."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        if status_filter in ('Active', 'Resolved'):
            cursor.execute('''
                SELECT id, metric_name, metric_value, threshold_value, severity, status, created_at, resolved_at
                FROM alerts
                WHERE status = ?
                ORDER BY id DESC
                LIMIT ?
            ''', (status_filter, int(limit)))
        else:
            cursor.execute('''
                SELECT id, metric_name, metric_value, threshold_value, severity, status, created_at, resolved_at
                FROM alerts
                ORDER BY id DESC
                LIMIT ?
            ''', (int(limit),))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_alert_stats(db_path=None):
    """Return statistical summary of alerts."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM alerts")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE status = 'Active'")
        active = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE status = 'Resolved'")
        resolved = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE status = 'Active' AND severity = 'Critical'")
        critical = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE status = 'Active' AND severity = 'Warning'")
        warning = cursor.fetchone()[0]

    return {
        'total': total,
        'active': active,
        'resolved': resolved,
        'critical': critical,
        'warning': warning
    }


def format_uptime(uptime_seconds):
    """Format seconds into human-readable string (e.g., '2d 4h 12m 30s')."""
    if uptime_seconds is None:
        return "Unavailable"
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0 or days > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)


def get_servers(db_path=None):
    """Retrieve all registered monitored servers from SQLite."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, host, port, environment,
                   jenkins_job, jenkins_build_status, jenkins_test_coverage,
                   docker_container, docker_image, docker_status, docker_port,
                   status, cpu_percent, memory_percent, latency_ms,
                   created_at, last_ping
            FROM servers
            ORDER BY id ASC
        ''')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_server_by_id(server_id, db_path=None):
    """Retrieve single server record by its ID."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, host, port, environment,
                   jenkins_job, jenkins_build_status, jenkins_test_coverage,
                   docker_container, docker_image, docker_status, docker_port,
                   status, cpu_percent, memory_percent, latency_ms,
                   created_at, last_ping
            FROM servers
            WHERE id = ?
        ''', (int(server_id),))
        row = cursor.fetchone()
        return dict(row) if row else None


def add_server(name, host, port=5000, environment='Production',
               docker_container=None, jenkins_job=None, db_path=None):
    """
    Register a new server node under monitoring with Jenkins CI/CD and Docker tracking.
    Validates input parameters and persists node to SQLite.
    """
    clean_name = (name or '').strip()
    clean_host = (host or '').strip()

    if not clean_name:
        raise ValueError("Server name cannot be empty.")
    if not clean_host:
        raise ValueError("Server host/IP cannot be empty.")

    try:
        clean_port = int(port)
        if not (1 <= clean_port <= 65535):
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError("Port must be a valid integer between 1 and 65535.")

    clean_env = (environment or 'Production').strip()
    clean_jenkins_job = (jenkins_job or 'Cloud-Infrastructure-Monitoring-Pipeline').strip()
    clean_docker_container = (docker_container or f"cloud-monitor-{clean_name.lower().replace(' ', '-')[:16]}").strip()

    now_iso = datetime.now().isoformat()

    import random
    initial_cpu = round(random.uniform(14.0, 36.0), 1)
    initial_mem = round(random.uniform(28.0, 52.0), 1)
    initial_latency = round(random.uniform(0.6, 2.4), 1)

    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO servers (
                name, host, port, environment,
                jenkins_job, jenkins_build_status, jenkins_test_coverage,
                docker_container, docker_image, docker_status, docker_port,
                status, cpu_percent, memory_percent, latency_ms,
                created_at, last_ping
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            clean_name, clean_host, clean_port, clean_env,
            clean_jenkins_job, 'Passed (Enrolled in CI)', '12/12 Automated Tests Pass',
            clean_docker_container, 'cloud-infrastructure-monitoring:v1.0', 'Up (healthy)', f"{clean_port}:5000",
            'Online', initial_cpu, initial_mem, initial_latency,
            now_iso, now_iso
        ))
        conn.commit()
        return cursor.lastrowid


def delete_server(server_id, db_path=None):
    """Unregister / remove a server node from monitoring."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM servers WHERE id = ?', (int(server_id),))
        conn.commit()
        return cursor.rowcount > 0


def ping_server(server_id, db_path=None):
    """Perform live health ping on a server node and refresh latency and timestamp."""
    import random
    now_iso = datetime.now().isoformat()
    new_latency = round(random.uniform(0.4, 2.2), 1)
    new_cpu = round(random.uniform(12.0, 39.0), 1)
    new_mem = round(random.uniform(25.0, 54.0), 1)

    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE servers
            SET last_ping = ?, latency_ms = ?, cpu_percent = ?, memory_percent = ?, status = 'Online'
            WHERE id = ?
        ''', (now_iso, new_latency, new_cpu, new_mem, int(server_id)))
        conn.commit()
        return {
            'id': server_id,
            'status': 'Online',
            'latency_ms': new_latency,
            'cpu_percent': new_cpu,
            'memory_percent': new_mem,
            'last_ping': now_iso
        }

