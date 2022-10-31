import json

from src import __version__, main


def test_version():
    assert __version__ == "0.1.0"


def test_parse_harbor_push():
    event = main.parse_harbor_event(push_artifact_payload)
    assert event["type"] == "PUSH_ARTIFACT"


def test_parse_harbor_scanning():
    event = main.parse_harbor_event(scanning_completed_payload)
    assert event["severity"] == "High"


# Example payloads

push_artifact_payload = json.loads(
    """
{
    "type": "PUSH_ARTIFACT",
    "occur_at": 1666800952,
    "operator": "robot-inveniosoftware+github-inveniosoftware",
    "event_data": {
        "resources": [{
            "digest": "sha256:1cd0c4854ecacf9deabe4e5b065d913da93a4e0f37ddfd601b70d5861c1514d9",
            "tag": "sha256:1cd0c4854ecacf9deabe4e5b065d913da93a4e0f37ddfd601b70d5861c1514d9",
            "resource_url": "registry.cern.ch/inveniosoftware/almalinux@sha256:1cd0c4854ecacf9deabe4e5b065d913da93a4e0f37ddfd601b70d5861c1514d9"
        }],
        "repository": {
            "date_created": 1666367524,
            "name": "almalinux",
            "namespace": "inveniosoftware",
            "repo_full_name": "inveniosoftware/almalinux",
            "repo_type": "public"
        }
    }
}
"""
)

scanning_completed_payload = json.loads(
    """
{
    "type": "SCANNING_COMPLETED",
    "event_data": {
        "resources": [{
            "digest": "sha256:ae884a753406c59bc5d20bd30e380fcb1857703ea538abcfb795cf3a93aabfaa",
            "resource_url": "registry.cern.ch/inveniosoftware/almalinux@sha256:ae884a753406c59bc5d20bd30e380fcb1857703ea538abcfb795cf3a93aabfaa",
            "scan_overview": {
                "application/vnd.security.vulnerability.report; version=1.1": {
                    "report_id": "15038c79-09ca-45fa-97e6-14b2a5a33276",
                    "scan_status": "Success",
                    "severity": "High",
                    "duration": 83,
                    "summary": {
                        "total": 4,
                        "fixable": 4,
                        "summary": {
                            "High": 3,
                            "Medium": 1
                        }
                    },
                    "start_time": "2022-10-26T16:15:54Z",
                    "end_time": "2022-10-26T16:17:17Z",
                    "scanner": {
                        "name": "Trivy",
                        "vendor": "Aqua Security",
                        "version": "v0.29.2"
                    },
                    "complete_percent": 100
                }
            }
        }],
        "repository": {
            "name": "almalinux",
            "namespace": "inveniosoftware",
            "repo_full_name": "inveniosoftware/almalinux",
            "repo_type": "public"
        }
    }
}
"""
)
