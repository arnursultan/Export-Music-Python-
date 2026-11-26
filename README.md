# Yandex Music to Apple Music

Утилита для переноса понравившихся треков из Яндекс Музыки в медиатеку Apple Music.

## Возможности

- Экспорт понравившихся треков из Яндекс Музыки.
- Поиск композиций в каталоге Apple Music.
- Автоматическое добавление найденных треков в медиатеку.
- Пропуск композиций, которые не удалось найти.
- Сохранение прогресса между запусками.
- Возобновление переноса после ошибки или остановки.
- Формирование CSV-отчёта.

## Требования

- Python 3.11+
- Git
- Аккаунт Яндекс Музыки
- Активная подписка Apple Music
- Интернет-соединение

Поддерживаемые ОС: macOS, Windows, Linux.

## Структура проекта

```text
MusicTransfer/
├── applemusic-agent-skill/
│   └── scripts/
│       └── applemusic_library.py
├── .venv/
├── export_yandex.py
├── transfer.py
├── yandex_liked.csv
├── transfer_state.json
├── transfer_report.csv
└── README.md
```

| Файл | Назначение |
|---|---|
| `export_yandex.py` | Экспорт треков из Яндекс Музыки |
| `transfer.py` | Поиск и добавление треков в Apple Music |
| `yandex_liked.csv` | Исходный список композиций |
| `transfer_state.json` | Состояние переноса |
| `transfer_report.csv` | Результаты переноса |

## 1. Установка

### macOS

Откройте Terminal.

Создайте рабочую директорию:

```bash
mkdir -p ~/MusicTransfer
cd ~/MusicTransfer
```

Клонируйте репозиторий инструмента Apple Music:

```bash
git clone https://github.com/jamiezigelbaum/applemusic-agent-skill.git
```

Создайте виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установите зависимости:

```bash
python -m pip install --upgrade pip
python -m pip install yandex-music
```

Поместите `export_yandex.py` и `transfer.py` в корень `MusicTransfer`.

### Windows

Установите Python с официального сайта:

https://www.python.org/downloads/windows/

При установке включите `Add Python to PATH`.

Откройте PowerShell:

```powershell
mkdir $HOME\MusicTransfer
cd $HOME\MusicTransfer
```

Клонируйте репозиторий:

```powershell
git clone https://github.com/jamiezigelbaum/applemusic-agent-skill.git
```

Создайте и активируйте виртуальное окружение:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Установите зависимости:

```powershell
python -m pip install --upgrade pip
python -m pip install yandex-music
```

### Linux

Для Ubuntu и Debian установите необходимые пакеты:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

Создайте рабочую директорию:

```bash
mkdir -p ~/MusicTransfer
cd ~/MusicTransfer
```

Клонируйте репозиторий:

```bash
git clone https://github.com/jamiezigelbaum/applemusic-agent-skill.git
```

Создайте виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установите зависимости:

```bash
python -m pip install --upgrade pip
python -m pip install yandex-music
```

## 2. Экспорт треков из Яндекс Музыки

Для экспорта потребуется токен Яндекс Музыки.

Получите токен через используемый в проекте способ авторизации и передайте его скрипту `export_yandex.py`.

Запустите:

**macOS / Linux**

```bash
python export_yandex.py
```

**Windows**

```powershell
python export_yandex.py
```

После успешного выполнения в корне проекта появится:

```text
yandex_liked.csv
```

Файл содержит название композиции, исполнителя, альбом и идентификатор трека.

Если CSV уже подготовлен, повторный экспорт не требуется.

## 3. Настройка Apple Music

Для доступа к медиатеке используется Apple Music API.

Первоначальное получение токенов выполняется на macOS через Safari. Для Windows и Linux можно использовать уже полученную пару токенов.

### Получение токенов на macOS

1. Откройте Safari.
2. Перейдите на https://music.apple.com.
3. Авторизуйтесь в аккаунте Apple Music.
4. Разрешите Terminal управлять Safari, если macOS запросит доступ.
5. Откройте Terminal.

Выполните:

```bash
cd ~/MusicTransfer/applemusic-agent-skill
python3 scripts/applemusic_library.py harvest
```

Проверьте подключение:

```bash
python3 scripts/applemusic_library.py doctor
```

Ожидаемый результат:

```text
PASS tokens_present
PASS token_expiry
PASS api_reachable
PASS library_scope

doctor: all checks passed
```

Токены сохраняются в:

```text
~/.config/applemusic-agent/tokens.json
```

### Использование на Windows и Linux

Перенесите `tokens.json` с macOS на целевую систему по защищённому каналу.

Расположение файла:

**Windows**

```text
%USERPROFILE%\.config\applemusic-agent\tokens.json
```

**Linux**

