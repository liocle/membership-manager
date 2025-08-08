# .tests/test_monitoring_alerts.py

import os
import time

import pytest
import requests

skip_if_ci = pytest.mark.skipif(
    os.getenv("CI") == "true", reason="Monitoring stack not running in GitHub Actions"
)

PROM_URL = "http://localhost:9090"
ALERTMANAGER_URL = "http://localhost:9093"


@skip_if_ci
@pytest.mark.monitoring
def test_alertmanager_health():
    """Ensure Alertmanager is running and healthy"""
    resp = requests.get(f"{ALERTMANAGER_URL}/-/healthy", timeout=5)
    assert resp.status_code == 200


@skip_if_ci
@pytest.mark.monitoring
def test_prometheus_rules_loaded():
    """Verify that container_alerts rule group is loaded"""
    resp = requests.get(f"{PROM_URL}/api/v1/rules", timeout=5)
    assert resp.status_code == 200
    groups = resp.json()["data"]["groups"]
    assert any(group["name"] == "container_alerts" for group in groups)


@skip_if_ci
@pytest.mark.monitoring
def test_alert_firing_pipeline():
    """
    Confirm that an always-firing alert reaches Alertmanager.
    Assumes Prometheus is already running with this rule:
      - alert: AlwaysFiring
        expr: vector(1)
        for: 5s
    """
    for _ in range(15):
        alerts = requests.get(f"{ALERTMANAGER_URL}/api/v2/alerts").json()
        for alert in alerts:
            if alert["labels"]["alertname"] == "AlwaysFiring":
                assert alert["status"]["state"] == "active"
                return
        time.sleep(1)

    raise AssertionError(
        f"AlwaysFiring alert did not appear. Seen: {[a['labels']['alertname'] for a in alerts]}"
    )
