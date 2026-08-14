import logging
import time

from extract import extract_data
from transform import transform_data
from load import load_data


logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


def main():

    inicio = time.perf_counter()

    logging.info("=" * 50)
    logging.info("INICIANDO PIPELINE DE VENDAS")
    logging.info("=" * 50)

    try:

        logging.info("Iniciando etapa de extração.")
        data = extract_data()
        logging.info(f"Arquivo lido com sucesso. Registros encontrados: {len(data)}")
        logging.info("Etapa de extração concluída com sucesso.")

        logging.info("Iniciando etapa de transformação.")
        data = transform_data(data)
        logging.info("Etapa de transformação concluída com sucesso.")

        logging.info("Iniciando etapa de carregamento.")
        load_data(data)
        logging.info("Etapa de carregamento concluída com sucesso.")

        logging.info("=" * 50)
        logging.info("PIPELINE FINALIZADO COM SUCESSO")
        logging.info("=" * 50)

    except Exception:

        logging.exception("Falha durante a execução do pipeline.")
        raise

    finally:

        fim = time.perf_counter()
        logging.info(f"Tempo total de execução: {fim - inicio:.2f} segundos")


if __name__ == "__main__":
    main()