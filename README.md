## Описание

Этот скрипт предназначен для парсинга различных данных с сайта [peps.python.org](https://peps.python.org/). Скрипт поддерживает несколько режимов работы, каждый из которых предоставляет определённый функционал:

- **whats-new**: сбор информации о новых возможностях в последних версиях Python.
- **latest-versions**: получение информации о последних версиях Python и их статусах.
- **download**: загрузка архива с последней версией документации Python.
- **pep**: сбор статистики по PEP (Python Enhancement Proposals).

## Установка

1. Убедитесь, что у вас установлен Python 3.7 или новее.
2. Установите виртуальное окружение:
``` sh
python -m venv venv
source venv/bin/activate  # Для Windows используйте venv\Scripts\activate
```
3. Установите зависимости:
``` sh
pip install -r requirements.txt
```

## Использование

Скрипт поддерживает следующие аргументы командной строки:

- **mode**: обязательный параметр, определяющий режим работы скрипта. Допустимые значения: `whats-new`, `latest-versions`, `download`, `pep`.
- **-c, --clear-cache**: опциональный флаг для очистки кэша сессии.
- **-o, --output**: опциональный параметр для выбора формата вывода. Возможные значения: `pretty` (красиво оформленный вывод в консоль), `file` (сохранение результатов в CSV файл).

Примеры запуска:

``` sh
python main.py whats-new -o pretty
python main.py latest-versions -o file
python main.py download -c
python main.py pep
```

Результаты выполнения скрипта могут быть выведены в консоль в виде таблицы или сохранены в CSV файл, в зависимости от выбранных опций.

Скрипт использует логирование для отслеживания выполнения операций и ошибок. Логи записываются в файл parse.log в директории logs.
