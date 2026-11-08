# Граф зависимостей пакетов

## Описание

Консольное приложение на Python для получения, построения и визуализации графов зависимостей Python-пакетов.

Приложение поддерживает получение информации из PyPI и работу с локальным тестовым репозиторием JSON.

## Реализованные возможности

### Этап 1. Работа с конфигурацией
- Чтение конфигурационных файлов TOML.
- Проверка наличия обязательных параметров.
- Проверка типов и корректности значений.
- Проверка формата версии пакета.
- Обработка ошибок чтения и разбора конфигурации.

### Этап 2. Получение зависимостей
- Получение информации о пакетах из PyPI.
- Работа с тестовым репозиторием JSON.
- Извлечение прямых зависимостей пакетов.

### Этап 3. Построение графа зависимостей
- Построение транзитивного графа зависимостей с использованием очереди BFS.
- Обработка зависимостей на нескольких уровнях.
- Исключение пакетов, содержащих заданную подстроку в имени.
- Обработка циклических зависимостей.
- Ограничение глубины обхода для PyPI.

### Этап 4. Обратные зависимости
- Построение графа обратных зависимостей.
- Поиск пакетов, которые зависят от заданного пакета.
- Обход обратного графа с использованием очереди.
- Фильтрация результатов.

### Этап 5. Визуализация графа
- Генерация графа в формате Mermaid.
- Создание HTML-представления графа.
- Открытие визуализации в браузере.
- Текстовое представление графа в виде ASCII-дерева.
- Подготовка конфигураций для сравнения с pipdeptree.

## Структура проекта

```text
vizualised/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── graph.py
│   ├── repository.py
│   └── visualization.py
├── tests/
│   ├── stage2/
│   ├── stage3/
│   ├── stage4/
│   └── stage5/
│       ├── config_requests.toml
│       ├── config_jinja2.toml
│       ├── config_werkzeug.toml
│       ├── config_rich.toml
│       └── run_demos.py
└── README.md
```

## Запуск приложения

Из корневой директории проекта:

```bash
python src/main.py
```

Для указания конфигурационного файла:

```bash
python src/main.py path/to/config.toml
```

## Тестовый режим

В тестовом режиме `test_repository_mode = true` приложение использует JSON-файл вместо URL репозитория.

Пример конфигурации:

```toml
package_name = "A"
repository = "tests/stage3/repository.json"
test_repository_mode = true
version = "1.0.0"
ascii_tree = true
filter_substring = ""
```

Пример тестового репозитория:

```json
{
  "A": ["B", "C"],
  "B": ["D"],
  "C": ["D", "E"],
  "D": ["F"],
  "E": [],
  "F": [],
  "G": ["H"],
  "H": ["G"],
  "I": []
}
```

## Демонстрация этапа 3

В директории `tests/stage3/` подготовлены конфигурации для пяти сценариев:

| Конфигурация | Проверяемый случай |
|---|---|
| `config_basic.toml` | Транзитивные и общие зависимости |
| `config_cycle.toml` | Циклические зависимости |
| `config_filter.toml` | Фильтрация по подстроке |
| `config_empty.toml` | Пакет без зависимостей |
| `config_missing.toml` | Отсутствующий пакет |

Запуск всех сценариев:

```bash
python tests/stage3/run_demos.py
```

## Демонстрация этапа 4

Для проверки обратных зависимостей используются конфигурации из `tests/stage4/`.

В конфигурации необходимо указать:

```toml
operation = "reverse_dependencies"
```

Обратные зависимости доступны в режиме тестового JSON-репозитория.

Запуск демонстраций:

```bash
python tests/stage4/run_demos.py
```

## Демонстрация этапа 5

В директории `tests/stage5/` находятся конфигурации для получения зависимостей из PyPI:

| Конфигурация | Пакет |
|---|---|
| `config_requests.toml` | requests |
| `config_jinja2.toml` | Jinja2 |
| `config_werkzeug.toml` | Werkzeug |
| `config_rich.toml` | rich |

Все конфигурации используют `test_repository_mode = false`.

Запуск отдельной конфигурации:

```bash
python src/main.py tests/stage5/config_requests.toml
```

```bash
python src/main.py tests/stage5/config_jinja2.toml
```

```bash
python src/main.py tests/stage5/config_werkzeug.toml
```

```bash
python src/main.py tests/stage5/config_rich.toml
```

Запуск всех демонстраций:

```bash
python tests/stage5/run_demos.py
```

## Пример работы: ASCII-визуализация графа зависимостей

Для демонстрации построения графа используется пакет `jsonschema`. У него достаточно большое количество прямых и транзитивных зависимостей, поэтому на этом примере можно увидеть не только непосредственные связи, но и несколько уровней вложенности.

### Пример ASCII-дерева

