"""
Modulo de consulta vetorial e geracao fundamentada (Capitulo 7).
Resgata fragmentos do SQLite local e invoca o modelo local no Ollama.
Requisitos: pip install sentence-transformers sqlite-vec openai
"""

import sys
import struct
import sqlite3
import sqlite_vec
from openai import OpenAI
from sentence_transformers import SentenceTransformer

# Conecta ao modelo de representacao e ao servico local de inferencia
modelo_embeddings = SentenceTransformer("BAAI/bge-m3")
cliente_llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def serializar_vetor(vetor: list) -> bytes:
    """Empacota a lista de pontos flutuantes no formato do indice."""
    return struct.pack(f"{len(vetor)}f", *vetor)


def recuperar_trechos_relevantes(pergunta: str, limite: int = 4) -> list:
    """Converte a consulta em coordenadas e busca os trechos mais proximos."""
    vetor_pergunta = modelo_embeddings.encode(pergunta).tolist()
    vetor_binario = serializar_vetor(vetor_pergunta)

    conexao = sqlite3.connect("conhecimento_local.db")
    conexao.enable_load_extension(True)
    sqlite_vec.load(conexao)
    conexao.enable_load_extension(False)

    cursor = conexao.cursor()
    # Busca vetorial cruzando a tabela virtual com a tabela de texto
    # Nota de verificacao: confira a sintaxe do MATCH/k na versao vigente do sqlite-vec
    cursor.execute("""
        SELECT d.conteudo, v.distance
        FROM indice_vetorial v
        JOIN documentos d ON d.id = v.rowid
        WHERE v.vetor_conteudo MATCH ? AND k = ?
        ORDER BY v.distance
    """, (vetor_binario, limite))

    resultados = [linha[0] for linha in cursor.fetchall()]
    conexao.close()
    return resultados


def executar_geracao_contextualizada(pergunta: str, trechos: list):
    """Monta o prompt fundamentado e emite a resposta em streaming."""
    contexto_formatado = "\n---\n".join(trechos)

    instrucao_sistema = (
        "Você é um consultor analítico corporativo. Responda à pergunta do usuário "
        "baseando-se EXCLUSIVAMENTE nas informações fornecidas no contexto abaixo.\n"
        "Se os fatos necessários não estiverem presentes nos trechos, afirme de forma "
        "educada que as evidências catalogadas não contemplam os dados exigidos.\n\n"
        f"CONTEXTO DOCUMENTAL:\n{contexto_formatado}"
    )

    print("\nResposta fundamentada:\n" + "-" * 50)

    fluxo = cliente_llm.chat.completions.create(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": instrucao_sistema},
            {"role": "user", "content": pergunta}
        ],
        stream=True
    )

    for fragmento in fluxo:
        delta = fragmento.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
    print("\n" + "-" * 50)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python perguntar.py 'Sua pergunta entre aspas'")
        sys.exit(1)

    pergunta_usuario = sys.argv[1]
    print(f"Buscando referências documentais para: '{pergunta_usuario}'...")
    trechos_encontrados = recuperar_trechos_relevantes(pergunta_usuario)

    if not trechos_encontrados:
        print("Nenhuma informação localizada na base local para apoiar essa resposta.")
    else:
        executar_geracao_contextualizada(pergunta_usuario, trechos_encontrados)