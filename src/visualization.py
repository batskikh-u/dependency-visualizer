
import html
import json
import webbrowser
from pathlib import Path


def generate_mermaid(graph):
    packages = list(graph)
    for dependencies in graph.values():
        for dependency in dependencies:
            if dependency not in packages:
                packages.append(dependency)

    identifiers = {
        package: f"node_{index}"
        for index, package in enumerate(packages)
    }

    lines = ["graph TD"]

    for package in packages:
        label = json.dumps(package, ensure_ascii=False)
        lines.append(f"    {identifiers[package]}[{label}]")

    for package, dependencies in graph.items():
        for dependency in dependencies:
            lines.append(
                f"    {identifiers[package]} --> "
                f"{identifiers[dependency]}"
            )

    return "\n".join(lines)


def generate_html(mermaid_code):
    safe_code = html.escape(mermaid_code)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Граф зависимостей</title>
    <script type="module">
        import mermaid from
        "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 30px;
        }}
        .mermaid {{
            text-align: center;
        }}
    </style>
</head>
<body>
    <h2>Граф зависимостей</h2>
    <pre class="mermaid">
{safe_code}
    </pre>
</body>
</html>
"""


def save_mermaid(graph, directory, package_name):
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)

    mermaid_code = generate_mermaid(graph)
    file_path = path / f"{package_name}.mmd"

    file_path.write_text(mermaid_code, encoding="utf-8")
    return file_path


def save_html(graph, directory, package_name):
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)

    mermaid_code = generate_mermaid(graph)
    html_code = generate_html(mermaid_code)

    file_path = path / f"{package_name}.html"
    file_path.write_text(html_code, encoding="utf-8")
    return file_path


def show_graph(graph, package_name):
    directory = Path("output")
    mermaid_path = save_mermaid(
        graph, directory, package_name
    )
    html_path = save_html(
        graph, directory, package_name
    )

    print("\nMermaid-представление:")
    print(mermaid_path.read_text(encoding="utf-8"))

    webbrowser.open(html_path.resolve().as_uri())
    print(f"HTML-файл: {html_path}")


def print_ascii_tree(graph, root):
    print("\nASCII-дерево зависимостей:")
    print(root)

    for index, dependency in enumerate(graph.get(root, [])):
        is_last = index == len(graph[root]) - 1
        connector = "└── " if is_last else "├── "
        prefix = "    " if is_last else "│   "

        _print_branch(
            graph, dependency, connector, prefix, {root}
        )


def _print_branch(graph, package, connector, prefix, path):
    print(f"{connector}{package}")

    if package in path:
        print(f"{prefix}└── (цикл)")
        return

    next_path = path | {package}
    dependencies = graph.get(package, [])

    for index, dependency in enumerate(dependencies):
        is_last = index == len(dependencies) - 1
        next_connector = "└── " if is_last else "├── "
        next_prefix = prefix + (
            "    " if is_last else "│   "
        )

        _print_branch(
            graph,
            dependency,
            prefix + next_connector,
            next_prefix,
            next_path
        )
