"""
CLI de Chat Local para Modelos Open Source.
Uso no terminal: python chat_local.py [nome_do_modelo]
Exemplo: python chat_local.py llama3.1:8b
"""

import sys
from openai import OpenAI
from openai import APIConnectionError


def inicializar_cliente() -> OpenAI:
    """Cria e devolve o cliente HTTP conectado à porta local do Ollama."""
    return OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )


def responder_com_streaming(cliente: OpenAI, modelo: str, historico: list) -> str:
    """Envia o histórico acumulado ao modelo e exibe os tokens em fluxo."""
    fluxo = cliente.chat.completions.create(
        model=modelo,
        messages=historico,
        stream=True
    )

    resposta_completa = []

    # Processa cada fragmento de texto conforme é gerado pela inferência
    for pedaco in fluxo:
        delta = pedaco.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
            resposta_completa.append(delta)

    print()  # Quebra de linha após o fim da resposta
    return "".join(resposta_completa)


def loop_principal():
    """Ciclo de vida interativo do chat de terminal."""
    # Define o modelo padrão caso o desenvolvedor não passe argumento no terminal
    modelo_alvo = sys.argv[1] if len(sys.argv) > 1 else "llama3.1:8b"
    cliente = inicializar_cliente()

    # Mensagem permanente de sistema no topo da pilha de contexto
    instrucao_sistema = {
        "role": "system",
        "content": "Você é um assistente local executado via terminal. Responda em português de forma clara."
    }

    historico = [instrucao_sistema]

    print("=" * 60)
    print(f"Chat Local Ativo | Modelo: {modelo_alvo}")
    print("Comandos: digite '/limpar' para reiniciar ou Ctrl+C para encerrar")
    print("=" * 60)

    while True:
        try:
            entrada = input("\nVocê: ").strip()

            if not entrada:
                continue

            # Comando operacional: zera o histórico e reduz o cache KV
            if entrada.lower() == "/limpar":
                historico = [instrucao_sistema]
                print("\n[Memória limpa! A escrivaninha de contexto foi esvaziada.]")
                continue

            # Registra a mensagem do usuário no histórico acumulado
            historico.append({"role": "user", "content": entrada})

            print(f"\n{modelo_alvo}: ", end="")
            conteudo_resposta = responder_com_streaming(cliente, modelo_alvo, historico)

            # Mantém coerência nos próximos turnos guardando a resposta emitida
            historico.append({"role": "assistant", "content": conteudo_resposta})

        except APIConnectionError:
            print("\n[Erro]: Falha ao conectar ao Ollama. O serviço está em execução na porta 11434?")
            break
        except KeyboardInterrupt:
            print("\n\nSessão encerrada pelo usuário. Até a próxima!")
            break


if __name__ == "__main__":
    loop_principal()