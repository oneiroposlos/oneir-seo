import logging
from typing import Any

import pandas as pd
from clickhouse_connect import get_client as ch_client
from clickhouse_connect.driver.client import Client

from src.config import *

logger = logging.getLogger(__name__)


class BaseClickHouseConnection:
    client: Client

    def __init__(
            self,
            host: str = None,
            port: int = None,
            username: str = None,
            password: str = None
    ):
        self.host = host or CH_HOST
        self.port = port or int(CH_PORT)
        self.username = username or CH_USER
        self.password = password or CH_PASS
        self.client = ch_client(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
        )

    def __enter__(self):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.warning(f"Closing connection to ClickHouse...")
        self.client.close()

    @property
    def connection(self) -> Client:
        return self.client

    def query(self, query: str, **kwargs: Any) -> pd.DataFrame:
        formatted_query: str = query.format(**kwargs)
        try:
            return self.client.query_df(formatted_query)
        except Exception as e:
            logger.error(f"An exception occurred when querying:\n{formatted_query}", stacklevel=6)
            raise e


if __name__ == '__main__':
    conn = BaseClickHouseConnection()
    df_test = conn.query("SELECT * FROM system.columns limit 10")
    print(type(df_test))
    print(df_test)
