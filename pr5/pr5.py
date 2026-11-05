"""Скрипт перевірки середовища розробки."""

import importlib
import sys


def check_python_version():
    """Перевіряє версію Python (потрібна >= 3.10)."""
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("  УВАГА: Потрібна версія Python >= 3.10! Спробуйте оновити Python.")
    else:
        print("  Версія Python відповідає вимогам (>= 3.10) ✓")


def check_package(package_name: str) -> bool:
    """Перевіряє, чи встановлено пакет, і виводить його версію.

    Args:
        package_name: назва пакета для перевірки.

    Returns:
        True, якщо пакет встановлено.
    """
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, '__version__', 'невідома')
        print(f"  {package_name}: {version} ✓")
        return True
    except ImportError:
        print(f"  {package_name}: НЕ ВСТАНОВЛЕНО ✗")
        return False


def main():
    check_python_version()

    print("\nВстановлені пакети:")
    packages = ['django', 'flask']
    results = {pkg: check_package(pkg) for pkg in packages}

    
    installed = [pkg for pkg, status in results.items() if status]
    missing = [pkg for pkg, status in results.items() if not status]

    print(f"\nПідсумок: встановлено {len(installed)} з {len(packages)} пакетів.")

    if missing:
        missing_str = " ".join(missing)
        print(f"  Відсутні пакети: {', '.join(missing)}")
        print(f"  Виконайте таку команду для встановлення:\n    pip install {missing_str}")
    else:
        print("  Усі необхідні пакети успішно встановлені!")


if __name__ == "__main__":
    main()
