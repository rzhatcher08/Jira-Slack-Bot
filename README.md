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
👉 https://www.loom.com/share/a87d4bf97ce948429b232b716b31481c?sid=b488beaa-cef9-4f91-839d-3345db48bd03 

---

## ⚙️ Technologies Used

- Python
- Flask
- Slack Bolt SDK
- Jira Cloud REST API
- Ngrok (for local development tunneling)
