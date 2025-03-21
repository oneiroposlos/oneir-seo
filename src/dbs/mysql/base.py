import json
import logging
from typing import Any, Dict

import pandas as pd
import sqlalchemy as sa
from sqlalchemy.engine import Engine, Connection

from src.config import *

logger = logging.getLogger(__name__)


class BaseMySQLConnection:
    """
    Base class to connect to MySQL using SQLAlchemy
    """
    engine: Engine
    connection: Connection
    logger: logging.Logger

    connect_params: Dict[str, Any] = {}

    def __init__(self, *, host: str, port: int, username: str, password: str, database: str):
        """
        Initialize the MySQL connection
        """

        url = sa.engine.URL.create(
            drivername="mysql+pymysql",
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
            query=self.connect_params,
        )

        self.engine = sa.create_engine(
            url,
            pool_recycle=3600,  # Recycle connections every 1 hour (adjust based on your DB's wait_timeout)
            pool_pre_ping=True,  # Test connections for validity before use
            echo=False
        )
        self.connection = self.engine.connect()
        logger.info(f"Connected to MySQL: {username}@{host}:{port}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        logger.warning(f"Closing connection to MySQL...")

    def query(self, query: str, **kwargs: Any) -> pd.DataFrame:
        """
        Run a query on the MySQL database
        """
        formatted_query = query.format(**kwargs)
        try:
            return pd.read_sql_query(sql=formatted_query, con=self.connection)
        except Exception as e:
            logger.error(f"An exception occurred when querying:\n{formatted_query}", stacklevel=6)
            raise

    def push_df(
            self,
            df: pd.DataFrame,
            table_name: str,
            if_exists: str = 'append',
            key_columns: list = None
    ) -> None:
        """
        Push a pandas DataFrame to a MySQL table. Only specific columns are pushed, and check for update if a key exists.
        """
        try:
            selected_columns = df.columns if key_columns is None else key_columns
            df_inserts = df[selected_columns]
            logger.info(f"Pushing {len(df_inserts)} users to table '{table_name}' with columns: {selected_columns}")
            df_inserts.to_sql(name=table_name, con=self.engine, if_exists=if_exists, chunksize=1000, index=False)
        except Exception as e:
            self.logger.error(f"An exception occurred when pushing DataFrame to table '{table_name}': {e}",
                              stacklevel=6)
            self.connection.rollback()
            pass

    def execute(self, query: str, **kwargs: Any) -> None:
        """
        Execute a query on the MySQL database
        """
        formatted_query = query.format(**kwargs)
        try:
            self.connection.execute(formatted_query)
        except Exception as e:
            logger.error(f"An exception occurred when executing:\n{formatted_query}", stacklevel=6)
            raise

    def insert_or_update(self, df: pd.DataFrame, table_name: str, key_columns: list) -> None:
        """
        Insert or update rows from a DataFrame into the SQL table.
        """
        primary_key = 'user_id'
        try:
            # Use SQLAlchemy's metadata to get the table definition
            metadata = sa.MetaData()
            table = sa.Table(table_name, metadata, autoload_with=self.engine)
            cols = df.columns if key_columns is None else key_columns
            df = df[cols]
            for _, row in df.iterrows():
                insert_statement = table.insert().values(**row.to_dict()).on_duplicate_key_update(
                    **{col: row[col] for col in df.columns if col != primary_key}
                )
                self.connection.execute(insert_statement)
        except Exception as e:
            logger.error(f"An exception occurred during insert or update: {e}", stacklevel=6)
            raise


if __name__ == '__main__':
    mood_conn = BaseMySQLConnection(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        username=MYSQL_USER,
        password=MYSQL_PASS,
        database=MYSQL_DB
    )

    data = pd.DataFrame(data=[{
        'user_id': '4178-8f0a-11ef-b71d-0615310044c3',
        'user_long_term': json.dumps([1.0, 0.75, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5]),
        'user_short_term': json.dumps([1.0, 0.75, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5])
    }]
        , columns=['user_id', 'user_long_term', 'user_short_term'])
    print(data.head())
    mood_conn.push_df(df=data, table_name='user_profiles', key_columns=['user_id', 'user_long_term', 'user_short_term'])
    # data = mood_conn.query('describe user_profiles')
    # print(data)
