import os
import subprocess
import sys
from pathlib import Path

PARENTS_NUM = 2

ROOT = Path(__file__).resolve().parents[PARENTS_NUM]
CONFIG_DIR = Path(__file__).resolve().parent
MAIN = ROOT / "src" / "main.py"

SCENARIOS = [
    ("Транзитивные зависимости", "config_basic.toml"),
    ("Циклические зависимости", "config_cycle.toml"),
    ("Фильтрация", "config_filter.toml"),
    ("Нет зависимостей", "config_empty.toml"),
    ("Пакет не найден", "config_missing.toml"),
]


def main():
    failed = False

    for title, config_name in SCENARIOS:
        config_path = CONFIG_DIR / config_name
        print(f"\n=== {title} ===")

        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        env["PYTHONPATH"] = os.pathsep.join(
            [str(ROOT / "src"), str(ROOT), env.get("PYTHONPATH", "")]
        )

        result = subprocess.run(
            [sys.executable, str(MAIN), str(config_path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )

        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="")

        if result.returncode != 0:
            failed = True
            print(f"Сценарий завершился с ошибкой: {title}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
