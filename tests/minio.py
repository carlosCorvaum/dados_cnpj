def df_to_s3(
    df,
    bucket_name,
    layer,
    prefix,
    date=None,
    access_key="ZEZQi4iz62AvZ31OQhy5",
    secret_key="NfpavGez5hAi1dFEswYIr5blz6QcVD65P5IliVaR",
):
    """
    Envia um DataFrame para o MinIO, organizando-o em uma estrutura de diretórios.
    """
    # Configuração do cliente MinIO
    client = Minio(
        "host.docker.internal:9000",
        access_key=access_key,
        secret_key=secret_key,
        secure=False,
    )

    # Criação do bucket, caso não exista
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # Gerar a data no formato YYYYMMDD
    date = date or datetime.now().strftime("%Y%m%d")

    # Gerar um nome único com base no prefixo e UUID
    unique_name = f"{prefix}_{uuid.uuid4().hex}"

    # Definir o caminho do arquivo no MinIO
    file_name = f"{layer}/{prefix}/{date}/{unique_name}.csv"

    # Salvar o DataFrame em um buffer CSV
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8")
    csv_buffer.seek(0)

    # Enviar para o MinIO
    client.put_object(
        bucket_name=bucket_name,
        object_name=file_name,
        data=csv_buffer,
        length=csv_buffer.getbuffer().nbytes,
        content_type="text/csv",
    )
    print(f"Arquivo salvo: {file_name}")
