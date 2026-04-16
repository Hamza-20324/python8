import os
import site
import sys


def in_virtual_environment() -> bool:
    return (
        hasattr(sys, "real_prefix")
        or sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    )


def get_environment_name() -> str:
    return os.path.basename(sys.prefix)


def get_site_packages_path() -> str:
    paths = site.getsitepackages()
    if paths:
        return paths[0]
    return "Unavailable"


if in_virtual_environment():
    print("MATRIX STATUS: Welcome to the construct")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {get_environment_name()}")
    print(f"Environment Path: {sys.prefix}")
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print("Package installation path:")
    print(get_site_packages_path())
else:
    print("MATRIX STATUS: You're still plugged in")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print("To enter the construct, run:")
    print("python3 -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print(r"matrix_env\Scripts\activate # On Windows")
    print("Then run this program again.")
    print("Global package installation path:")
    print(get_site_packages_path())
