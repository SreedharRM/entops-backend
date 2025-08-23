import os
from agentmail import AgentMail

def sendmes(
    inbox_id: str,
    to: str | list[str],
    subject: str,
    text: str = None,
    html: str = None,
    cc: str | list[str] = None,
    bcc: str | list[str] = None,
    labels: list[str] = None,
    reply_to: str | list[str] = None,
    attachments: list[dict] = None
):
    # Get API key from environment
    api_key = "fe14c6b65b37a6174abc483730488cbec7edb9a2c1499ed8aecfe42e2e8d96e4"
    if not api_key:
        raise ValueError("AGENTMAIL_API_KEY environment variable is not set")

    client = AgentMail(api_key=api_key)

    # Build message payload dynamically
    message_data = {
        "inbox_id": "shinyproperty819@agentmail.to",
        "to": "bhargavicon123@gmail.com",
        "subject": "subject",
    }

    message_data["cc"] = "bhargavicon123@gmail.com"

    # Send message
    response = client.inboxes.messages.send(**message_data)
    return response
