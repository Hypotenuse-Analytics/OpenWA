import os

# ─────────────────────────────────────────────────────────────
# OpenWA Configuration
# ─────────────────────────────────────────────────────────────

OPENWA_BASE_URL = os.environ.get(
    "OPENWA_BASE_URL",
    "http://localhost:2785"
)

OPENWA_API_KEY = os.environ.get(
    "OPENWA_API_KEY",
    "owa_k1_044acb58ff6267297ffdb710191761fe1ca7ad0c39acd856d8b4c38531ddd342"
)

OPENWA_SESSION_ID = os.environ.get(
    "OPENWA_SESSION_ID",
    "2f6ad25b-ce04-4272-bf33-271d7287668b"
)

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")

# ─────────────────────────────────────────────────────────────
# Flask
# ─────────────────────────────────────────────────────────────

FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

# ─────────────────────────────────────────────────────────────
# User State
# ─────────────────────────────────────────────────────────────

STATE_FILE = "users.json"
IDLE_TIMEOUT_SECONDS = 15 * 60

# ─────────────────────────────────────────────────────────────
# Trigger Message
# (Sent automatically from website WhatsApp button)
# ─────────────────────────────────────────────────────────────

TRIGGER_MESSAGE = (
    "hi hypotenuse analytics, i'd like to learn more about your platform."
)

# ─────────────────────────────────────────────────────────────
# Logo
# ─────────────────────────────────────────────────────────────

WELCOME_CAPTION = (
    "Welcome to Hypotenuse Analytics\n\n"
    "Predict. Protect. Verify."
)

LOGO_PATH = "assets/hypotenuse_logo.png"

# ─────────────────────────────────────────────────────────────
# Main Menu
# ─────────────────────────────────────────────────────────────

MAIN_MENU = (
    "Thank you for contacting Hypotenuse Analytics.\n\n"

    "Please choose an option:\n\n"

    "1. About Us\n"
    "2. Products\n"
    "3. Critical Infrastructure Intelligence\n"
    "4. Surveillance Intelligence Lab™\n"
    "5. Reality Trust Center™\n"
    "6. Contact Support\n\n"

    "Reply with the option number to continue."
)

# ─────────────────────────────────────────────────────────────
# About Us
# ─────────────────────────────────────────────────────────────

ABOUT_US = (
    "*About Hypotenuse Analytics*\n\n"

    "Hypotenuse Analytics is a unified multi-modal AI inference platform "
    "that transforms fragmented signals into operational intelligence.\n\n"

    "Our platform combines AI, computer vision, sensor telemetry, "
    "video analytics, and deep learning to help organizations "
    "predict risks, protect critical assets, and verify digital trust.\n\n"

    "Reply *Menu* to return to the main menu."
)

# ─────────────────────────────────────────────────────────────
# Products
# ─────────────────────────────────────────────────────────────

PRODUCTS_MENU = (
    "*Products*\n\n"

    "1. Critical Infrastructure Intelligence\n"
    "2. Surveillance Intelligence Lab™\n"
    "3. Reality Trust Center™\n\n"

)

# ─────────────────────────────────────────────────────────────
# Product Details
# ─────────────────────────────────────────────────────────────

PRODUCT_SHM = (
    "*Critical Infrastructure Intelligence*\n\n"

    "AI-powered Structural Health Monitoring for bridges, buildings, "
    "railways, tunnels, dams, industrial facilities, and other critical "
    "infrastructure.\n\n"

    "Uses sensors, computer vision, and predictive analytics to detect "
    "risks before failures occur.\n\n"
)
PRODUCT_SURVEILLANCE = (
    "*Surveillance Intelligence Lab™*\n\n"

    "Advanced AI video analytics platform that delivers real-time "
    "threat detection, anomaly detection, behavior analysis, "
    "cross-camera intelligence, and operational insights.\n\n"

)
PRODUCT_REALITY_TRUST = (
    "*Reality Trust Center™*\n\n"

    "AI-powered deepfake detection and digital authenticity platform "
    "for verifying videos, images, audio, documents, and digital identities.\n\n"
)
# ─────────────────────────────────────────────────────────────
# Contact
# ─────────────────────────────────────────────────────────────

CONTACT_SUPPORT = (
    "*Contact Support*\n\n"

    "Email: info@hypotenuseanalytics.com\n"
    "Website: https://www.hypotenuseanalytics.com\n\n"

    "Our team will be happy to assist you.\n\n"

    "Reply *Menu* to return."
)

# ─────────────────────────────────────────────────────────────
# Fallback
# ─────────────────────────────────────────────────────────────

FALLBACK_PROMPT = (
    "Invalid option.\n\n"
    "Reply *Menu* to return to the main menu."
)