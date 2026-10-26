import sys
from config import read_config
from repository import get_direct_dependencies

FILES_NUMBER = 2
CONFIG_QUEUE = 1

def print_config(config):
    print("Параметры конфигурации:")
    for key, value in config.items():
        print(f"{key} = {value}")

def print_dependencies(package_name, dependencies):
    print(f"\nПрямые зависимости пакета {package_name}: ")
    if not dependencies:
        print("Зависимости не найдены")
        return
    for dependency in dependencies:
        print(f"- {dependency}")

def main():
    if len(sys.argv) > FILES_NUMBER:
        print("Ошибка: укажите не более одного файла")
        return

    file_name = "config_real.toml"
    if len(sys.argv) == FILES_NUMBER:
        file_name = sys.argv[CONFIG_QUEUE]

    try:
        config = read_config(file_name)
        dependencies = get_direct_dependencies(config)
        print_dependencies(config["package_name"], dependencies)
    except ValueError as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()