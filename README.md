> Sales ETL Pipeline

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
➞ Sobre

Este projeto apresenta um pipeline de vendas desenvolvido como projeto de portfólio em Engenharia de Dados, com o objetivo de demonstrar conhecimentos práticos na construção de um processo ETL completo.

O pipeline realiza o processo completo de ETL:

> 𝗘𝘅𝘁𝗿𝗮𝗰𝘁 → 𝗧𝗿𝗮𝗻𝘀𝗳𝗼𝗿𝗺 → 𝗟𝗼𝗮𝗱

Os dados são extraídos de um arquivo CSV, tratados e padronizados utilizando Python e Pandas e, posteriormente, carregados em um banco PostgreSQL.

Após o carregamento, os dados podem ser analisados utilizando SQL e Power BI.

O projeto busca simular um cenário próximo ao encontrado em ambientes reais de dados, incluindo tratamento de dados inconsistentes, padronização, logs de execução, armazenamento em banco de dados e visualização dos resultados.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

➞ Tecnologias

- Python
- Pandas
- NumPy
- SQLAlchemy
- PostgreSQL
- SQL
- Power BI
- python-dotenv
- Git
- GitHub

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

➞ Estrutura do Projeto

sales_pipeline/
│
├── data/
│   ├── raw/
│   │   └── vendas_sujas.csv
│
├── logs/
│   └── pipeline.log
│
├── sql/
│   └── queries.sql
│
├── scripts/
│   ├── a_extract.py
│   ├── b_transform.py
│   ├── c_load.py
│   └── main.py 
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── run.bat
└── README.md