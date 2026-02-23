"""
WhatsApp Business Cloud API utilities.
Wraps Meta Graph API for sending and parsing webhook payloads.

Meta docs: https://developers.facebook.com/docs/whatsapp/cloud-api/
"""
import json
import logging
import requests

logger = logging.getLogger(__name__)

META_API_BASE = "https://graph.facebook.com/v18.0"


# ──────────────────────────────────────────────────────────────
# SEND
# ──────────────────────────────────────────────────────────────

def send_whatsapp_message(config, to_phone: str, body: str, reply_to_wamid: str = None) -> dict:
    """
    Send a text message via Meta WhatsApp Cloud API.

    Args:
        config:          CompanyWhatsAppConfig instance (must have valid credentials).
        to_phone:        Recipient phone number in E.164 format, e.g. "+351912345678".
                         Leading "+" is stripped automatically if present.
        body:            Plain-text message body (max 4096 chars).
        reply_to_wamid:  Optional WhatsApp Message ID to thread the reply under.

    Returns:
        dict with keys:
            success (bool)
            wamid   (str)  — WhatsApp Message ID on success
            error   (str)  — human-readable error on failure
            raw     (dict) — full API response body
    """
    # Normalise phone: strip + and spaces
    to_phone_clean = to_phone.strip().lstrip("+").replace(" ", "").replace("-", "")

    token = config.get_decrypted_token()
    phone_number_id = config.phone_number_id

    url = f"{META_API_BASE}/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload: dict = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_phone_clean,
        "type": "text",
        "text": {"preview_url": False, "body": body},
    }

    if reply_to_wamid:
        payload["context"] = {"message_id": reply_to_wamid}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        raw = resp.json()

        if resp.ok and raw.get("messages"):
            wamid = raw["messages"][0].get("id", "")
            logger.info("[WhatsApp] Message sent → %s | wamid=%s", to_phone_clean, wamid)
            return {"success": True, "wamid": wamid, "error": "", "raw": raw}

        # API returned an error JSON
        error_detail = raw.get("error", {})
        error_msg = error_detail.get("message", str(raw))
        logger.error("[WhatsApp] Send failed: %s", error_msg)
        return {"success": False, "wamid": "", "error": error_msg, "raw": raw}

    except requests.RequestException as exc:
        logger.exception("[WhatsApp] Network error sending to %s", to_phone_clean)
        return {"success": False, "wamid": "", "error": str(exc), "raw": {}}


# ──────────────────────────────────────────────────────────────
# WEBHOOK PARSING
# ──────────────────────────────────────────────────────────────

def parse_webhook_payload(data: dict) -> list[dict]:
    """
    Parse a raw Meta webhook POST body and extract inbound text messages.

    Args:
        data: Parsed JSON body from the webhook POST request.

    Returns:
        List of message dicts, each containing:
            wamid      (str)  — WhatsApp Message ID
            from_phone (str)  — sender phone in E.164 without leading "+"
            to_phone   (str)  — recipient (your number), may be empty
            body       (str)  — message text
            timestamp  (int)  — Unix timestamp
            wa_name    (str)  — sender display name (may be empty)
    """
    messages = []
    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})

                if change.get("field") != "messages":
                    continue

                contacts = {c["wa_id"]: c.get("profile", {}).get("name", "")
                            for c in value.get("contacts", [])}

                for msg in value.get("messages", []):
                    # Only handle text messages for now
                    if msg.get("type") != "text":
                        logger.debug("[WhatsApp] Skipping non-text message type: %s", msg.get("type"))
                        continue

                    messages.append({
                        "wamid": msg.get("id", ""),
                        "from_phone": msg.get("from", ""),
                        "to_phone": value.get("metadata", {}).get("display_phone_number", ""),
                        "body": msg.get("text", {}).get("body", ""),
                        "timestamp": int(msg.get("timestamp", 0)),
                        "wa_name": contacts.get(msg.get("from", ""), ""),
                    })

    except (KeyError, TypeError, ValueError) as exc:
        logger.warning("[WhatsApp] Error parsing webhook payload: %s", exc)

    return messages


# ──────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────

def normalise_phone(phone: str) -> str:
    """
    Strip non-digit characters to get a bare phone number for DB lookups.
    E.g.  "+351 912 345 678"  →  "351912345678"
    """
    return "".join(c for c in phone if c.isdigit())


def phones_match(a: str, b: str) -> bool:
    """
    Compare two phone numbers by their digits only.
    Also matches if one is a suffix of the other (local vs E.164).
    """
    da, db = normalise_phone(a), normalise_phone(b)
    if not da or not db:
        return False
    return da == db or da.endswith(db) or db.endswith(da)
