"""
Automated Test Suite for Cloud Infrastructure Monitoring System
Uses Pytest with isolated temporary databases and mocked system metrics.
Command: python -m pytest test_app.py
"""

import os
import tempfile
import pytest
from unittest.mock import patch

import monitoring
from app import app


@pytest.fixture
def temp_db():
    """Create an isolated temporary SQLite database for each test run."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    old_env = os.environ.get('DATABASE_PATH')
    os.environ['DATABASE_PATH'] = path

    # Initialize tables and default settings in temp db
    monitoring.init_db(path)

    yield path

    # Cleanup temporary database
    if old_env is not None:
        os.environ['DATABASE_PATH'] = old_env
    else:
        os.environ.pop('DATABASE_PATH', None)

    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass


@pytest.fixture
def client(temp_db):
    """Create a Flask test client configured with the test database."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as test_client:
        yield test_client


def test_flask_app_initialization():
    """Verify that Flask application starts and has correct configuration."""
    assert app is not None
    assert app.name == 'app'


def test_home_and_dashboard_routes(client, temp_db):
    """Verify root redirect and dashboard HTTP 200 response."""
    # Root redirects to /dashboard
    response_root = client.get('/')
    assert response_root.status_code == 302
    assert response_root.headers['Location'] == '/dashboard'

    # Dashboard loads successfully
    with patch('monitoring.get_system_metrics', return_value={
        'cpu_percent': 35.0,
        'memory_percent': 50.0,
        'disk_percent': 40.0,
        'uptime_seconds': 12000,
        'collected_at': '2026-10-13 18:00:00',
        'monitored_fs': '/',
        'is_container': False,
        'node_name': 'test-node',
        'system': 'Linux Test'
    }):
        response_dash = client.get('/dashboard')
        assert response_dash.status_code == 200
        assert b'Infrastructure Monitoring Dashboard' in response_dash.data
        assert b'CPU Utilization' in response_dash.data


def test_health_endpoint(client, temp_db):
    """Verify container health check endpoint returns 200 and healthy JSON."""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'healthy'
    assert json_data['database'] == 'connected'
    assert 'timestamp' in json_data


def test_metrics_collection_endpoint(client, temp_db):
    """Verify /metrics route collects, stores, and returns structured JSON."""
    mock_metrics = {
        'cpu_percent': 42.5,
        'memory_percent': 65.0,
        'disk_percent': 55.0,
        'uptime_seconds': 9999,
        'collected_at': '2026-10-13 18:05:00',
        'monitored_fs': '/',
        'is_container': True,
        'node_name': 'docker-ci-node',
        'system': 'Linux Container'
    }

    with patch('monitoring.get_system_metrics', return_value=mock_metrics):
        response = client.get('/metrics')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['metrics']['cpu_percent'] == 42.5
        assert data['metrics']['memory_percent'] == 65.0
        assert data['snapshot_id'] is not None


def test_metric_snapshot_storage(temp_db):
    """Verify that metric snapshots are accurately persisted and retrieved in SQLite."""
    sample = {
        'cpu_percent': 25.5,
        'memory_percent': 40.2,
        'disk_percent': 60.1,
        'uptime_seconds': 86400,
        'collected_at': '2026-10-13 18:10:00'
    }

    snapshot_id, _ = monitoring.evaluate_and_record_metrics(sample, db_path=temp_db)
    assert snapshot_id is not None

    history = monitoring.get_metrics_history(limit=5, db_path=temp_db)
    assert len(history) == 1
    assert history[0]['cpu_percent'] == 25.5
    assert history[0]['memory_percent'] == 40.2
    assert history[0]['disk_percent'] == 60.1
    assert history[0]['uptime_seconds'] == 86400


