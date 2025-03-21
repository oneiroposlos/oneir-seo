import logging
import re
from datetime import datetime
from urllib.parse import urlparse
from pytz import timezone
from src import config as cf

logger = logging.getLogger(__name__)


def url2domain(url: str):
    domain = "other.com"
    try:
        domain = urlparse(url).netloc.replace('www.', '')
    except Exception as e:
        logger.error(f'[GET_DOMAIN]: {e}, {url}')
    return domain


def remove_www(url: str):
    path = ''
    try:
        pattern = re.compile(r"https?://(www\.)?")
        path = pattern.sub('', url).strip().strip('/')
    except Exception as e:
        logger.error(f'[GET_PATH]: {e}, {url}')
    return path


def get_current_time():
    return datetime.now(timezone(cf.DB_TIMEZONE))


def get_timestamp():
    return datetime.now(timezone(cf.DB_TIMEZONE))


if __name__ == '__main__':
    print(remove_www('http://www.facebook.com.vn'))
    print(remove_www('http://www.test.facebook.com'))
    print(remove_www('http://www.shopee.vn/'))
    print(remove_www('http://www.shopee.vn/?...'))
