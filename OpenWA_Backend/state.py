import json
import os
import time
import threading
import config

_lock = threading.Lock()


def _load_all() -> dict:
    if not os.path.exists(config.STATE_FILE):
        return {}
    try:
        with open(config.STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_all(data: dict) -> None:
    tmp_path = config.STATE_FILE + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, config.STATE_FILE)  # atomic on same filesystem


def get_state(user_id: str) -> dict:
    """
    Returns the conversation state dict for a user.
    Resets to main_menu automatically if the user has been idle
    longer than IDLE_TIMEOUT_SECONDS.
    """
    with _lock:
        all_states = _load_all()
        user_state = all_states.get(user_id)

        if user_state is None:
            return {
                "crm_synced": False
            }

        last_seen = user_state.get("last_seen", 0)
        if time.time() - last_seen > config.IDLE_TIMEOUT_SECONDS:
            return {
                "crm_synced": False
            }

        return user_state


def save_state(user_id: str, user_state: dict) -> None:
    user_state["last_seen"] = time.time()
    with _lock:
        all_states = _load_all()
        all_states[user_id] = user_state
        _save_all(all_states)
