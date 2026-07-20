import config


def handle_message(text: str, user_state: dict) -> str:
    """
    Handles incoming WhatsApp messages.
    """

    normalized = text.strip().lower()

    # ----------------------------------------------------------
    # Website Trigger
    # ----------------------------------------------------------
    if normalized == config.TRIGGER_MESSAGE:
        user_state["stage"] = "main_menu"
        return config.MAIN_MENU

    # ----------------------------------------------------------
    # Global Menu Command
    # ----------------------------------------------------------
    if normalized == "menu":
        user_state["stage"] = "main_menu"
        return config.MAIN_MENU

    # ----------------------------------------------------------
    # Global Navigation (Works from Anywhere)
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
        user_state["stage"] = "contact_support"
        return config.CONTACT_SUPPORT

    # ----------------------------------------------------------
    # Current Stage
    # ----------------------------------------------------------
    stage = user_state.get("stage", "main_menu")

    # ----------------------------------------------------------
    # Products Menu
    # ----------------------------------------------------------
    if stage == "products_menu":
        return config.PRODUCTS_MENU

    # ----------------------------------------------------------
    # About Us
    # ----------------------------------------------------------
    elif stage == "about_us":
        return config.ABOUT_US

    # ----------------------------------------------------------
    # Critical Infrastructure
    # ----------------------------------------------------------
    elif stage == "critical_infrastructure":
        return config.PRODUCT_SHM

    # ----------------------------------------------------------
    # Surveillance
    # ----------------------------------------------------------
    elif stage == "surveillance":
        return config.PRODUCT_SURVEILLANCE

    # ----------------------------------------------------------
    # Reality Trust
    # ----------------------------------------------------------
    elif stage == "reality_trust":
        return config.PRODUCT_REALITY_TRUST

    # ----------------------------------------------------------
    # Contact Support
    # ----------------------------------------------------------
    elif stage == "contact_support":
        return config.CONTACT_SUPPORT

    # ----------------------------------------------------------
    # Default
    # ----------------------------------------------------------
    return config.FALLBACK_PROMPT