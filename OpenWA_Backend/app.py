import base64
import hashlib
import hmac
import json
import logging
import mimetypes

import requests
from flask import Flask, request, jsonify

import config
import chatbot
import state

from crm import TwentyCRM
crm = TwentyCRM()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("hypotenuse-bot")

# Keep track of delivery IDs we've already processed, to guard against
# OpenWA's at-least-once webhook delivery re-sending the same event.
_seen_delivery_ids = set()


def verify_signature(raw_body: bytes, signature_header: str) -> bool:
    """Verify X-OpenWA-Signature: sha256=<hex> against WEBHOOK_SECRET."""
    if not config.WEBHOOK_SECRET:
        return True  # no secret configured -> skip verification

    if not signature_header or not signature_header.startswith("sha256="):
        return False

    expected = hmac.new(
        config.WEBHOOK_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    received = signature_header.split("sha256=", 1)[1]
    return hmac.compare_digest(expected, received)


def send_reply(chat_id: str, text: str) -> None:
    url = f"{config.OPENWA_BASE_URL}/api/sessions/{config.OPENWA_SESSION_ID}/messages/send-text"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": config.OPENWA_API_KEY,
    }
    payload = {"chatId": chat_id, "text": text}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code not in (200, 201):\
            log.error("Failed to send reply (%s): %s", resp.status_code, resp.text)
        else:
            log.info("Reply sent successfully.")
    except requests.RequestException as exc:
        log.error("Error calling OpenWA send-text API: %s", exc)
def send_image(chat_id: str, image_path: str, caption: str = "") -> None:
    url = f"{config.OPENWA_BASE_URL}/api/sessions/{config.OPENWA_SESSION_ID}/messages/send-image"

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": config.OPENWA_API_KEY,
    }

    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        payload = {
            "chatId": chat_id,
            "base64": base64.b64encode(image_bytes).decode("utf-8"),
            "mimetype": mimetypes.guess_type(image_path)[0] or "image/png",
            "filename": image_path.split("/")[-1],
            "caption": caption,
        }

        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=20,
        )

        if resp.status_code not in (200, 201):
            log.error(
                "Failed to send image (%s): %s",
                resp.status_code,
                resp.text,
            )

    except Exception as exc:
        log.error("Error sending image: %s", exc)

def send_document(chat_id: str, doc_path: str, filename: str, caption: str = "") -> None:
    url = f"{config.OPENWA_BASE_URL}/api/sessions/{config.OPENWA_SESSION_ID}/messages/send-document"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": config.OPENWA_API_KEY,
    }
    try:
        with open(doc_path, "rb") as f:
            file_bytes = f.read()

        payload = {
            "chatId": chat_id,
            "base64": base64.b64encode(file_bytes).decode("utf-8"),
            "mimetype": "application/pdf",
            "filename": filename,
            "caption": caption,
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=30)

        if resp.status_code not in (200, 201):
            log.error("Failed to send document (%s): %s", resp.status_code, resp.text)
        else:
            log.info("Pitch deck sent successfully.")
    except Exception as exc:
        log.error("Error sending document: %s", exc)


def resolve_phone(contact_id):

    url = (
        f"{config.OPENWA_BASE_URL}/api/sessions/"
        f"{config.OPENWA_SESSION_ID}/contacts/{contact_id}/phone"
    )

    headers = {
        "X-API-Key": config.OPENWA_API_KEY
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            return None

        data = r.json()

        return data.get("phone")

    except Exception as e:
        log.error(e)
        return None

@app.route("/webhook", methods=["POST"])
def webhook():
    raw_body = request.get_data()  # raw bytes, needed for signature check
    signature_header = request.headers.get("X-OpenWA-Signature", "")

    if not verify_signature(raw_body, signature_header):
        log.warning("Rejected webhook: invalid signature")
        return jsonify({"error": "invalid signature"}), 401

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "invalid json"}), 400

    event = payload.get("event")
    delivery_id = payload.get("deliveryId")

    # Ignore anything that isn't an inbound message
    if event != "message.received":
        return jsonify({"status": "ignored"}), 200

    # De-duplicate at-least-once deliveries
    if delivery_id in _seen_delivery_ids:
        return jsonify({"status": "duplicate"}), 200
    _seen_delivery_ids.add(delivery_id)

    data = payload.get("data", {})
    chat_id = data.get("chatId") or data.get("from")
    body = data.get("body", "")

    log.info("FULL PAYLOAD:\n%s", json.dumps(data, indent=2))

    contact = data.get("contact", {})

    sender_name = (
        contact.get("pushName")
        or contact.get("name")
        or data.get("pushName")
        or data.get("notifyName")
        or "Unknown"
        )


    phone = resolve_phone(chat_id)

    log.info("Resolved phone: %s", phone)

    if not phone:
        phone = chat_id.split("@")[0]

    # Ignore messages the bot itself sent, and non-text messages
    if data.get("fromMe"):
        return jsonify({"status": "ignored_from_me"}), 200
    if not chat_id or not body:
        return jsonify({"status": "ignored_empty"}), 200

    log.info("Incoming message from %s: %r", chat_id, body)

    normalized_body = body.strip().lower()

    # Load user's conversation state
    user_state = state.get_state(chat_id)

   # Sync CRM only once per active conversation
    if not user_state.get("crm_synced", False):
        try:
            crm.sync_contact(
                name=sender_name,
                phone=phone,
                chat_id=chat_id,
            )
            user_state["crm_synced"] = True
        except Exception as e:
            log.error(f"CRM Sync Failed: {e}")

    reply_text = chatbot.handle_message(body, user_state)
    state.save_state(chat_id, user_state)

    if normalized_body == config.TRIGGER_MESSAGE.strip().lower():
        send_image(
        chat_id=chat_id,
        image_path=config.LOGO_PATH,
        caption=config.WELCOME_CAPTION,
    )
    if reply_text:
        send_reply(chat_id, reply_text)

    # Send the pitch deck PDF only when THIS message was actually "6",
    # not just because the stored stage happens to still say "pitch_deck"
    # from an earlier session (that stage never resets otherwise).
    # Sent AFTER reply_text so the caption text arrives before the file.
    if normalized_body == "6":
        send_reply(
            chat_id,
            "You can view and download our latest Hypotenuse Analytics Pitch Deck here📄:\n\nhttps://drive.google.com/file/d/1-Js1y4MY29MoorRxdd_BGNvkHTldGnph/view?usp=sharing"
    )

    if normalized_body == "7":
        send_document(
            chat_id=chat_id,
            doc_path=config.WHITE_PAPER_PATH,
            filename=config.WHITE_PAPER_FILENAME,
            caption="",
        )
        logging.info("Technical White Paper sent successfully")

    return jsonify({"status": "ok"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=False)