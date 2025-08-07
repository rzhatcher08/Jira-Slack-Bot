from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request, make_response
from dotenv import load_dotenv
import os
import re
import requests
from requests.auth import HTTPBasicAuth
# Load environment variables
load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

# Initialize Slack app
app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

# Flask setup
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# 🔥 Your Slack event handler
import re

@app.event("message")
def handle_message_events(event, say):
    text = event.get("text", "")
    user = event.get("user")

    print("📩 MESSAGE TEXT:", text)

    if event.get("subtype") is not None:
        return  # Skip messages from bots or edits

    # Extract fields using regex
    story_match = re.search(r"Story:\s*(.*)", text, re.IGNORECASE)
    epic_match = re.search(r"Epic:\s*(.*)", text, re.IGNORECASE)
    points_match = re.search(r"Story Points:\s*(\d+)", text, re.IGNORECASE)
    desc_match = re.search(r"Description:\s*(.*)", text, re.IGNORECASE)
    labels_match = re.search(r"Labels:\s*(.*)", text, re.IGNORECASE)
    priority_match = re.search(r"Priority:\s*(.*)", text, re.IGNORECASE)

    if not story_match:
        say(f"⚠️ Hi <@{user}>, I couldn't find a `Story:` in your message.")
        return

    # Extracted values
    story = story_match.group(1).strip()
    epic = epic_match.group(1).strip() if epic_match else None
    story_points = int(points_match.group(1)) if points_match else None
    description = desc_match.group(1).strip() if desc_match else None
    labels = [l.strip() for l in labels_match.group(1).split(",")] if labels_match else []
    priority = priority_match.group(1).strip() if priority_match else "Medium"

    # Confirm parsed story
    say(
        f"✅ Thanks <@{user}>! Here’s what I got:\n"
        f"*Story*: {story}\n"
        f"*Epic*: {epic or 'None'}\n"
        f"*Story Points*: {story_points or 'None'}\n"
        f"*Description*: {description or 'None'}\n"
        f"*Labels*: {', '.join(labels) if labels else 'None'}\n"
        f"*Priority*: {priority}"
    )
    # 🚀 Call Jira API
    jira_key = create_jira_issue(
        summary=story,
        description=description,
        epic=epic,
        story_points=story_points,
        labels=labels,
        priority=priority
    )
    

    if jira_key:
        say(f"🎫 Jira ticket *{jira_key}* created successfully!")
    else:
        say(f"❌ Sorry <@{user}>, I couldn’t create the Jira ticket.")

    # TODO: Send this to Jira
def create_jira_issue(summary, description, epic=None, story_points=None, labels=[], priority="Medium"):
    url = f"{JIRA_URL}/rest/api/3/issue"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    issue_fields = {
    "project": {"key": JIRA_PROJECT_KEY},
    "summary": summary,
    "description": {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": description or summary
                    }
                ]
            }
        ]
    },
    "issuetype": {"name": "Story"},
    "priority": {"name": priority},
    "labels": labels
}


    

    payload = {"fields": issue_fields}

    # ✅ Add this to print what you're sending
    print("📦 Payload being sent to Jira:", payload)



    response = requests.post(url, json=payload, headers=headers, auth=auth)

    # ✅ Add this to print the full response
    print("📥 Jira response code:", response.status_code)
    print("📥 Jira response body:", response.text)

    if response.status_code == 201:
        return response.json()["key"]
    else:
        return None 

    response = requests.post(url, json=payload, headers=headers, auth=auth)

    if response.status_code == 201:
        return response.json()["key"]
    else:
        print("❌ Jira error:", response.status_code, response.text)
        return None

# 🔐 URL Verification + Event Routing
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    payload = request.get_json()

    # ✅ Handle Slack's URL verification challenge
    if payload.get("type") == "url_verification":
        return make_response(payload["challenge"], 200, {"content_type": "text/plain"})

    # 🔁 Forward all other events to Bolt
    return handler.handle(request)

# 🚀 Start the Flask app
if __name__ == "__main__":
    flask_app.run(port=3000)
