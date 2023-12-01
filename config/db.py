import psycopg2
from config.settings import Settings
settings = Settings()

class Database:
    def __init__(self):
        connection_params = settings.connection_params
        self.connection = psycopg2.connect(**connection_params)

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
        
    def execute(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
        return self.connection.commit()
