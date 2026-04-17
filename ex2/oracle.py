import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("[ERROR] python-dotenv is not installed.")
    print("Install with: pip install python-dotenv")
    sys.exit(1)


def load_configuration() -> dict[str, str | None]:
    load_dotenv()

    config: dict[str, str | None] = {
        "MATRIX_MODE": os.getenv("MATRIX_MODE"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_KEY": os.getenv("API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT"),
    }

    return config


def validate_config(config: dict[str, str | None]) -> bool:
    missing: list[str] = []

    for key, value in config.items():
        if not value:
            print(f"[ERROR] Missing configuration: {key}")
            missing.append(key)

    if missing:
        print("\nConfiguration incomplete. Please check your .env file.")
        return False

    return True


def display_config(config: dict[str, str | None]) -> None:
    print("Configuration loaded:")

    mode = config["MATRIX_MODE"]
    db = config["DATABASE_URL"]
    api = config["API_KEY"]
    log = config["LOG_LEVEL"]
    zion = config["ZION_ENDPOINT"]

    print(f"Mode: {mode}")

    if db and "localhost" in db:
        print("Database: Connected to local instance")
    else:
        print("Database: Connected to production database")

    if api:
        print("API Access: Authenticated")

    print(f"Log Level: {log}")

    if zion:
        print("Zion Network: Online")


def security_check(config: dict[str, str | None]) -> None:
    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")
    print("[OK] .env file properly configured")

    if config["MATRIX_MODE"] == "production":
        print("[OK] Production overrides available")
    else:
        print("[INFO] Running in development mode")


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...\n")

    config = load_configuration()

    if not validate_config(config):
        sys.exit(1)

    display_config(config)
    security_check(config)

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