def test_alert_lifecycle_trigger_dedup_and_resolve(temp_db):
    """
    Comprehensive test of the automated alert lifecycle:
    1. Metric exceeds threshold -> Alert created (Active)
    2. Continuous high metric -> Deduplication (no duplicate row)
    3. Metric returns below threshold -> Auto-resolution (Resolved)
    """
    # 1. Exceed CPU threshold (default: 80.0%)
    high_metric = {
        'cpu_percent': 92.5,
        'memory_percent': 50.0,
        'disk_percent': 40.0,
        'uptime_seconds': 5000,
        'collected_at': '2026-10-13 18:15:00'
    }
    monitoring.evaluate_and_record_metrics(high_metric, db_path=temp_db)

    active_alerts = monitoring.get_alerts(status_filter='Active', db_path=temp_db)
    assert len(active_alerts) == 1
    alert = active_alerts[0]
    assert alert['metric_name'] == 'CPU Utilization'
    assert alert['metric_value'] == 92.5
    assert alert['status'] == 'Active'
    assert alert['severity'] == 'Critical'
    assert alert['resolved_at'] is None
    original_alert_id = alert['id']

    # 2. Continuous high metric - test Deduplication
    high_metric_2 = {
        'cpu_percent': 94.0,
        'memory_percent': 50.0,
        'disk_percent': 40.0,
        'uptime_seconds': 5005,
        'collected_at': '2026-10-13 18:15:05'
    }
    monitoring.evaluate_and_record_metrics(high_metric_2, db_path=temp_db)

    active_alerts_after = monitoring.get_alerts(status_filter='Active', db_path=temp_db)
    # Must still have only 1 active alert (deduplicated)
    assert len(active_alerts_after) == 1
    assert active_alerts_after[0]['id'] == original_alert_id
    assert active_alerts_after[0]['metric_value'] == 94.0

    # 3. Metric drops below threshold - test Auto-Resolution
    normal_metric = {
        'cpu_percent': 35.0,
        'memory_percent': 50.0,
        'disk_percent': 40.0,
        'uptime_seconds': 5010,
        'collected_at': '2026-10-13 18:15:10'
    }
    monitoring.evaluate_and_record_metrics(normal_metric, db_path=temp_db)

    # Active alerts should now be 0
    active_now = monitoring.get_alerts(status_filter='Active', db_path=temp_db)
    assert len(active_now) == 0

    # Resolved alerts should contain the alert
    resolved_now = monitoring.get_alerts(status_filter='Resolved', db_path=temp_db)
    assert len(resolved_now) == 1
    assert resolved_now[0]['id'] == original_alert_id
    assert resolved_now[0]['status'] == 'Resolved'
    assert resolved_now[0]['resolved_at'] is not None


def test_threshold_settings_validation(temp_db):
    """Verify threshold validation rules (must be numeric between 1.0 and 100.0)."""
    # Valid update
    ok, msg = monitoring.validate_and_update_settings('75.0', '70.0', '80.0', db_path=temp_db)
    assert ok is True
    settings = monitoring.get_settings(temp_db)
    assert settings['cpu_threshold'] == 75.0
    assert settings['memory_threshold'] == 70.0
    assert settings['disk_threshold'] == 80.0

    # Invalid: non-numeric
    ok, msg = monitoring.validate_and_update_settings('abc', '70.0', '80.0', db_path=temp_db)
    assert ok is False
    assert "valid numbers" in msg

    # Invalid: below 1%
    ok, msg = monitoring.validate_and_update_settings('0.0', '70.0', '80.0', db_path=temp_db)
    assert ok is False
    assert "between 1.0% and 100.0%" in msg

    # Invalid: above 100%
    ok, msg = monitoring.validate_and_update_settings('105.0', '70.0', '80.0', db_path=temp_db)
    assert ok is False
    assert "between 1.0% and 100.0%" in msg


def test_settings_update_post_route(client, temp_db):
    """Verify POST /update_settings form submission and redirection."""
    response = client.post('/update_settings', data={
        'cpu_threshold': '65.0',
        'memory_threshold': '75.0',
        'disk_threshold': '85.0'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Thresholds successfully updated' in response.data

    settings = monitoring.get_settings(temp_db)
    assert settings['cpu_threshold'] == 65.0


def test_history_and_alerts_pages_return_200(client, temp_db):
    """Verify history, alerts, and settings pages render HTTP 200."""
    res_history = client.get('/history')
    assert res_history.status_code == 200
    assert b'Historical Metrics' in res_history.data

    res_alerts = client.get('/alerts')
    assert res_alerts.status_code == 200
    assert b'Automated Incident' in res_alerts.data

    res_settings = client.get('/settings')
    assert res_settings.status_code == 200
    assert b'Configure Anomaly Thresholds' in res_settings.data

    res_api_hist = client.get('/api/history')
    assert res_api_hist.status_code == 200
    assert isinstance(res_api_hist.get_json(), list)


def test_empty_history_graceful_handling(client, temp_db):
    """Verify that an empty database is handled gracefully without errors."""
    res_history = client.get('/history')
    assert res_history.status_code == 200
    assert b'No Historical Metrics Found' in res_history.data

    res_alerts = client.get('/alerts')
    assert res_alerts.status_code == 200
    assert b'No Alerts Found' in res_alerts.data


def test_format_uptime_utility():
    """Verify uptime seconds formatter."""
    assert monitoring.format_uptime(None) == "Unavailable"
    assert monitoring.format_uptime(45) == "45s"
    assert monitoring.format_uptime(125) == "2m 5s"
    assert monitoring.format_uptime(3665) == "1h 1m 5s"
    assert monitoring.format_uptime(90061) == "1d 1h 1m 1s"


def test_pipeline_and_devops_dashboard_route(client):
    """Verify DevOps operations and CI/CD hub renders HTTP 200 without template syntax errors."""
    res_pipeline = client.get('/pipeline')
    assert res_pipeline.status_code == 200
    assert b'Jenkins' in res_pipeline.data
    assert b'Docker' in res_pipeline.data

    res_devops = client.get('/devops')
    assert res_devops.status_code == 200
