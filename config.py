import tomllib
import re
from pathlib import Path
from urllib.parse import urlparse


def read_toml(file_name):
    path = Path(file_name)
    if not path.is_file():
        raise ValueError(f"Файл не найден: {file_name}")

    try:
        with path.open("rb") as file:
            return tomllib.load(file)
    except tomllib.TOMLDecodeError as error:
        raise ValueError(f"Ошибка TOML: {error}") from error
    except OSError as error:
        raise ValueError(f"Ошибка чтения файла: {error}") from error


def check_required(config):
    keys = [
        "package_name", "repository",
        "test_repository_mode", "version",
        "ascii_tree", "filter_substring"
    ]
    errors = []
    for key in keys:
        if key not in config:
            errors.append(f"Отсутствует параметр: {key}")
    return errors


def check_package_name(config):
    value = config.get("package_name")
    if not isinstance(value, str) or not value.strip():
        return ["package_name должен быть непустой строкой"]
    return []


def check_repository_type(config):
    value = config.get("repository")
    if not isinstance(value, str) or not value.strip():
        return ["repository должен быть непустой строкой"]
    return []


def check_boolean(config, key):
    if type(config.get(key)) is not bool:
        return [f"{key} должен быть true или false"]
    return []


def check_version(config):
    value = config.get("version")
    if not isinstance(value, str):
        return ["version должна быть строкой"]
    if not re.fullmatch(r"[0-9]+(\.[0-9]+)*", value):
        return ["Неверный формат version, например 1.2.0"]
    return []


def check_filter(config):
    if not isinstance(config.get("filter_substring"), str):
        return ["filter_substring должен быть строкой"]
    return []


def check_repository(config):
    repository = config.get("repository")
    test_mode = config.get("test_repository_mode")

    if not isinstance(repository, str) or not repository.strip():
        return []
    if type(test_mode) is not bool:
        return []

    if test_mode:
        if not Path(repository).is_file():
            return [f"Тестовый файл не найден: {repository}"]
    else:
        url = urlparse(repository)
        if url.scheme not in ("http", "https") or not url.hostname:
            return ["Укажите корректный HTTP/HTTPS URL"]
    return []


def validate_config(config):
    errors = check_required(config)
    errors += check_package_name(config)
    errors += check_repository_type(config)
    errors += check_boolean(config, "test_repository_mode")
    errors += check_version(config)
    errors += check_boolean(config, "ascii_tree")
    errors += check_filter(config)
    errors += check_repository(config)

    if errors:
        raise ValueError("\n".join(errors))


def read_config(file_name):
    config = read_toml(file_name)
    validate_config(config)
    return config
