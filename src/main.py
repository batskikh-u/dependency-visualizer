
import sys

from src.config import read_config
from graph import build_graph, print_graph

FILES_NUMBER = 2
CONFIG_QUEUE = 1


def print_config(config):
    print("Параметры конфигурации:")
    for key, value in config.items():
        print(f"{key} = {value}")


def main():
    if len(sys.argv) > FILES_NUMBER:
        print("Ошибка: укажите не более одного файла")
        return

    file_name = "config.toml"
    if len(sys.argv) == FILES_NUMBER:
        file_name = sys.argv[CONFIG_QUEUE]

    try:
        config = read_config(file_name)
        graph = build_graph(config)
        print_graph(graph)
    except ValueError as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
