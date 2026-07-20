import base64
import hashlib
import hmac
import logging
import mimetypes

import requests
from flask import Flask, request, jsonify

import config
import chatbot
import state

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
        if resp.status_code != 200:
            log.error("Failed to send reply (%s): %s", resp.status_code, resp.text)
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

    # Ignore messages the bot itself sent, and non-text messages
    if data.get("fromMe"):
        return jsonify({"status": "ignored_from_me"}), 200
    if not chat_id or not body:
        return jsonify({"status": "ignored_empty"}), 200

    log.info("Incoming message from %s: %r", chat_id, body)

    user_state = state.get_state(chat_id)
    reply_text = chatbot.handle_message(body, user_state)
    state.save_state(chat_id, user_state)

    if body.strip().lower() == config.TRIGGER_MESSAGE.strip().lower():
        send_image(
        chat_id=chat_id,
        image_path=config.LOGO_PATH,
        caption=config.WELCOME_CAPTION,
    )

    send_reply(chat_id, reply_text)

    return jsonify({"status": "ok"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=False)
