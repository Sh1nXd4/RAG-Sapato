📄 Documentação de Governança de Dados - Sprint 3
1. Arquitetura e Armazenamento (Medallion)

O Data Lake foi estruturado em 3 camadas lógicas: Bronze, Silver e Gold.
(Se for questionado sobre o MinIO): A estrutura atual foi desenvolvida em sistema de arquivos local (local filesystem) para validação do pipeline, estando pronta para ser migrada para buckets do MinIO (Object Storage) alterando apenas os caminhos de gravação no script Python.
2. Linhagem de Dados (Data Lineage)

Origem: Arquivo plano food_coded.csv extraído de pesquisa de hábitos alimentares.
Camada Bronze: O arquivo é ingerido em seu formato bruto (.csv) sem nenhuma alteração, garantindo a imutabilidade do dado original.
Camada Silver: O dado é convertido para .parquet (compressão colunar).
Transformações aplicadas: Remoção de colunas duplicadas, conversão de tipagem estrita nas colunas numéricas (GPA e weight), preenchimento de nulos (fillna) em campos textuais críticos e padronização dos cabeçalhos para lower case.
Camada Gold: Criação de tabelas agregadas para consumo do time de Negócios/BI, como metricas_por_genero e top_comfort_food_esportistas.
3. Dicionário de Dados (Resumo Camada Silver)

gpa (Float): Grade Point Average (Média de notas do aluno).
gender (Inteiro): Identificador de gênero do respondente (1 ou 2).
comfort_food (Texto): Alimentos consumidos em momentos de conforto emocional.
weight (Float): Peso do estudante.
sports (Inteiro): Indicador se o estudante pratica esportes (1 = Sim, 2 = Não).
4. Políticas de Retenção

Bronze: Retenção permanente (histórico completo).
Silver/Gold: Sobrescrita permitida a cada processamento (atualização de estado).
