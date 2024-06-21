import argparse
import logging
from logging.handlers import RotatingFileHandler
from constants import BASE_DIR, DATETIME_FORMAT, LOG_FORMAT


def configure_argument_parser(available_methods):
    """
    Конфигурирует парсер аргументов командной строки.

    Args:
        available_methods (list): Список доступных режимов работы парсера.

    Returns:
        argparse.ArgumentParser: Настроенный парсер аргументов.
    """
    parser = argparse.ArgumentParser(description='Парсер документации Python')
    parser.add_argument(
        'mode',
        choices=available_methods,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=('pretty', 'file'),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging():
    """
    Настраивает логирование с использованием ротации файлов.

    Логи будут сохраняться в директорию 'logs'.
    """
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'parse.log'
    rotating_handler = RotatingFileHandler(
        log_file,
        maxBytes=10**6,
        backupCount=5
    )
    logger = logging.basicConfig(
        datefmt=DATETIME_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
