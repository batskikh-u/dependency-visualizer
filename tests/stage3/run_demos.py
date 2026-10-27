import os
import subprocess
import sys
from pathlib import Path

PARENTS_NUM = 2

ROOT = Path(__file__).resolve().parents[PARENTS_NUM]
CONFIG_DIR = Path(__file__).resolve().parent

SCENARIOS = [
    ("Транзитивные зависимости", "config_basic.toml"),
    ("Циклические зависимости", "config_cycle.toml"),
    ("Фильтрация", "config_filter.toml"),
    ("Нет зависимостей", "config_empty.toml"),
    ("Пакет не найден", "config_missing.toml"),
]


def main():

    for title, config_name in SCENARIOS:
        config_path = CONFIG_DIR / config_name
        print(title)

        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"

        result = subprocess.run(
            [sys.executable, str(ROOT / "main.py"), str(config_path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="")


if __name__ == "__main__":
    main()
