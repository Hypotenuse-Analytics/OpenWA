import os
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────────────
# OpenWA Configuration
# ─────────────────────────────────────────────────────────────
OPENWA_BASE_URL = os.getenv("OPENWA_BASE_URL")
OPENWA_API_KEY = os.getenv("OPENWA_API_KEY")
OPENWA_SESSION_ID = os.getenv("OPENWA_SESSION_ID")
TWENTY_BASE_URL = os.getenv("TWENTY_BASE_URL")
TWENTY_API_KEY = os.getenv("TWENTY_API_KEY")

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")

PITCH_DECK_PATH = "assets/PitchDeck_v2.0.pdf"
PITCH_DECK_FILENAME = "Hypotenuse_Analytics_Pitch_Deck.pdf"

WHITE_PAPER_PATH = "assets/HypotenuseAnalytics_TechnicalWhitePaper_Version2_2026.pdf"
WHITE_PAPER_FILENAME = "Hypotenuse_Analytics_Technical_White_Paper.pdf"

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
    "Predict Protect Verify"
)

LOGO_PATH = "assets/hypotenuse_logo.png"

# ─────────────────────────────────────────────────────────────
# Main Menu
# ─────────────────────────────────────────────────────────────

MAIN_MENU = (
    "Thank you for contacting Hypotenuse Analytics.\n\n"

    "How can we assist you today? Please select an option:\n\n"

    "1. About Us\n"
    "2. Products\n"
    "3. Critical Infrastructure Intelligence\n"
    "4. Surveillance Intelligence Lab™\n"
    "5. Reality Trust Center™\n"
    "6. Pitch Deck\n"
    "7. Technical White Paper\n"
    "8. Contact Support\n"
)

# ─────────────────────────────────────────────────────────────
# About Us
# ─────────────────────────────────────────────────────────────

ABOUT_US = (
    "*About Hypotenuse Analytics*\n\n"

    "Hypotenuse Analytics is a unified AI platform built to answer three "
    "questions that matter to anyone running a physical site:\n\n"

    "• Is this structure safe?\n"
    "• Is something unusual happening here?\n"
    "• Is this piece of evidence real?\n\n"

    "We bring together Critical Infrastructure Intelligence, Surveillance "
    "Intelligence, and our Reality Trust Center (powered by ZSure) on a "
    "single AI-native platform, so evidence from sensors, cameras, and "
    "documents can be cross-checked against each other instead of living "
    "in disconnected systems.\n\n"

    "Our platform monitors structures from the first day of construction "
    "through decades of operation, runs efficiently on on-site edge "
     "hardware, and keeps sensitive data on-site by design.\n\n"

    "Every AI prediction is validated against real engineering physics "
    "before an alert is ever raised.\n\n"
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
    "railways, tunnels, dams, and industrial facilities, from the first "
    "day of construction through decades of operation.\n\n"

    "• The platform combines vibration, strain, displacement, and thermal "
    "sensor data with satellite radar and laser scanning to detect risks "
    "long before they become failures.\n\n"

    "• Every alert is linked to real on-site activity, such as excavation, "
    "blasting, or weather, and checked against real engineering physics "
    "before it ever reaches you.\n\n"

    "• A live Digital Twin of the structure, built from real sensor and "
    "scan data rather than a static 3D model, lets you see exactly how it "
    "behaves and even simulate what happens under future loads.\n\n"

    "• The result is a live view of structural health and a maintenance "
    "schedule built around actual condition rather than a fixed calendar, "
    "using the sensors you already have in place.\n\n"
)

PRODUCT_SURVEILLANCE = (
    "*Surveillance Intelligence Lab™*\n\n"

    "Advanced AI video analytics that turns your existing CCTV cameras "
    "into an active monitoring system, instead of a wall of feeds no "
    "one can fully watch.\n\n"

    "• The platform predicts movement before it happens, follows people "
    "and vehicles across multiple cameras as a single continuous path, "
    "and reads number plates accurately even in poor conditions.\n\n"

    "• Every detection is mapped onto a live Digital Twin of your site, "
    "so you see exactly where an event is happening rather than just "
    "which camera caught it.\n\n"

    "• When an incident occurs, the platform automatically builds a "
    "clear, plain-language timeline from every camera involved.\n\n"

    "• Most processing happens on-site, keeping alerts fast and footage "
    "private, and every alert is followed through by a named person "
    "until it's resolved.\n\n"
)

PRODUCT_REALITY_TRUST = (
    "*Reality Trust Center™*\n\n"

    "AI-powered deepfake and forged-document detection for videos, "
    "images, voice recordings, and documents.\n\n"

    "• Rather than a plain yes-or-no answer, the platform highlights "
    "exactly what led to its conclusion, whether it's a specific region "
    "of an image, a voice pattern, or a document inconsistency, giving "
    "you evidence you can act on with confidence.\n\n"

    "• It's built to catch new manipulation techniques, not just "
    "familiar ones, and can cross-check flagged content against real "
    "camera footage or sensor data from the same site for an added "
    "layer of certainty.\n\n"
)



WHITE_PAPER_CAPTION = (
    "*Hypotenuse Analytics — Technical White Paper*\n\n"
    "Attached is our Technical White Paper, providing an in-depth overview of our platform, its underlying technologies, system architecture, and key innovations."
)

# ─────────────────────────────────────────────────────────────
# Contact
# ─────────────────────────────────────────────────────────────

CONTACT_SUPPORT = (
    "*Contact Support*\n\n"

    "Email: info@hypotenuseanalytics.com\n\n"

    "Website: https://www.hypotenuseanalytics.com\n"
    "ZSure: https://www.zsure.in/\n\n"

    "Our team will be happy to assist you.\n"
)

# ─────────────────────────────────────────────────────────────
# Fallback
# ─────────────────────────────────────────────────────────────

FALLBACK_PROMPT = (
    "Invalid option.\n\n"
    "Reply *Menu* to return to the main menu."
)