```text
~/.config/applemusic-agent/tokens.json
```

На Linux ограничьте права доступа:

```bash
chmod 600 ~/.config/applemusic-agent/tokens.json
```

После переноса проверьте подключение:

**Windows**

```powershell
python applemusic-agent-skill/scripts/applemusic_library.py doctor
```

**Linux**

```bash
python applemusic-agent-skill/scripts/applemusic_library.py doctor
```

Если проверка не проходит, перенос запускать не нужно.

## 4. Запуск переноса

Перед запуском убедитесь, что:

- `yandex_liked.csv` находится в корне проекта.
- Apple Music API проходит проверку `doctor`.
- Виртуальное окружение активировано.
- В каталоге проекта присутствует `transfer.py`.

Запуск:

```bash
python transfer.py
```

Скрипт последовательно обрабатывает исходный список:

1. Читает композицию из CSV.
2. Выполняет поиск в Apple Music.
3. Сравнивает название и исполнителя.
4. Выбирает наиболее подходящее совпадение.
5. Добавляет найденные композиции в медиатеку.
6. Сохраняет прогресс и отчёт.

Добавление выполняется пакетами по 20 треков.

## 5. Возобновление переноса

Состояние сохраняется в:

```text
transfer_state.json
```

Если процесс остановился, повторно запустите:

```bash
python transfer.py
```

Уже обработанные записи будут пропущены.

**Не удаляйте `transfer_state.json` во время переноса.**

При тайм-ауте добавления сначала проверьте Apple Music. Запрос мог выполниться на стороне сервиса, даже если клиент не получил ответ.

Не запускайте несколько экземпляров `transfer.py` одновременно.

## 6. Результаты

После завершения обработки формируется:

```text
transfer_report.csv
```

В отчёте используются следующие статусы:

| Статус | Описание |
|---|---|
| `matched` | Найдено совпадение |
| `already_added` | Трек уже добавлен |
| `not_found` | Композиция отсутствует в результатах поиска |
| `error` | Ошибка обработки |

Отчёт можно открыть в Excel, Numbers или LibreOffice Calc.

Перенесённые композиции доступны в Apple Music:

`Медиатека → Песни`

## 7. Конфигурация

Основные параметры находятся в начале `transfer.py`:

```python
BATCH_SIZE = 20
MIN_SCORE = 0.76
SEARCH_TIMEOUT = 90
ADD_TIMEOUT = 300
```

| Параметр | Назначение |
|---|---|
| `BATCH_SIZE` | Количество треков в одной пачке |
| `MIN_SCORE` | Минимальный общий коэффициент совпадения |
| `SEARCH_TIMEOUT` | Тайм-аут поиска в секундах |
| `ADD_TIMEOUT` | Тайм-аут добавления в секундах |

Изменять параметры рекомендуется только при необходимости.

## 8. Типовые ошибки

### `401 Unauthorized`

Проверьте актуальность токенов Apple Music и авторизацию аккаунта.

При необходимости повторите `harvest` на macOS.

### `403 Forbidden`

Проверьте доступ к медиатеке и активность подписки Apple Music.

### `429 Too Many Requests`

Apple Music ограничил частоту запросов. Сделайте паузу перед следующим запуском.

### `Timeout`

Запрос не получил ответ за установленное время.

Проверьте результат операции в Apple Music перед повторной отправкой пачки.

### `CERTIFICATE_VERIFY_FAILED`

Обновите сертификаты Python:

```bash
python -m pip install --upgrade certifi
```

Для macOS / Linux:

```bash
export SSL_CERT_FILE=$(python -m certifi)
export REQUESTS_CA_BUNDLE=$(python -m certifi)
```

Для PowerShell:

```powershell
$env:SSL_CERT_FILE = python -m certifi
$env:REQUESTS_CA_BUNDLE = python -m certifi
```

## 9. Безопасность

Файлы с токенами и пользовательскими данными не должны попадать в публичный репозиторий.

Рекомендуемый `.gitignore`:

```gitignore
venv/
.venv/
__pycache__/
*.py[cod]
.DS_Store
.idea/workspace.xml
.idea

.env
tokens.json

yandex_liked.csv
transfer_state.json
transfer_report.csv
```

Не публикуйте `tokens.json` и не передавайте его третьим лицам.

## 10. Ограничения

- Для добавления треков требуется активная подписка Apple Music.
- Не все композиции из Яндекс Музыки доступны в Apple Music.
- Ремиксы, ускоренные и замедленные версии могут отсутствовать в каталоге.
- Автоматическое сопоставление не гарантирует идентичность всех версий треков.
- Токены Apple Music имеют ограниченный срок действия и требуют обновления.
- Перенос не копирует историю прослушиваний и отметки «Нравится» как избранное Apple Music.

---

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.