```text
jsonschema
├── attrs
├── jsonschema-specifications
│   └── referencing
│       ├── attrs
│       ├── rpds-py
│       └── typing-extensions
├── referencing
│   ├── attrs
│   ├── rpds-py
│   └── typing-extensions
├── rpds-py
├── fqdn
│   ├── cached-property
│   ├── myst-parser
│   │   ├── docutils
│   │   ├── jinja2
│   │   ├── markdown-it-py
│   │   ├── mdit-py-plugins
│   │   ├── pyyaml
│   │   ├── sphinx
│   │   │   ├── sphinxcontrib-applehelp
│   │   │   ├── sphinxcontrib-devhelp
│   │   │   ├── sphinxcontrib-htmlhelp
│   │   │   ├── sphinxcontrib-jsmath
│   │   │   ├── sphinxcontrib-qthelp
│   │   │   ├── sphinxcontrib-serializinghtml
│   │   │   ├── jinja2
│   │   │   ├── pygments
│   │   │   ├── docutils
│   │   │   ├── snowballstemmer
│   │   │   ├── babel
│   │   │   ├── alabaster
│   │   │   ├── imagesize
│   │   │   ├── requests
│   │   │   ├── packaging
│   │   │   └── defusedxml
│   │   ├── pre-commit
│   │   ├── linkify-it-py
│   │   ├── ipython
│   │   └── sphinx-book-theme
│   └── sphinx
│       ├── sphinxcontrib-applehelp
│       ├── sphinxcontrib-devhelp
│       ├── sphinxcontrib-htmlhelp
│       ├── jinja2
│       ├── pygments
│       ├── docutils
│       └── requests
├── idna
│   ├── ruff
│   ├── mypy
│   │   ├── typing-extensions
│   │   ├── mypy-extensions
│   │   ├── pathspec
│   │   ├── tomli
│   │   └── setuptools
│   ├── ty
│   ├── pytest
│   │   ├── colorama
│   │   ├── exceptiongroup
│   │   ├── iniconfig
│   │   ├── packaging
│   │   ├── pluggy
│   │   └── pygments
│   └── hypothesis
│       ├── sortedcontainers
│       ├── black
│       ├── click
│       ├── django
│       ├── numpy
│       ├── pandas
│       ├── pytest
│       │   └── (цикл)
│       ├── python-dateutil
│       ├── pytz
│       ├── rich
│       └── watchdog
├── isoduration
│   └── arrow
│       ├── python-dateutil
│       ├── backports-zoneinfo
│       ├── tzdata
│       └── simplejson
├── jsonpointer
├── rfc3339-validator
│   └── six
├── rfc3987
└── uri-template
    ├── types-pyyaml
    ├── mypy
    │   ├── typing-extensions
    │   ├── mypy-extensions
    │   └── pathspec
    └── flake8
        ├── mccabe
        ├── pycodestyle
        └── pyflakes
```

### Сравнение с pipdeptree

Для сравнения результатов можно использовать `pipdeptree` — инструмент экосистемы Python для просмотра дерева установленных зависимостей.

```powershell
python -m pip install pipdeptree
python -m pipdeptree --packages jsonschema
```

Для получения Mermaid-представления:

```powershell
python -m pipdeptree --packages jsonschema -o mermaid
```

При сравнении необходимо учитывать, что приложение получает сведения из метаданных репозитория пакетов, а `pipdeptree` по умолчанию анализирует установленное окружение Python.

Поэтому результаты могут отличаться. В частности, метаданные могут содержать условные и дополнительные зависимости, которые не используются в текущем окружении. Если приложение не учитывает условия `environment markers` и дополнительные группы зависимостей (`extras`), часть таких пакетов может попасть в его граф, хотя `pipdeptree` их не показывает.

Таким образом, различия в деревьях не обязательно означают ошибку обхода графа: они могут быть связаны с источником метаданных, установленными версиями пакетов и способом обработки дополнительных зависимостей.
В установленном окружении pipdeptree также показывает требуемые диапазоны версий и фактически установленные версии зависимостей.

## Сравнение с pipdeptree

Для сравнения результатов используется утилита pipdeptree, которая позволяет отображать зависимости установленных Python-пакетов в виде дерева и графа.

Установка:

```bash
python -m pip install pipdeptree
```

Получение дерева зависимостей:

```bash
python -m pipdeptree --packages requests
```

Получение графа в формате Mermaid:

```bash
python -m pipdeptree --packages requests -o mermaid
```

Получение графа в формате Graphviz:

```bash
python -m pipdeptree --packages requests -o graphviz
```

Для сохранения Mermaid-представления в файл:

```bash
python -m pipdeptree --packages requests -o mermaid > requests_pipdeptree.mmd
```

Для получения SVG-представления:

```bash
python -m pipdeptree --packages requests -o graphviz-svg > requests_pipdeptree.svg
```

Аналогичные команды можно выполнить для Jinja2, Werkzeug и Rich, заменив имя пакета.

### Объяснение возможных расхождений

Результаты построения графов могут отличаться по следующим причинам:

1. Приложение получает зависимости из метаданных PyPI, а pipdeptree по умолчанию анализирует пакеты, установленные в текущем Python-окружении.
2. Метаданные PyPI могут содержать зависимости с условиями установки (environment markers).
3. Некоторые зависимости активируются только при установке дополнительных возможностей пакета (extras).
4. Установленные версии зависимостей могут отличаться от диапазонов версий, указанных в метаданных.
5. При построении графа приложение может учитывать зависимости, которые не установлены в текущем окружении.

Поэтому различия между результатами не обязательно свидетельствуют об ошибке алгоритма. Для корректного сравнения необходимо учитывать источник данных, версию Python, установленные пакеты и условия установки зависимостей.

## Используемые технологии

- Python
- TOML
- JSON
- PyPI JSON API
- Mermaid
- HTML
- pipdeptree
