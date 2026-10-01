"""
Analise de imagens locais utilizando modelo multimodal via Ollama (Capitulo 8).
Requisitos: pip install openai | Requer modelo de visao no Ollama (ex.: llava)
"""

import base64
from openai import OpenAI


def codificar_imagem_em_base64(caminho_imagem: str) -> str:
    """Le um arquivo de imagem em bytes e converte para texto puro em Base64."""
    with open(caminho_imagem, "rb") as arquivo:
        dados_binarios = arquivo.read()
        return base64.b64encode(dados_binarios).decode("utf-8")


def analisar_documento_com_visao(caminho_imagem: str, pergunta: str):
    # Conecta a instancia do Ollama na porta padrao (Capitulo 4)
    cliente = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    # Converte o arquivo de imagem para transmissao segura em texto
    imagem_base64 = codificar_imagem_em_base64(caminho_imagem)
    uri_imagem = f"data:image/jpeg;base64,{imagem_base64}"

    print("Enviando imagem e instrucao para a inferencia local...")
    # Requisicao multimodal combinando prompt textual e a imagem tratada
    resposta = cliente.chat.completions.create(
        model="llava:7b",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": pergunta},
                    {"type": "image_url", "image_url": {"url": uri_imagem}}
                ]
            }
        ],
        stream=True
    )

    print("\nResposta da analise visual:")
    for pedaco in resposta:
        texto = pedaco.choices[0].delta.content
        if texto:
            print(texto, end="", flush=True)
    print()


if __name__ == "__main__":
    analisar_documento_com_visao(
        caminho_imagem="recibo_despesa.jpg",
        pergunta="Extraia a data, o nome do estabelecimento e o valor final deste recibo."
    )