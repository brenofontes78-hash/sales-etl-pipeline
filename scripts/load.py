import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
import logging
load_dotenv()


def load_data(data):

    host = os.getenv("DB_HOST")
    porta = os.getenv("DB_PORT")
    banco = os.getenv("DB_NAME")
    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASSWORD")

    logging.info("Conectando ao PostgreSQL...")
    try:

        engine = create_engine(
            f"postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{banco}"
        )

        data.to_sql(
            name="dados_vendas",
            con=engine,
            if_exists="replace",
            index=False
        )

        print("Dados carregados com sucesso.")

    except Exception as e:

        print(f"Erro ao carregar os dados: {e}")