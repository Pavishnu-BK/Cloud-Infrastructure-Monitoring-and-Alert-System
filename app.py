"""
Cloud Infrastructure Monitoring and Automated Alert System
Flask Web Application & REST Controller
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import monitoring

app = Flask(__name__)
# Secret key for secure session handling and flash messaging
app.secret_key = os.environ.get('SECRET_KEY', 'devops-cloud-monitoring-secret-key-2026')

# Initialize database schema upon application launch
monitoring.init_db()


@app.context_processor
def inject_common_context():
    """Make common formatting helpers and status available across all Jinja2 templates."""
    try:
        health_status = monitoring.get_system_health_status()
    except Exception:
        health_status = 'Unavailable'

    return {
        'format_uptime': monitoring.format_uptime,
        'current_year': datetime.now().year,
        'global_health_status': health_status
    }


@app.route('/')
def home():
    """Root route redirecting to the main monitoring dashboard."""
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    """
    Main Monitoring Dashboard.
    Collects live system metrics, evaluates alerts against configured thresholds,
    and displays system overview, metric cards, recent samples, and alert status.
    """
    error_message = None
    metrics_data = None

    try:
        # Collect live system metrics
        metrics_data = monitoring.get_system_metrics()
        # Persist snapshot and evaluate alert thresholds
        monitoring.evaluate_and_record_metrics(metrics_data)
    except Exception as e:
        error_message = str(e)

    # Fetch recent history for table and quick trend preview
    recent_history = monitoring.get_metrics_history(limit=10)
    # Fetch active alerts for dashboard alert banner
    active_alerts = monitoring.get_alerts(status_filter='Active', limit=10)
    # Fetch current alert thresholds
    settings = monitoring.get_settings()
    # Overall system health
    health_status = monitoring.get_system_health_status()
    alert_stats = monitoring.get_alert_stats()

    # Fetch registered server nodes (tracked in Jenkins & Docker)
    servers_list = monitoring.get_servers()

    return render_template(
        'index.html',
        metrics=metrics_data,
        recent_history=recent_history,
        active_alerts=active_alerts,
        settings=settings,
        health_status=health_status,
        alert_stats=alert_stats,
        servers=servers_list,
        error_message=error_message
    )


@app.route('/metrics', methods=['GET'])
def metrics_endpoint():
    """
    Metrics Collection and API Endpoint.
    Collects real-time metrics, records to SQLite, evaluates thresholds,
    and returns structured JSON for automated collectors and AJAX pollers.
    """
    try:
        metrics_data = monitoring.get_system_metrics()
        snapshot_id, alert_actions = monitoring.evaluate_and_record_metrics(metrics_data)
        health_status = monitoring.get_system_health_status()
        alert_stats = monitoring.get_alert_stats()

        return jsonify({
            'status': 'success',
            'snapshot_id': snapshot_id,
            'metrics': metrics_data,
            'alert_actions': alert_actions,
            'system_health': health_status,
            'alert_stats': alert_stats
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/history', methods=['GET'])
def history():
    """
    Metrics History View.
    Displays tabular metric snapshots and trend charts of CPU, memory, and disk.
    Gracefully handles empty history.
    """
    limit = request.args.get('limit', default=50, type=int)
    history_records = monitoring.get_metrics_history(limit=limit)
    return render_template('history.html', history=history_records, limit=limit)


@app.route('/api/history', methods=['GET'])
def api_history():
    """JSON API returning chronological metric history for client-side charts."""
    limit = request.args.get('limit', default=30, type=int)
    # Fetch latest snapshots then reverse for left-to-right chronological chart order
    records = monitoring.get_metrics_history(limit=limit)
    records.reverse()
    return jsonify(records), 200


@app.route('/alerts', methods=['GET'])
def alerts_page():
    """
    Alerts View.
    Displays active and resolved alerts with severity, metric name,
    measured value, threshold, and timestamps.
    """
    status_filter = request.args.get('status', default=None)
    alerts_list = monitoring.get_alerts(status_filter=status_filter, limit=100)
    stats = monitoring.get_alert_stats()
    return render_template(
        'alerts.html',
        alerts=alerts_list,
        stats=stats,
        current_filter=status_filter
    )


@app.route('/settings', methods=['GET'])
def settings_page():
    """
    System Status & Threshold Settings View.
    Displays monitored host info, last collection timestamp,
    and form to update CPU, Memory, and Disk alert thresholds.
    """
    settings = monitoring.get_settings()
    recent = monitoring.get_metrics_history(limit=1)
    last_collection = recent[0]['collected_at'] if recent else "Never"

    try:
        sys_info = monitoring.get_system_metrics()
    except Exception:
        sys_info = None

    return render_template(
        'settings.html',
        settings=settings,
        last_collection=last_collection,
        sys_info=sys_info
    )


@app.route('/update_settings', methods=['POST'])
def update_settings():
    """
    Handle threshold settings updates with strict numeric validation (1–100%).
    Persists changes into SQLite and informs the user via flash messages.
    """
    cpu = request.form.get('cpu_threshold', '').strip()
    mem = request.form.get('memory_threshold', '').strip()
    disk = request.form.get('disk_threshold', '').strip()

    success, message = monitoring.validate_and_update_settings(cpu, mem, disk)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('settings_page'))


@app.route('/health', methods=['GET'])
def health_check():
    """
    Container Health Check Endpoint.
    Returns HTTP 200 and operational health metadata for Docker and load balancer health checks.
    """
    try:
        # Verify SQLite accessibility
        settings = monitoring.get_settings()
        health_state = monitoring.get_system_health_status()
        return jsonify({
            'status': 'healthy',
            'service': 'cloud-infrastructure-monitoring',
            'database': 'connected',
            'system_health': health_state,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 503


@app.route('/pipeline')
@app.route('/devops')
def devops_pipeline():
    """DevOps operations dashboard displaying Jenkins, Docker, and GitHub telemetry."""
    servers_list = monitoring.get_servers()
    return render_template('devops_pipeline_dashboard.html', servers=servers_list)


@app.route('/api/servers', methods=['GET'])
def api_get_servers():
    """Retrieve JSON list of all monitored servers with Jenkins and Docker metadata."""
    try:
        servers_list = monitoring.get_servers()
        return jsonify({'status': 'success', 'servers': servers_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/servers/add', methods=['POST'])
@app.route('/add_server', methods=['POST'])
def api_add_server():
    """
    Register a new server under monitoring with automated Jenkins & Docker tracking.
    Supports both JSON and form data submission.
    """
    is_api = request.path.startswith('/api/') or request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.is_json:
        payload = request.get_json() or {}
        name = payload.get('name')
        host = payload.get('host')
        port = payload.get('port', 5000)
        environment = payload.get('environment', 'Production')
        docker_container = payload.get('docker_container')
        jenkins_job = payload.get('jenkins_job')
    else:
        name = request.form.get('name')
        host = request.form.get('host')
        port = request.form.get('port', 5000)
        environment = request.form.get('environment', 'Production')
        docker_container = request.form.get('docker_container')
        jenkins_job = request.form.get('jenkins_job')

    try:
        server_id = monitoring.add_server(
            name=name,
            host=host,
            port=port,
            environment=environment,
            docker_container=docker_container,
            jenkins_job=jenkins_job
        )
        new_server = monitoring.get_server_by_id(server_id)

        if is_api:
            return jsonify({
                'status': 'success',
                'message': f"Server '{name}' successfully registered under Jenkins & Docker monitoring!",
                'server': new_server
            }), 201
        else:
            flash(f"Server '{name}' successfully registered and enrolled in Jenkins CI & Docker tracking!", "success")
            return redirect(url_for('dashboard'))

    except ValueError as ve:
        if is_api:
            return jsonify({'status': 'error', 'message': str(ve)}), 400
        else:
            flash(str(ve), "danger")
            return redirect(url_for('dashboard'))
    except Exception as e:
        if is_api:
            return jsonify({'status': 'error', 'message': f"Internal server error: {str(e)}"}), 500
        else:
            flash(f"Error registering server: {str(e)}", "danger")
            return redirect(url_for('dashboard'))


@app.route('/api/servers/<int:server_id>/delete', methods=['POST', 'DELETE'])
@app.route('/delete_server/<int:server_id>', methods=['POST'])
def api_delete_server(server_id):
    """Unregister / remove a server node from active monitoring."""
    is_api = request.path.startswith('/api/') or request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    success = monitoring.delete_server(server_id)

    if is_api:
        if success:
            return jsonify({'status': 'success', 'message': f'Server #{server_id} removed.'}), 200
        return jsonify({'status': 'error', 'message': f'Server #{server_id} not found.'}), 404
    else:
        if success:
            flash(f"Server #{server_id} successfully unregistered.", "info")
        else:
            flash(f"Server #{server_id} not found.", "warning")
        return redirect(url_for('dashboard'))


@app.route('/api/servers/<int:server_id>/ping', methods=['POST'])
def api_ping_server(server_id):
    """Perform live health ping and update latency/CPU telemetry for server node."""
    server = monitoring.get_server_by_id(server_id)
    if not server:
        return jsonify({'status': 'error', 'message': 'Server not found'}), 404

    result = monitoring.ping_server(server_id)
    return jsonify({
        'status': 'success',
        'message': f"Ping to {server['name']} ({server['host']}) successful: {result['latency_ms']}ms",
        'result': result
    }), 200


@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html', page_error="Page not found (404)"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('base.html', page_error="Internal server error (500)"), 500


if __name__ == '__main__':
    # Listen on 0.0.0.0 and port 5000 as required
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    print(f"[*] Starting Cloud Infrastructure Monitoring on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug_mode)
