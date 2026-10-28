import re
from src.repository import get_dependencies

INDEX_GROW = 1
ZERO_MODE = 0
MAX_RECURSION_DEPTH = 3

def normalize_name(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def should_include(name, substring):
    return not substring or substring.lower() not in name.lower()


def process_queue(queue, index, graph, visited, config, depth=ZERO_MODE):
    if index >= len(queue):
        return

    if not config["test_repository_mode"] and depth >= MAX_RECURSION_DEPTH:
        return

    package, version = queue[index]
    key = normalize_name(package)

    if key in visited:
        process_queue(
            queue, index + INDEX_GROW, graph, visited, config, depth
        )
        return

    visited.add(key)
    graph.setdefault(package, [])
    dependencies = get_dependencies(config, package, version)

    for dependency in dependencies:
        if not should_include(dependency, config["filter_substring"]):
            continue
        graph[package].append(dependency)
        queue.append((dependency, None))

    process_queue(
        queue, index + INDEX_GROW, graph, visited,
        config, depth + INDEX_GROW
    )


def build_graph(config):
    root = config["package_name"]
    version = config["version"]
    graph = {}
    visited = set()
    queue = [(root, version)]
    process_queue(queue, ZERO_MODE, graph, visited, config)
    return graph


def print_graph(graph):
    print("\nГраф зависимостей:")
    if not graph:
        print("Граф пуст.")
        return
    for package, dependencies in graph.items():
        print(f"{package}:")
        if dependencies:
            for dependency in dependencies:
                print(f"  -> {dependency}")
        else:
            print("  (нет зависимостей)")
