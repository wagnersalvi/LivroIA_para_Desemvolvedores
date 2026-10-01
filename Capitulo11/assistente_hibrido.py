"""
Assistente corporativo hibrido para terminal (Capitulo 11).
Roteador local/nuvem com triagem por regras, streaming e telemetria.
Requisitos: pip install openai
A chave da nuvem deve ficar em variavel de ambiente: CHAVE_API_NUVEM
"""

import os
import sys
import time
import socket
from openai import OpenAI

# 1. Configuracao dos clientes de inferencia
cliente_local = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="token-interno"
)

cliente_nuvem = OpenAI(
    base_url="https://api.provedor-externo.com/v1",
    api_key=os.environ.get("CHAVE_API_NUVEM", "chave-demonstracao")
)

# 2. Base de registro operacional em memoria
historico_telemetria = {
    "total_requisicoes": 0,
    "destinos": {"local": 0, "nuvem": 0},
    "tokens_estimados": 0
}


def checar_conexao() -> bool:
    """Verifica rapidamente a viabilidade da rota externa de comunicacao."""
    try:
        socket.setdefaulttimeout(1.5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except (socket.timeout, OSError):
        return False


def despachar_fluxo(cliente: OpenAI, modelo: str, mensagens: list) -> str:
    """Transmite os tokens gerados em tempo real na tela do operador."""
    fluxo = cliente.chat.completions.create(
        model=modelo,
        messages=mensagens,
        stream=True
    )

    texto_gerado = []
    for pedaco in fluxo:
        fragmento = pedaco.choices[0].delta.content or ""
        if fragmento:
            print(fragmento, end="", flush=True)
            texto_gerado.append(fragmento)

    print()  # Quebra final de linha
    return "".join(texto_gerado)


def executar_atendimento_hibrido(pergunta_usuario: str, canal: str) -> None:
    """Aplica as diretrizes de triagem, realiza a chamada e grava as metricas."""
    inicio_tempo = time.time()
    mensagens = [
        {"role": "system", "content": "Você é um assistente técnico corporativo útil e direto."},
        {"role": "user", "content": pergunta_usuario}
    ]

    # Avaliacao da rota adequada (hierarquia: privacidade > offline > capacidade > custo)
    canais_restritos = ["financeiro", "saude", "rh"]
    destino_escolhido = "local"
    modelo_alvo = "modelo-local-8b"
    cliente_alvo = cliente_local
    motivo_rota = "privacidade_preservada"

    if canal in canais_restritos:
        destino_escolhido = "local"
        motivo_rota = "regra_privacidade"
    elif not checar_conexao():
        destino_escolhido = "local"
        motivo_rota = "contingencia_offline"
    elif len(pergunta_usuario.split()) > 100:
        # Consultas muito extensas e complexas sao delegadas a nuvem se houver rede
        try:
            destino_escolhido = "nuvem"
            modelo_alvo = "modelo-comercial-fronteira"
            cliente_alvo = cliente_nuvem
            motivo_rota = "capacidade_cognitiva"
        except Exception:
            destino_escolhido = "local"
            motivo_rota = "fallback_emergencia"
    else:
        destino_escolhido = "local"
        motivo_rota = "politica_custo_zero"

    # Exibicao do cabecalho de resposta
    print(f"\n[Encaminhamento: {destino_escolhido.upper()} | Motivo: {motivo_rota}]")
    print("Resposta: ", end="")

    try:
        texto_saida = despachar_fluxo(cliente_alvo, modelo_alvo, mensagens)
    except Exception as erro:
        print(f"\n[Falha de operacao no motor {destino_escolhido}]: {erro}")
        return

    # Contabilizacao do tempo de inferencia e telemetria
    duracao = time.time() - inicio_tempo
    # Estimativa de tokens: media aproximada de uma palavra e meia por token
    tokens_calculados = int((len(pergunta_usuario.split()) + len(texto_saida.split())) * 1.3)

    historico_telemetria["total_requisicoes"] += 1
    historico_telemetria["destinos"][destino_escolhido] += 1
    historico_telemetria["tokens_estimados"] += tokens_calculados

    print(f"[Log Auditoria] Tempo: {duracao:.2f}s | Volume Calculado: ~{tokens_calculados} tokens\n")


def exibir_relatorio_administrativo() -> None:
    """Imprime o balanco consolidado de utilizacao da infraestrutura."""
    total = historico_telemetria["total_requisicoes"]
    locais = historico_telemetria["destinos"]["local"]
    nuvem = historico_telemetria["destinos"]["nuvem"]

    print("\n" + "=" * 50)
    print("PAINEL DE AUDITORIA E TELEMETRIA DA INFRAESTRUTURA")
    print("=" * 50)
    print(f"Total de atendimentos realizados: {total}")
    print(f"Atendimentos retidos internamente (Custo Zero): {locais}")
    print(f"Atendimentos despachados para a nuvem: {nuvem}")
    print(f"Volume acumulado de processamento: ~{historico_telemetria['tokens_estimados']} tokens")

    if total > 0:
        taxa_retencao = (locais / total) * 100
        print(f"Indice de independencia de infraestrutura: {taxa_retencao:.1f}%")
    print("=" * 50 + "\n")


def loop_terminal():
    """Ciclo interativo com comandos de operacao."""
    canal_ativo = "geral"
    print("Assistente Corporativo Hibrido Inicializado.")
    print("Comandos: '/canal [nome]' para alternar o canal | '/status' para relatorio | 'sair' para encerrar.")
    print(f"Canal operacional padrao: [{canal_ativo}]")

    while True:
        try:
            entrada = input(f"\n[{canal_ativo}] Digite sua solicitacao: ").strip()

            if not entrada:
                continue
            if entrada.lower() == "sair":
                break
            if entrada.lower() == "/status":
                exibir_relatorio_administrativo()
                continue
            if entrada.lower().startswith("/canal"):
                pedacos = entrada.split()
                if len(pedacos) > 1:
                    canal_ativo = pedacos[1].lower()
                    print(f"[Sistema]: Canal operacional alterado para '{canal_ativo}'.")
                else:
                    print("[Sistema]: Informe o canal desejado (exemplo: /canal financeiro).")
                continue

            executar_atendimento_hibrido(entrada, canal_ativo)

        except KeyboardInterrupt:
            print("\nEncerrando sessao do assistente.")
            break


if __name__ == "__main__":
    loop_terminal()