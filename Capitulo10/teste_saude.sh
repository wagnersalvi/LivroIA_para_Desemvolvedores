#!/usr/bin/env bash
# Teste de fumaça e verificação de integridade (Capitulo 10)

# 1. Consulta a rota de integridade para confirmar servico operacional
curl -s http://localhost:8000/health

# 2. Medicao do tempo de resposta total com uma requisicao minima
# A flag -w imprime o cronometro do tempo total consumido
curl -s -w "\nTempo total de resposta: %{time_total} segundos\n" \
    -X POST http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "./modelo_especialista", "messages": [{"role": "user", "content": "ping"}], "max_tokens": 1}'