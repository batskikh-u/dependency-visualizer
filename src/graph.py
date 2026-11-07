import re
from repository import get_dependencies, get_reverse_dependency_map

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

def process_reverse_queue(queue, index, graph, visited, reverse_map, config):
    if index >= len(queue):
        return
    package = queue[index]
    key = normalize_name(package)
    if key in visited:
        process_reverse_queue(
            queue, index + INDEX_GROW, graph, visited, reverse_map, config
        )
        return

    visited.add(key)
    graph.setdefault(package, [])

    for dependent in reverse_map.get(key, []):
        if not should_include(dependent, config["filter_substring"]):
            continue

        graph[package].append(dependent)
        queue.append(dependent)

    process_reverse_queue (
        queue, index + INDEX_GROW, graph, visited, reverse_map, config
    )

def build_reverse_graph(config):
    root = config["package_name"]
    reverse_map = get_reverse_dependency_map(config)

    normalized_map = {
        normalize_name(package): dependents
        for package, dependents in reverse_map.items()
    }

    normalized_root = normalize_name(root)

    if normalized_root not in normalized_map:
        raise ValueError(f"Пакет не найден: {root}")

    graph = {}
    visited = set()
    queue = [root]

    process_reverse_queue(
        queue, ZERO_MODE, graph, visited, normalized_map, config
    )

    return graph

def print_reverse_graph(graph):
    print("\nГраф обратных зависимостей:")
    if not graph:
        print("Граф пуст.")
        return

    for package, dependents in graph.items():
        print(f"{package}:")
        if dependents:
            for dependent in dependents:
                print(f"  -> {dependent}")
        else:
            print("  (нет обратных зависимостей)")