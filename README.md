# IA Local para Desenvolvedores — Código dos Projetos

Repositório oficial do código do livro **IA Local para Desenvolvedores — Como rodar LLMs
no dispositivo e na sua infraestrutura: quantização, RAG offline e arquiteturas híbridas**.

Cada pasta corresponde a um capítulo e contém os projetos executáveis apresentados no livro.
Todo o código roda 100% local: nenhum projeto do repositório envia seus dados para a nuvem
(exceto os blocos opcionais de arquitetura híbrida do capítulo 11, claramente marcados).

## Estrutura

| Pasta | Capítulo | Conteúdo |
|---|---|---|
| `capitulo-04-primeiro-llm` | Rodando seu primeiro LLM | CLI de chat local em Python (Ollama + streaming) |
| `capitulo-05-hardware` | Hardware | Script de medição de hardware e benchmark no terminal |
| `capitulo-06-mobile` | On-Device em Mobile | Snippets nativos: Swift (MLX) e Kotlin (LiteRT-LM) |
| `capitulo-07-rag` | RAG sem nuvem | Busca semântica local: indexação e consulta com SQLite-VEC |
| `capitulo-08-multimodal` | Áudio, visão e voz | Transcrição, legendas .srt, visão local e assistente de voz |
| `capitulo-09-finetuning` | Fine-tuning | Dataset, treino QLoRA (Unsloth), teste e exportação GGUF |
| `capitulo-10-servidor` | Servindo modelos | Docker Compose do vLLM, cliente e teste de saúde |
| `capitulo-11-hibrido` | IA híbrida | Roteador de inferência local/nuvem com telemetria |
| `capitulo-12-producao` | Checklist final | Gerador de alvará de produção (vistoria interativa) |

## Pré-requisitos

1. **Ollama instalado e em execução** (`https://ollama.com`) com ao menos um modelo baixado:
   ```bash
   ollama run llama3.1:8b
