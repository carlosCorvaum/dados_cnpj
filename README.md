# Cadastro Nacional da Pessoa Jurídica (CNPJ)

## Introdução

O Cadastro Nacional da Pessoa Jurídica (CNPJ) é o registro que cada entidade jurídica, seja ela uma empresa, fundação, associação ou outra forma de organização, recebe. Cada entidade possui um número de CNPJ único, composto por 14 dígitos, permitindo uma ampla gama de aplicações.

Esses dados são utilizados desde estudos acadêmicos sobre o tecido empresarial brasileiro até o desenvolvimento de ferramentas de análise de risco e inteligência de mercado. A amplitude das informações contidas nos dados abertos do CNPJ sugere um recurso valioso para quem busca entender o panorama empresarial brasileiro.

## Fonte de Dados

Os Dados Abertos do CNPJ disponibilizam informações públicas sobre as empresas registradas no Brasil. Este conjunto de dados abrange:

- Informações básicas de registro;

- Detalhes sobre os estabelecimentos;

- Dados relacionados ao regime tributário do Simples Nacional;

- Informações sobre sócios ou acionistas de cada empresa.

- Adicionalmente, inclui tabelas de apoio com informações sobre:

- Países;

- Municípios;

- Qualificações dos sócios;

- Natureza jurídica das empresas;

- Atividades econômicas (CNAEs).



# Arquitetura da Solução

<img src="docs/diagram.svg">

A arquitetura apresentada e um fluxo de ETL para os Dados Abertos de CNPJ, utilizando ferramentas modernas para processamento e disponibilização dos dados.

1. Fonte de Dados

O processo começa com a Receita Federal, que disponibiliza os Dados Abertos do CNPJ.
O Apache Airflow é responsável por orquestrar o pipeline de ETL.

2. Extração e Armazenamento

O Airflow realiza a extração dos dados brutos diretamente da Receita Federal.
Os dados brutos são armazenados no MinIO, um serviço de armazenamento de objetos compatível com S3.

3. Transformação e Carga

O Airflow processa os dados, realizando transformações necessárias.
Após a transformação, os dados são carregados no PostgreSQL, que atua como o banco de dados principal para consultas estruturadas.

4. Exposição dos Dados

Um API Gateway permite o acesso aos dados processados.
Essa API fornece informações para diferentes aplicações, como:
Ferramentas de análise de risco;
Ferramentas de inteligência de mercado;
Microsserviços, que podem consumir esses dados para diversos fins.

Essa abordagem garante um processamento escalável, seguro e eficiente, permitindo análises avançadas e integração com diversos sistemas.