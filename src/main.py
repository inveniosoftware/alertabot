import http
import json
import os

import requests
import sentry_sdk
from fastapi import FastAPI, Header, HTTPException, Request, Response

app = FastAPI()

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

# Basic heartbeat endpoint
@app.get("/health")
def ping():
    return {"42": "foo"}


def parse_harbor_event(payload):
    event = {
        "type": payload["type"],
        "repo": payload["event_data"]["repository"]["repo_full_name"],
    }

    if event["type"] == "SCANNING_COMPLETED":
        scan_overview = payload["event_data"]["resources"][0]["scan_overview"]
        scan = list(scan_overview.values())[0]
        event["severity"] = scan["severity"]
        event["summary"] = scan["summary"]
    return event


# The endpoint here is built using the WEBHOOK_TOKEN from env and should be kept secret
@app.post(
    f'/webhook/{os.environ.get("WEBHOOK_TOKEN")}',
    status_code=http.HTTPStatus.ACCEPTED,
)
async def webhook(request: Request, response: Response):
    payload = await request.body()
    target = os.environ.get("DISCORD_TARGET").encode("utf-8")

    # Decode incoming request
    json_payload = json.loads(payload)

    try:
        event = parse_harbor_event(json_payload)
    except Exception:
        # If we can't parse the payload as an Harbor event, return a Bad Request
        response.status_code = 400
        return {"outcome": "Malformed payload"}

    # The message to be posted on Discord
    msg_content = f"""
    Event **{event["type"]}** coming from **{event["repo"]}**
    """

    # Prepare the Discord "embeds"
    if event["type"] == "SCANNING_COMPLETED":
        vuln_embed = {
            "title": "Vulnerabilities found",
            "color": 16711680,
            "description": f"{event['summary']['total']} total vulnerabilities ({event['summary']['fixable']} fixable), {event['summary']['summary']['High']} high severity.",
        }
        embeds = [vuln_embed]
    else:
        embeds = []

    # Prepare final payload to sent to the Discord webhook
    message = {
        "username": "Harbor",
        "avatar_url": "https://goharbor.io/img/logos/harbor-icon-color.png",
        "content": msg_content,
        "embeds": embeds,
    }

    # Post to the target webhook
    discord_response = requests.post(target, json=message)

    # Return success and wrap the response from Discord
    return {
        "outcome": "success",
        "discord_data": {"status_code": discord_response.status_code},
    }
