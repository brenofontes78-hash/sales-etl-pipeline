import logging
import pandas as pd
import numpy as np

MAPA_ESTADOS = {
    'acre': 'AC', 'alagoas': 'AL', 'amapa': 'AP', 'amazonas': 'AM', 
    'bahia': 'BA', 'ceara': 'CE', 'distrito federal': 'DF', 'espirito santo': 'ES', 
    'goias': 'GO', 'maranhao': 'MA', 'mato grosso': 'MT', 'mato grosso do sul': 'MS', 
    'minas gerais': 'MG', 'para': 'PA', 'paraiba': 'PB', 'parana': 'PR', 
    'pernambuco': 'PE', 'piaui': 'PI', 'rio de janeiro': 'RJ', 'rio grande do norte': 'RN', 
    'rio grande do sul': 'RS', 'rondonia': 'RO', 'roraima': 'RR', 'santa catarina': 'SC', 
    'sao paulo': 'SP', 'sergipe': 'SE', 'tocantins': 'TO'
}


def corrigir_preco(val):
    """Trata e padroniza os diferentes formatos de moeda e separadores decimais."""
    val = str(val).replace('R$', '').replace('BRL', '').strip().lower()
    if val in ['nan', 'nd', 'n/a', 'sem preco', 'sem preco_']:
        return np.nan
    try:
        if ',' in val and '.' in val:
            val = val.replace('.', '').replace(',', '.')
        elif ',' in val:
            val = val.replace(',', '.')
        elif '.' in val and len(val.split('.')[-1]) > 2:
            val = str(round(float(val), 2))
        return float(val)
    except (ValueError, TypeError):
        return np.nan


def padronizar_texto_base(df):
    """Aplica caixa baixa, remove espaços e limpa caracteres especiais das colunas de texto."""
    for col in ['nome_produto', 'categoria_prod', 'uf_cliente', 'forma_pagamento']:
        df[col] = df[col].astype(str).str.strip().str.lower()
        df[col] = df[col].str.replace(r'[@_!#\$]', '', regex=True)
        df[col] = df[col].replace(['nd', 'nan', 'n/a', 'nao categorizado'], np.nan)
    return df

def limpar_cadastros(df):
    """Garante a formatação dos identificadores de transações e clientes."""
    df['id_transacao'] = df['id_transacao'].astype(str).str.strip()
    df['id_transacao'] = df['id_transacao'].apply(
        lambda x: f"TRN-{x}" if (x != 'nan' and not x.startswith("TRN-")) else x
    )
    df['id_transacao'] = df['id_transacao'].replace('nan', np.nan)
    
    df['id_cliente'] = df['id_cliente'].astype(str).str.strip().str.replace("ID-", "", regex=False)
    df['id_cliente'] = df['id_cliente'].replace('nan', np.nan)
    return df

def limpar_datas(df):
    """Converte e padroniza a coluna temporal, eliminando registros nulos."""
    df['data_da_venda'] = pd.to_datetime(df['data_da_venda'], errors='coerce', format='mixed')
    df = df.dropna(subset=['data_da_venda'])
    return df

def padronizar_produtos(df):
    """Corrige falhas de digitação nos produtos e reconstrói categorias nulas."""
    df.loc[df['nome_produto'].str.contains('mous', na=False), 'nome_produto'] = 'mouse sem fio'
    df.loc[df['nome_produto'].str.contains('phon|smar', na=False), 'nome_produto'] = 'smartphone y'
    df.loc[df['nome_produto'].str.contains('fon|ouvid', na=False), 'nome_produto'] = 'fone de ouvido'
    df.loc[df['nome_produto'].str.contains('tecl|m3c', na=False), 'nome_produto'] = 'teclado mecanico'
    df.loc[df['nome_produto'].str.contains('not|book', na=False), 'nome_produto'] = 'notebook x'
    df.loc[df['nome_produto'].str.contains('moni|tora', na=False), 'nome_produto'] = 'monitor 24'
    df.loc[df['nome_produto'].str.contains('tab', na=False), 'nome_produto'] = 'tablet z'
    df['nome_produto'] = df['nome_produto'].fillna('sem nome')
    df['nome_produto'] = df['nome_produto'].replace('tbl3t z','tablet z')

    mapa_categorias = df.dropna(subset=['categoria_prod']).set_index('nome_produto')['categoria_prod'].to_dict()
    df['categoria_prod'] = df['categoria_prod'].fillna(df['nome_produto'].map(mapa_categorias))
    df['categoria_prod'] = df['categoria_prod'].fillna('nao categorizado')
    return df

def tratar_valores(df):

    df['qtd_vendida'] = df['qtd_vendida'].astype(str).str.extract(r'(\d+)')
    df['qtd_vendida'] = pd.to_numeric(df['qtd_vendida'], errors='coerce').fillna(0).astype(int)
    df = df[df['qtd_vendida'] > 0]

    df['preco_unitario'] = df['preco_unitario'].apply(corrigir_preco)
    medianas = df.groupby('nome_produto')['preco_unitario'].transform('median')
    df['preco_unitario'] = df['preco_unitario'].fillna(medianas)
    df = df[df['preco_unitario'] > 0]
    
    df['faturamento_total'] = df['qtd_vendida'] * df['preco_unitario']
    return df

def limpar_localidade_e_pagamentos(df):
    """Mapeia nomes de estados para siglas padrão e trata formas de pagamento."""
    df['uf_cliente'] = df['uf_cliente'].str.replace('-', '', regex=False).str.strip()
    df['uf_cliente'] = df['uf_cliente'].apply(lambda x: MAPA_ESTADOS.get(x, x).upper() if pd.notna(x) else x)

    df['forma_pagamento'] = df['forma_pagamento'].replace(['cc', 'ccred', 'c. créd.'], 'cartao de credito')
    df['forma_pagamento'] = df['forma_pagamento'].fillna('nao informado')
    return df


def transform_data(data):
    """Executa a orquestração sequencial de todas as subetapas do pipeline de transformação."""
    linhas_brutas = len(data)
    
    df = data.copy()
    df = df.drop_duplicates()
    linhas_sem_duplicatas = len(df)

    df = padronizar_texto_base(df)
    logging.info("Padronização de textos concluída.")

    df = limpar_cadastros(df)
    logging.info("Padronização dos cadastros concluída.")

    df = limpar_datas(df)
    logging.info("Tratamento das datas concluído.")

    df = padronizar_produtos(df)
    logging.info("Padronização de produtos e categorias concluída.")

    df = tratar_valores(df)
    logging.info("Tratamento dos valores concluído.")

    df = limpar_localidade_e_pagamentos(df)
    logging.info("Padronização de estados e formas de pagamento concluída.")

    linhas_finais = len(df)
    
    logging.info(f"Linhas brutas: {linhas_brutas}")
    logging.info(f"Linhas removidas por dados inválidos: {linhas_sem_duplicatas - linhas_finais}")
    logging.info(f"Registros finais após transformação: {linhas_finais}")

    return df
