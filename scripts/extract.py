from pathlib import Path
import pandas as pd


def extract_data():

    arquivo = Path(__file__).parent.parent / "data" / "raw" / "vendas_sujas.csv"
    
    df = pd.read_csv(arquivo)

    return df