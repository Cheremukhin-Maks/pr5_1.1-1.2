"""Генератор requirements.txt з перевіркою залежностей."""

import json
import os
import subprocess
import sys


def get_installed_packages() -> list[dict]:
    """Повертає список встановлених пакетів з версіями.

    Returns:
        Список словників {'name': ..., 'version': ...}.
    """
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'list', '--format=json'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return json.loads(result.stdout)
    return []


def generate_requirements(packages: list[dict], filename: str = 'requirements.txt'):
    """Записує пакети у файл requirements.txt.

    Args:
        packages: список словників з ключами 'name' та 'version'.
        filename: ім'я файлу для запису.
    """
    ignored_packages = {'pip', 'setuptools', 'wheel'}
    
    with open(filename, 'w', encoding='utf-8') as f:
        for pkg in packages:
            if pkg['name'].lower() not in ignored_packages:
                f.write(f"{pkg['name']}=={pkg['version']}\n")


def verify_requirements(filename: str = 'requirements.txt') -> bool:
    """Перевіряє, чи всі пакети з requirements.txt встановлені.

    Args:
        filename: шлях до файлу requirements.txt.

    Returns:
        True, якщо всі залежності задоволені.
    """
    if not os.path.exists(filename):
        print(f"Помилка: Файл {filename} не знайдено!")
        return False

    installed = {pkg['name'].lower(): pkg['version'] for pkg in get_installed_packages()}
    all_ok = True

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '==' in line:
                name, req_version = line.split('==', 1)
                name = name.strip().lower()
                req_version = req_version.strip()
                
                if name not in installed:
                    print(f"  Відсутній пакет: {name}")
                    all_ok = False
                elif installed[name] != req_version:
                    print(f"  Невідповідність версії для {name}: треба {req_version}, є {installed[name]}")
                    all_ok = False

    return all_ok


def main():
    packages = get_installed_packages()
    print(f"Знайдено {len(packages)} встановлених пакетів\n")

    for pkg in packages[:10]:
        print(f"  {pkg['name']}=={pkg['version']}")
    if len(packages) > 10:
        print(f"  ... та ще {len(packages) - 10}")

    generate_requirements(packages)
    print(f"\nФайл requirements.txt створено/оновлено")

    ok = verify_requirements()
    print(f"Перевірка залежностей: {'✓ Усе OK' if ok else '✗ Є розбіжності'}")


if __name__ == "__main__":
    main()
