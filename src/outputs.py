import csv
import logging
from datetime import datetime
from prettytable import PrettyTable
from constants import BASE_DIR, DATETIME_FORMAT


def control_output(results, cli_args):
    if cli_args.output == 'pretty':
        pretty_output(results)
    elif cli_args.output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    if results is not None:
        for row in results:
            print(*row)


def pretty_output(results):
    table = PrettyTable()
    table.field_names = (results[0])
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / 'output'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранен: {file_path}')
