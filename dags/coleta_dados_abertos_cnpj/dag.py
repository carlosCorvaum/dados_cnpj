from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import os
import sys
from airflow.utils.task_group import TaskGroup
from coleta_dados_abertos_cnpj.jobs.extract import extract
from coleta_dados_abertos_cnpj.jobs.transform.cnaes import cnaes

# Definir o caminho inicial com base no diretório onde o DAG está localizado
dag_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "coleta_dados_abertos_cnpj", "jobs"
    )
)

BASE_URL = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj"

date = "{{ ds }}"

prefixes = [
    "Cnaes",
    "Empresas",
    "Estabelecimentos",
    "Motivos",
    "Municipios",
    "Naturezas",
    "Paises",
    "Qualificacoes",
    "Simples",
    "Socios",
]

default_args = {
    "owner": "Corvaum",
    "start_date": datetime(2022, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(seconds=15),
}

with DAG(
    "coleta_dados_abertos_cnpj",
    default_args=default_args,
    schedule_interval="0 0 10 * *",
    catchup=False,
) as dag:

    # TaskGroup para processar extrações paralelas
    with TaskGroup("extract", prefix_group_id=False) as extract_group:
        for prefix in prefixes:
            PythonOperator(
                task_id=f"extract_{prefix.lower()}",
                python_callable=extract,
                op_kwargs={
                    "BASE_URL": BASE_URL,
                    "date": date,
                    "prefixes": [prefix],
                },
                dag=dag,
            )

    # TaskGroup para transformações paralelas
    with TaskGroup("transform", prefix_group_id=False) as transform_group:
        for prefix in prefixes:
            PythonOperator(
                task_id=f"transform_{prefix.lower()}",
                python_callable=cnaes,
                op_kwargs={"prefix": prefix},
                dag=dag,
            )

    # Task final (echo)
    echo_task = BashOperator(
        task_id="echo_hello_world",
        bash_command='echo "Hello, Airflow!"',
        dag=dag,
    )

    # Definição da sequência de tarefas
    extract_group >> transform_group >> echo_task
