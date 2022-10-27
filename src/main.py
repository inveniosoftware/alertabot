import hashlib
import hmac
import http
import json
import os

import requests
from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def generate_hash_signature(
    secret: bytes,
    payload: bytes,
    digest_method=hashlib.sha1,
):
    return hmac.new(secret, payload, digest_method).hexdigest()


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


@app.post("/webhook/1", status_code=http.HTTPStatus.ACCEPTED)
async def webhook(request: Request, x_hub_signature: str = Header(None)):
    payload = await request.body()
    secret = os.environ.get("WEBHOOK_SECRET").encode("utf-8")
    target = os.environ.get("DISCORD_TARGET").encode("utf-8")

    # Decode incoming request
    json_payload = json.loads(payload)

    event = parse_harbor_event(json_payload)

    msg_content = f"""
    Event **{event["type"]}** coming from **{event["repo"]}**
    """

    if event["type"] == "SCANNING_COMPLETED":
        vuln_embed = {
            "title": "Vulnerabilities found",
            "color": 16711680,
            "description": f"{event['summary']['total']} total vulnerabilities ({event['summary']['fixable']} fixable), {event['summary']['summary']['High']} high severity.",
        }
        embeds = [vuln_embed]
    else:
        embeds = []

    # Prepare payload to post to Discord
    message = {
        "username": "Harbor",
        "avatar_url": "https://goharbor.io/img/logos/harbor-icon-color.png",
        "content": msg_content,
        "embeds": embeds,
    }

    # Post to the target webhook
    x = requests.post(target, json=message)

    print(x.content)
    return {"ecoci"}
