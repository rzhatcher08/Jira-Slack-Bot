# Jira-Slack-Bot
Slack bot that creates Jira tickets from structured messages


# 🧠 Jira Slack Bot

This is a Slack bot that listens for structured messages in a Slack channel and creates Jira tickets automatically.

---

## ✨ Features

- Listens for messages in the format:
Story: As a user, I want to...
Epic: ...
Story Points: ...
Description: ...
Labels: ...
Priority: ...

- Parses content using regex
- Sends API request to Jira Cloud
- Posts a confirmation in Slack

---

## 🎥 Loom Demo

Watch a video walkthrough of how it works:  
<div style="position: relative; padding-bottom: 62.5%; height: 0;"><iframe src="https://www.loom.com/embed/1d3426a8a4454187958a8e640d1fb98b?sid=54c73418-869c-4d29-95c3-fb730918ffe5" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

---

## ⚙️ Technologies Used

- Python
- Flask
- Slack Bolt SDK
- Jira Cloud REST API
- Ngrok (for local development tunneling)
