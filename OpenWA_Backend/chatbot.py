import config

import requests


def handle_message(text: str, user_state: dict) -> str:
    """
    Handles incoming WhatsApp messages.
    """

    normalized = text.strip().lower()

    # ----------------------------------------------------------
    # Website Trigger — this is the ONLY thing that can (re)start
    # or continue a session. It always wins, regardless of state.
    # ----------------------------------------------------------
    if normalized == config.TRIGGER_MESSAGE:
        user_state["stage"] = "main_menu"
        return config.MAIN_MENU

    # ----------------------------------------------------------
    # No active session yet -> stay completely silent for
    # anything else, including "hi", "hello", random words, etc.
    # ----------------------------------------------------------
    if "stage" not in user_state:
        return ""

    # ----------------------------------------------------------
    # We DO have an active session at this point. Only respond
    # to recognized menu commands. Anything else (stray "hi",
    # "hello", typos, etc.) is ignored -> bot stays silent
    # instead of re-showing menu/product content.
    # ----------------------------------------------------------
    valid_commands = {"1", "2", "3", "4", "5", "6",  "7", "8","menu", "0"}

    if normalized not in valid_commands:
        return ""

    # "menu" or "0" always returns to main menu
    if normalized in ("menu", "0"):
        user_state["stage"] = "main_menu"
        return config.MAIN_MENU

    # ----------------------------------------------------------
    # Global Navigation (Works from Anywhere in an active session)
    # ----------------------------------------------------------
    if normalized == "1":
        user_state["stage"] = "about_us"
        return config.ABOUT_US

    elif normalized == "2":
        user_state["stage"] = "products_menu"
        return config.PRODUCTS_MENU

    elif normalized == "3":
        user_state["stage"] = "critical_infrastructure"
        return config.PRODUCT_SHM

    elif normalized == "4":
        user_state["stage"] = "surveillance"
        return config.PRODUCT_SURVEILLANCE

    elif normalized == "5":
        user_state["stage"] = "reality_trust"
        return config.PRODUCT_REALITY_TRUST

    elif normalized == "6":
        user_state["stage"] = "pitch_deck"
        return ""
    
    elif normalized == "7":
        user_state["stage"] = "technical_whitepaper"
        return config.WHITE_PAPER_CAPTION

    elif normalized == "8":
        user_state["stage"] = "contact_support"
        return config.CONTACT_SUPPORT

    # Should never reach here, but stay silent just in case.
    return ""