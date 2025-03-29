import pandas as pd
from io import BytesIO
from minio import Minio


client = Minio(
    "host.docker.internal:9000",
    access_key="Meg0Wufz3QcxA6snJUel",
    secret_key="qphKazgGKNhyVkSjXdGr3HxNAWdw0pvE3MkIrrFa",
    secure=False,
)

response = client.list_objects("raw", prefix="full_cpf/Motivos/2025-01/")

# Lê e processa cada arquivo CSV
for obj in response:
    print(f"Lendo o arquivo: {obj.object_name}")

    # Obtém o objeto do MinIO
    response = client.get_object("raw", obj.object_name)

    # Lê o conteúdo do objeto como um DataFrame
    try:
        df = pd.read_csv(BytesIO(response.read()))
        print(df)
    except Exception as e:
        print(f"Erro ao processar o arquivo {obj.object_name}: {e}")
    finally:
        response.close()
        response.release_conn()
