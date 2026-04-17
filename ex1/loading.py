import importlib
from types import ModuleType


def check_package(name: str) -> tuple[ModuleType | None, str | None]:
    try:
        package = importlib.import_module(name)
        version = getattr(package, "__version__", "unknown")
        return package, version
    except ImportError:
        return None, None


def check_dependencies() -> bool:
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")

    descriptions: dict[str, str] = {
        "pandas": "Data manipulation ready",
        "numpy": "Numerical computation ready",
        "matplotlib": "Visualization ready",
    }

    required: list[str] = ["pandas", "numpy", "matplotlib"]
    missing: list[str] = []

    for pkg in required:
        module, version = check_package(pkg)
        if module:
            print(f"[OK] {pkg} ({version}) - {descriptions[pkg]}")
        else:
            print(f"[MISSING] {pkg}")
            missing.append(pkg)

    if missing:
        print("\nMissing dependencies!")
        print("Install with:")
        print("pip install -r requirements.txt")
        print("or")
        print("poetry install")
        return False

    return True


def main() -> None:
    np, _ = check_package("numpy")
    pd, _ = check_package("pandas")
    plt = importlib.import_module("matplotlib.pyplot")

    data = np.random.rand(1000)  # type: ignore

    print("\nAnalyzing Matrix data...")
    print(f"Processing {len(data)} data points...")

    df = pd.DataFrame(data, columns=["values"])  # type: ignore

    print("Generating \n")
    plt.plot(df["values"])
    plt.title("Matrix Data")
    plt.savefig("matrix_analysis.png")

    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    if check_dependencies():
        main()
