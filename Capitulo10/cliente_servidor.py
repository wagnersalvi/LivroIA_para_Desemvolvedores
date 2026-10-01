"""
Cliente de inferencia apontando para o servidor central da equipe (Capitulo 10).
Requisitos: pip install openai
"""

from openai import OpenAI

# Substitua '192.168.1.150' pelo endereço IP ou domínio real da sua rede interna
CLIENTE_SERVIDOR = OpenAI(
    base_url="http://192.168.1.150:8000/v1",
    api_key="token-interno-nao-utilizado"
)


def consultar_suporte_corporativo(pergunta_usuario: str):
    """Envia o chamado tecnico ao servidor compartilhado com streaming ativo."""
    resposta_em_fluxo = CLIENTE_SERVIDOR.chat.completions.create(
        model="./modelo_especialista",
        messages=[
            {"role": "system", "content": "Você é o assistente técnico interno da empresa."},
            {"role": "user", "content": pergunta_usuario}
        ],
        stream=True
    )

    print("Resposta do servidor interno:")
    for pedaco in resposta_em_fluxo:
        texto = pedaco.choices[0].delta.content
        if texto:
            print(texto, end="", flush=True)
    print()


if __name__ == "__main__":
    consultar_suporte_corporativo("Qual é o procedimento de reinicialização do roteador da filial?")