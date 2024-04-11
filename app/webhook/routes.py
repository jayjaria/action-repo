from flask import Blueprint, request, jsonify, json
import requests

bp = Blueprint("Webhook", __name__, url_prefix="/webhook")
URL = "http://127.0.0.1:5001/webhook/receiver"


@bp.route("/", methods=["POST"])
def call_webhook():
    if "X-Github-Event" in request.headers:
        event = request.headers["X-Github-Event"]

        # {author} pushed to {to_branch} on {timestamp}

        msg = {}
        if event == "push":

            pusher = request.json.get("pusher")
            head_commit = request.json.get("head_commit")
            ref = request.json.get("ref")
            msg["req_id"] = request.json.get("after")

            if pusher:
                msg["author"] = pusher["name"]
            if head_commit:
                msg["timestamp"] = head_commit["timestamp"]
            if ref:
                msg["to_branch"] = ref.split("/")[-1]

            msg["action"] = "PUSH"

        elif event == "pull_request":

            action = request.json.get("action")
            pull_request = request.json.get("pull_request")
            head = pull_request.get("head")
            base = pull_request.get("base")

            if action == "synchronize":
                return {}, 200

            if pull_request:
                msg["timestamp"] = pull_request["created_at"]
            if head:
                msg["from_branch"] = head["ref"]
            if base:
                msg["to_branch"] = base["ref"]
                msg["author"] = base["label"].split(":")[0]

            msg["action"] = "MERGE" if action == "closed" else "PULL"

        headers = {
            "Content-Type": "application/json",
        }
        requests.post(URL, data=json.dumps(msg), headers=headers)

    return {}, 200


@bp.route("/", methods=["GET"])
def hello():
    return "WELCOME"
