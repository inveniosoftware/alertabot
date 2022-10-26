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


@app.post("/webhook/7938421", status_code=http.HTTPStatus.ACCEPTED)
async def webhook(request: Request, x_hub_signature: str = Header(None)):
    payload = await request.body()
    secret = os.environ.get("WEBHOOK_SECRET").encode("utf-8")
    target = os.environ.get("DISCORD_TARGET").encode("utf-8")

    # Decode incoming request
    json_payload = json.loads(payload)

    print(json_payload)
    
    # Prepare payload to post to Discord
    message = {
        "username": "Harbor",
        "avatar_url": "https://goharbor.io/img/logos/harbor-icon-color.png",
        "content": f'Event {json_payload["type"]} coming from TODO',
    }

    # Post to the target webhook
    x = requests.post(target, json=message)

    print(x.content)
    return {"ecoci"}
