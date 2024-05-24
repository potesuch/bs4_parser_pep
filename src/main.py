import re
import requests_cache
import logging
from requests import RequestException
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from tqdm import tqdm
from constants import BASE_DIR, MAIN_DOC_URL, PEP_URL, EXPECTED_STATUS
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import get_response, find_tag


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    soup = BeautifulSoup(response.text, 'lxml')
    main_div = find_tag(soup, 'section', {'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', 
                           {'class': 'toctree-wrapper compound'})
    sections_by_python = div_with_ul.find_all('li', class_='toctree-l1')
    results = []
    results.append(('Ссылка на статью', 'Заголовок', 'Редактор, Автор'))
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        response = get_response(session, version_link)
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in tqdm(ul_tags):
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    results = []
    results.append(('Ссылка на документацию', 'Версия', 'Статус'))
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a in tqdm(a_tags):
        link = a['href']
        text_match = re.search(pattern, a.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a.text, ''
        results.append((link, version, status))
    return results


def download(session):
    download_url = urljoin(MAIN_DOC_URL, 'download.html')
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    response = get_response(session, download_url)
    soup = BeautifulSoup(response.text, 'lxml')
    table_tag = find_tag(soup, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(download_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    archive_path = downloads_dir / filename
    response = get_response(session, archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив с результатами был сохранен: {archive_path}')


def pep(session):
    response = get_response(session, PEP_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    section_tag = find_tag(soup, 'section', {'id': 'numerical-index'})
    table_tag = find_tag(section_tag, 'table', {'class': 'pep-zero-table docutils align-default'})
    tbody_tag = find_tag(table_tag, 'tbody')
    tr_tags = tbody_tag.find_all('tr')
    peps = []
    for tr in tr_tags:
        abbr_tag = find_tag(tr, 'abbr')
        pep_abbr = abbr_tag.text
        a_tag = find_tag(tr, 'a')
        pep_number = a_tag.text
        pep_link = urljoin(PEP_URL, a_tag['href'])
        peps.append((pep_abbr, pep_number, pep_link))
    pep_count = 0
    status_count = {
        'Accepted': 0,
        'Active': 0,
        'Deferred': 0,
        'Draft': 0,
        'Final': 0,
        'Provisional': 0,
        'Rejected': 0,
        'Superseded': 0,
        'Withdrawn': 0,
        'April Fool!': 0
    }
    for pep in tqdm(peps):
        pep_count += 1
        preview_status = pep[0][1:]
        response = get_response(session, pep[2])
        soup = BeautifulSoup(response.text, 'lxml')
        dl_tag = find_tag(soup, 'dl', {'class': 'rfc2822 field-list simple'})
        dt_tags = dl_tag.find_all('dt')
        for dt in dt_tags:
            if dt.text == 'Status:':
                dd = dt.find_next_sibling('dd')
                status = dd.string
        if preview_status and status not in EXPECTED_STATUS[preview_status]:
            logging.info('Несовпадающие статусы: '
                         f'{pep[2]}'
                         'Статус в карточке:'
                         f'{status}')
        status_count[status] += 1
        results = []
        results.append(('Статус', 'Количество'))
        for k, v in status_count.items():
            results.append((k, v))
        results.append(('Total', pep_count))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
