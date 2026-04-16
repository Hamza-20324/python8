import importlib
import importlib.util
import sys
from typing import Any


PACKAGE_DESCRIPTIONS = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
    "requests": "Network access ready",
}


def module_available(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def get_module_version(module_name: str) -> str:
    try:
        module = importlib.import_module(module_name)
        version: str = getattr(module, "__version__", "unknown")
        return version
    except Exception:
        return "unknown"


def print_dependency_status() -> dict[str, str]:
    installed: dict[str, str] = {}

    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")
    for module_name in ("pandas", "numpy", "matplotlib", "requests"):
        if module_available(module_name):
            version = get_module_version(module_name)
            installed[module_name] = version
            print(
                f"[OK] {module_name} ({version})"
                f" - {PACKAGE_DESCRIPTIONS[module_name]}"
            )
        else:
            print(f"[MISSING] {module_name} - Not installed")
    return installed


def print_install_help() -> None:
    print("Missing required dependencies.")
    print("Install them with pip:")
    print("pip install -r requirements.txt")
    print("Or with Poetry:")
    print("poetry install")


def print_manager_comparison(installed: dict[str, str]) -> None:
    print("Dependency management comparison:")
    print("- pip uses requirements.txt to pin package versions.")
    print("- Poetry uses pyproject.toml and resolves dependencies.")
    if installed:
        print("Installed package versions detected in this environment:")
        for module_name, version in installed.items():
            print(f"  * {module_name}: {version}")


def build_dataset(np_module: Any, pd_module: Any) -> Any:
    signal = np_module.random.normal(loc=50, scale=12, size=1000)
    drift = np_module.linspace(-5, 5, 1000)
    values = signal + drift
    indexes = np_module.arange(1, 1001)
    return pd_module.DataFrame(
        {
            "cycle": indexes,
            "signal_strength": values,
        }
    )


def analyze_and_plot() -> str:
    pandas_module = importlib.import_module("pandas")
    numpy_module = importlib.import_module("numpy")
    matplotlib_module = importlib.import_module("matplotlib.pyplot")

    print("Analyzing Matrix data...")
    dataframe = build_dataset(numpy_module, pandas_module)
    print(f"Processing {len(dataframe)} data points...")

    dataframe["rolling_mean"] = dataframe["signal_strength"].rolling(
        window=25,
        min_periods=1,
    ).mean()

    print("Generating visualization...")
    figure = matplotlib_module.figure(figsize=(10, 5))
    axes = figure.add_subplot(111)
    axes.plot(dataframe["cycle"], dataframe["signal_strength"], label="Signal")
    axes.plot(
        dataframe["cycle"],
        dataframe["rolling_mean"],
        label="Rolling Mean",
    )
    axes.set_title("Matrix Signal Analysis")
    axes.set_xlabel("Cycle")
    axes.set_ylabel("Signal Strength")
    axes.legend()
    output_name = "matrix_analysis.png"
    figure.tight_layout()
    figure.savefig(output_name)
    matplotlib_module.close(figure)
    print("Analysis complete!")
    print(f"Results saved to: {output_name}")
    return output_name


def main() -> int:
    installed = print_dependency_status()
    print_manager_comparison(installed)

    required = ("pandas", "numpy", "matplotlib")
    missing_required = [name for name in required if name not in installed]
    if missing_required:
        print_install_help()
        return 1

    analyze_and_plot()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
