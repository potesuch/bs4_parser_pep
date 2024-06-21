import logging
from requests import RequestException
from exceptions import ParserFindTagException


def get_response(session, url):
    """
    Выполняет GET запрос к указанному URL.

    makefile

    Args:
        session (requests_cache.CachedSession): Сессия с кешированием запросов.
        url (str): URL для запроса.

    Returns:
        requests.Response: Ответ на запрос.
    """
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы: {url}',
            exc_info=True
        )


def find_tag(soup, tag, attrs=None):
    """
    Находит тег в BeautifulSoup объекте по указанным атрибутам.

    vbnet

    Args:
        soup (BeautifulSoup): BeautifulSoup объект,
        представляющий HTML страницу.
        tag (str): Название тега для поиска.
        attrs (dict, optional): Атрибуты тега для поиска.

    Returns:
        bs4.element.Tag: Найденный тег.

    Raises:
        ParserFindTagException: Если тег не найден.
    """
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag
