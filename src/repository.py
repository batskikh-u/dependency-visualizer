
import json
import re
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen


def read_test_repository(file_name):
    path = Path(file_name)
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Ошибка тестового репозитория: {error}") from error
    if not isinstance(data, dict):
        raise ValueError("Описание репозитория должно быть JSON-объектом")
    return data


def get_test_dependencies(repository, package_name):
    if package_name not in repository:
        raise ValueError(f"Пакет не найден: {package_name}")
    dependencies = repository[package_name]
    if not isinstance(dependencies, list):
        raise ValueError("Список зависимостей должен быть массивом")
    if not all(isinstance(item, str) for item in dependencies):
        raise ValueError("Названия зависимостей должны быть строками")
    return dependencies


def fetch_package_metadata(repository, package_name, version):
    package = quote(package_name, safe="")
    release = quote(version, safe="")
    url = f"{repository.rstrip('/')}/{package}/{release}/json"
    try:
        with urlopen(url, timeout=10) as response:
            return json.load(response)
    except HTTPError as error:
        raise ValueError(f"Ошибка HTTP: {error.code}, {url}") from error
    except URLError as error:
        raise ValueError(f"Не удалось подключиться: {error.reason}") from error
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError("Сервер вернул некорректный JSON") from error


def extract_dependencies(metadata):
    info = metadata.get("info")
    if not isinstance(info, dict):
        raise ValueError("В ответе отсутствует информация о пакете")
    requirements = info.get("requires_dist") or []
    if not isinstance(requirements, list):
        raise ValueError("Некорректное поле requires_dist")
    return requirements


def normalize_dependency(requirement):
    match = re.match(r"\s*([A-Za-z0-9][A-Za-z0-9._-]*)", requirement)
    if not match:
        raise ValueError(f"Не удалось разобрать зависимость: {requirement}")
    return match.group(1)


def get_direct_dependencies(config):
    if config["test_repository_mode"]:
        repository = read_test_repository(config["repository"])
        return get_test_dependencies(repository, config["package_name"])
    metadata = fetch_package_metadata(
        config["repository"],
        config["package_name"],
        config["version"],
    )
    return extract_dependencies(metadata)
