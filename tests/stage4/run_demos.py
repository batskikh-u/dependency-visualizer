
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = Path(__file__).resolve().parent
MAIN = ROOT / "src" / "main.py"

SCENARIOS = [
    ("Прямые обратные зависимости", "config_reverse_basic.toml"),
    ("Транзитивные зависимости", "config_reverse_chain.toml"),
    ("Нет обратных зависимостей", "config_reverse_empty.toml"),
    ("Циклические зависимости", "config_reverse_cycle.toml"),
    ("Фильтрация", "config_reverse_filter.toml"),
    ("Отсутствующий пакет", "config_reverse_missing.toml"),
]


def create_environment():
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONPATH"] = os.pathsep.join(
        [str(ROOT / "src"), str(ROOT), env.get("PYTHONPATH", "")]
    )
    return env


def run_scenario(config_name):
    config_path = CONFIG_DIR / config_name
    return subprocess.run(
        [sys.executable, str(MAIN), str(config_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=create_environment(),
    )


def check_result(config_name, result):
    if config_name == "config_reverse_missing.toml":
        return (
            result.returncode != 0
            and "Пакет не найден: J" in result.stdout
        )
    return result.returncode == 0


def print_result(title, result, success):
    print(f"\n{title}")
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")


def main():
    failed = False

    for title, config_name in SCENARIOS:
        result = run_scenario(config_name)
        success = check_result(config_name, result)
        print_result(title, result, success)
        failed = failed or not success

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
