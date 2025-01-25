from datetime import datetime
import requests
from bs4 import BeautifulSoup
from minio import Minio
from io import BytesIO
import uuid
import zipfile
import os
import shutil


def list_files(URL: str, prefixes: list[str]):
    """
    Lista todos os arquivos com extensão '.zip' disponíveis em um diretório web
    que começam com os prefixos especificados.
    """
    file_list = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()

        # Usando BeautifulSoup para parsear o conteúdo HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Encontrar todos os links com a tag <a>
        links = soup.find_all("a", href=True)

        # Filtra os links que terminam com '.zip' e começam com os prefixos fornecidos
        for link in links:
            href = link["href"]
            if href.endswith(".zip") and any(
                href.startswith(prefix) for prefix in prefixes
            ):
                file_list.append(href)
        return file_list
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erro ao listar os arquivos: {e}")


def download_with_requests(download_file_url):
    """
    Faz o download de um arquivo utilizando requests e retorna o conteúdo em memória como um objeto BytesIO.
    """
    try:
        print(f"Baixando o arquivo: {download_file_url}")
        with requests.get(download_file_url, stream=True) as r:
            r.raise_for_status()
            file_in_memory = BytesIO()
            for chunk in r.iter_content(chunk_size=8192):
                file_in_memory.write(chunk)
            file_in_memory.seek(0)
            print(f"Download concluído: {download_file_url}")
            return file_in_memory
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer o download do arquivo: {e}")
        return None


def unzip(zip_file):
    """
    Descompacta o arquivo .zip e retorna os caminhos completos dos arquivos extraídos.
    """
    temp_extract_path = f"/tmp/{uuid.uuid4().hex}_extracted"
    os.makedirs(temp_extract_path, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(temp_extract_path)

        extracted_files = [
            os.path.join(temp_extract_path, file)
            for file in os.listdir(temp_extract_path)
        ]
        print(f"Arquivos descompactados: {extracted_files}")
        return extracted_files, temp_extract_path
    except zipfile.BadZipFile as e:
        print(f"Erro ao descompactar o arquivo ZIP: {e}")
        return [], None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return [], None


def upload_to_bucket(file, bucket_name, layer, prefix, date=None):
    client = Minio(
        "host.docker.internal:9000",
        access_key="Meg0Wufz3QcxA6snJUel",
        secret_key="qphKazgGKNhyVkSjXdGr3HxNAWdw0pvE3MkIrrFa",
        secure=False,
    )

    date = date or datetime.now().strftime("%Y%m%d")
    unique_name = f"{prefix}_{uuid.uuid4().hex}"
    file_name = f"{layer}/{prefix}/{date}/{unique_name}.csv"

    file.seek(0)
    client.put_object(
        bucket_name=bucket_name,
        object_name=file_name,
        data=file,
        length=file.getbuffer().nbytes,
        content_type="text/csv",
    )

    print(f"Arquivo {file_name} carregado com sucesso no MinIO!")


def extract(BASE_URL: str, date: str, prefixes: list[str]):
    BUCKET_NAME = "raw"
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    format_date = date_obj.strftime("%Y-%m")
    print(f"Data formatada: {format_date}")

    url = f"{BASE_URL}/{format_date}"

    try:
        files = list_files(url, prefixes)
        print(f"Arquivos encontrados: {files}")
    except RuntimeError as e:
        print(f"Erro ao obter a lista de arquivos: {e}")
        raise

    for file in files:
        download_file_url = f"{url}/{file}"
        try:
            zip_file = download_with_requests(download_file_url)
            extracted_files, temp_path = unzip(zip_file)

            for extracted_file in extracted_files:
                file_prefix = next(
                    (prefix for prefix in prefixes if prefix in file), "Outros"
                )

                with open(extracted_file, "rb") as f:
                    file_content = BytesIO(f.read())

                upload_to_bucket(
                    file_content,
                    BUCKET_NAME,
                    "full_cpf",
                    file_prefix,
                    format_date,
                )

            # Limpeza do diretório temporário
            shutil.rmtree(temp_path, ignore_errors=True)

        except Exception as e:
            print(f"Erro ao processar o arquivo {file}: {e}")
            continue
