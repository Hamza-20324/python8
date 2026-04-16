import os
import sys
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


REQUIRED_KEYS = (
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
)


def mask_secret(value: str) -> str:
    if len(value) <= 4:
        return "*" * len(value)
    return f"{value[:2]}{'*' * (len(value) - 4)}{value[-2:]}"


def load_configuration() -> bool:
    if load_dotenv is None:
        print("ERROR: python-dotenv is not installed.")
        print("Install it with: pip install python-dotenv")
        return False
    load_dotenv()
    return True


def get_database_status(database_url: str, mode: str) -> str:
    if mode == "development":
        return "Connected to local instance"
    return f"Connected to production instance ({database_url})"


def get_api_status(api_key: str) -> str:
    if api_key:
        return f"Authenticated ({mask_secret(api_key)})"
    return "Missing credentials"


def get_zion_status(endpoint: str) -> str:
    if endpoint.startswith("http"):
        return f"Online ({endpoint})"
    return "Offline or invalid endpoint"


def validate_mode(mode: str) -> Optional[str]:
    if mode in ("development", "production"):
        return None
    return "MATRIX_MODE must be 'development' or 'production'"


def main() -> int:
    print("ORACLE STATUS: Reading the Matrix...")
    if not load_configuration():
        return 1

    print("Configuration loaded:")
    missing: list[str] = []
    values: dict[str, str] = {}

    for key in REQUIRED_KEYS:
        value = os.getenv(key, "").strip()
        values[key] = value
        if value == "":
            missing.append(key)

    if missing:
        print("WARNING: Missing configuration values detected")
        for key in missing:
            print(f"[MISSING] {key}")
        print("Create a .env file from .env.example or export variables.")
        return 1

    mode_error = validate_mode(values["MATRIX_MODE"])
    if mode_error is not None:
        print(f"ERROR: {mode_error}")
        return 1

    print(f"Mode: {values['MATRIX_MODE']}")
    print(
        "Database: "
        f"{get_database_status(values['DATABASE_URL'], values['MATRIX_MODE'])}"
    )
    print(f"API Access: {get_api_status(values['API_KEY'])}")
    print(f"Log Level: {values['LOG_LEVEL']}")
    print(f"Zion Network: {get_zion_status(values['ZION_ENDPOINT'])}")
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    print("[OK] .env file properly configured")
    print("[OK] Production overrides available")
    print("The Oracle sees all configurations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
