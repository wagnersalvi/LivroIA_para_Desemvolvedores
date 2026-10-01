#!/usr/bin/env bash
# Medicao de hardware e benchmark de inferencia (Capitulo 5).
# Execute os blocos correspondentes ao seu sistema operacional.

# ---- Linux: inventario de hardware ----
# Identifica placas aceleradoras conectadas ao barramento PCI
lspci | grep -i 'vga\|3d\|display'

# Exibe o total de memoria RAM em formato legivel
free -h

# ---- macOS (Apple Silicon): ficha tecnica do chip ----
system_profiler SPHardwareDataType | grep 'Chip\|Memory'
sysctl hw.memsize

# ---- Windows (via PowerShell): VRAM e RAM ----
# nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
# wmic computersystem get TotalPhysicalMemory

# ---- Benchmark nativo do Ollama (modo verboso) ----
# No final da resposta o terminal imprime as metricas:
# prompt eval rate  = tokens de ENTRADA lidos por segundo
# eval rate         = tokens de SAIDA gerados por segundo (a metrica do chat)
ollama run --verbose llama3.1:8b "Explique a importancia da banda de memoria em um paragrafo conciso."

# ---- Benchmark avancado (opcional): llama-bench da biblioteca llama.cpp ----
# -m: caminho do GGUF | -p: tokens do prompt | -n: tokens gerados | -t: threads
# ./llama-bench -m ./models/llama-3.1-8b-instruct-q4_k_m.gguf -p 512,2048 -n 128 -t 8