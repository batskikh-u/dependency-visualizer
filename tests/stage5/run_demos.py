import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = Path(__file__).resolve().parent
MAIN_FILE = ROOT_DIR / "src" / "main.py"


def main():
    config_files = sorted(CONFIG_DIR.glob("config_*.toml"))

    if not config_files:
        print("Конфигурационные файлы не найдены.")
        return

    print(f"Найдено конфигураций: {len(config_files)}")

    for config_file in config_files:
        print(f"\n{'=' * 50}")
        print(f"Запуск: {config_file.name}")
        print(f"{'=' * 50}")

        result = subprocess.run(
            [
                sys.executable,
                str(MAIN_FILE),
                str(config_file)
            ],
            cwd=ROOT_DIR
        )

        if result.returncode == 0:
            print(f"\nЗавершено: {config_file.name}")
        else:
            print(f"\nОшибка при запуске: {config_file.name}")


if __name__ == "__main__":
    main()