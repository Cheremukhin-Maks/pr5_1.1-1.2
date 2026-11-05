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
    # TODO: Розпарсити JSON-відповідь та повернути список пакетів
    if result.returncode == 0 and result.stdout:
        return json.loads(result.stdout)
    return []


def generate_requirements(packages: list[dict], filename: str = 'requirements.txt'):
    """Записує пакети у файл requirements.txt.

    Args:
        packages: список словників з ключами 'name' та 'version'.
        filename: ім'я файлу для запису.
    """
    # TODO: Відфільтрувати системні пакети (pip, setuptools, wheel)
    system_packages = {'pip', 'setuptools', 'wheel'}
    filtered_packages = [
        pkg for pkg in packages 
        if pkg['name'].lower() not in system_packages
    ]

    # TODO: Записати у файл у форматі package==version
    with open(filename, 'w', encoding='utf-8') as f:
        for pkg in filtered_packages:
            f.write(f"{pkg['name']}=={pkg['version']}\n")


def verify_requirements(filename: str = 'requirements.txt') -> bool:
    """Перевіряє, чи всі пакети з requirements.txt встановлені.

    Args:
        filename: шлях до файлу requirements.txt.

    Returns:
        True, якщо всі залежності задоволені.
    """
    # TODO: Прочитати файл, для кожного пакета перевірити наявність
    if not os.path.exists(filename):
        print(f"Помилка: Файл '{filename}' відсутній!")
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
                    print(f"  [✗] Відсутній пакет: {name}")
                    all_ok = False
                elif installed[name] != req_version:
                    print(f"  [✗] Невідповідність версії {name}: треба {req_version}, встановлено {installed[name]}")
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
    print(f"\nФайл requirements.txt створено")

    ok = verify_requirements()
    print(f"Перевірка залежностей: {'✓ Усе OK' if ok else '✗ Є розбіжності'}")


if __name__ == "__main__":
    main()