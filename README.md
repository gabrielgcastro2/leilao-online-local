# Projeto: Leilão Online (Simulação Local)

Este é um projeto simples em Python para simular uma arquitetura de leilão online desacoplada, similar ao que seria feito na AWS.

## Arquitetura (Simulada)

* **API Gateway (Simulado):** `api_server.py` (usando Flask). Recebe os lances.
* **Lambda 1 (Simulada):** A função `dar_lance()` no `api_server.py`. Ela é rápida e apenas "enfileira" o lance.
* **Fila SQS (Simulada):** Uma tabela `Lances` no banco `leilao.db`. O `api_server.py` insere lances com status `PENDENTE`.
* **Lambda 2 (Simulada):** O script `worker.py`. Ele roda separadamente, lendo a tabela `Lances` (a "fila") e processando os lances pendentes.
* **DynamoDB (Simulado):** A tabela `ItensLeilao` no banco `leilao.db`.

## Lógica Obrigatória

* **`for` loop:** Usado no `worker.py` para processar múltiplos lances da fila.
* **`if/else`:** Usado no `worker.py` para verificar se o `novo_lance` é maior que o `lance_atual`.