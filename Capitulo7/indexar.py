"""
Modulo de fatiamento e indexacao vetorial de documentos locais (Capitulo 7).
Processa arquivos de texto e persiste fragmentos e vetores em SQLite local.
Requisitos: pip install sentence-transformers sqlite-vec
"""

import os
import struct
import sqlite3
import sqlite_vec
from sentence_transformers import SentenceTransformer

# 1. Carrega o modelo de embeddings aberto e multilingue
#    Confira os pesos recomendados vigentes para a sua necessidade
print("Carregando o modelo de embeddings...")
modelo_embeddings = SentenceTransformer("BAAI/bge-m3")


def serializar_vetor(vetor: list) -> bytes:
    """Converte a lista de pontos flutuantes no formato binario do sqlite-vec."""
    return struct.pack(f"{len(vetor)}f", *vetor)


def fatiar_texto(conteudo: str, tamanho_fatia: int = 300, sobreposicao: int = 50) -> list:
    """Segmenta o texto em blocos de palavras com margem de sobreposicao."""
    palavras = conteudo.split()
    if not palavras:
        return []

    fatias = []
    passo = tamanho_fatia - sobreposicao
    for i in range(0, len(palavras), passo):
        trecho = " ".join(palavras[i:i + tamanho_fatia])
        fatias.append(trecho)
        if i + tamanho_fatia >= len(palavras):
            break
    return fatias


def inicializar_banco(conexao: sqlite3.Connection):
    """Ativa a extensao vetorial e cria as tabelas de dados e indice."""
    conexao.enable_load_extension(True)
    sqlite_vec.load(conexao)
    conexao.enable_load_extension(False)

    cursor = conexao.cursor()
    # Tabela convencional para metadados e textos legiveis
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origem TEXT,
            conteudo TEXT
        )
    """)
    # Tabela virtual vetorial com dimensao fixa do modelo (1024 dimensoes)
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS indice_vetorial USING vec0(
            vetor_conteudo float[1024]
        )
    """)
    conexao.commit()


def processar_diretorio(caminho_pasta: str, conexao: sqlite3.Connection):
    """Le arquivos da pasta indicada e executa o pipeline de ingestao."""
    cursor = conexao.cursor()
    # Para leitura de PDFs, adicione bibliotecas especializadas como pypdf
    arquivos = [f for f in os.listdir(caminho_pasta) if f.endswith(('.txt', '.md'))]

    for nome_arquivo in arquivos:
        caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
        with open(caminho_completo, "r", encoding="utf-8") as f:
            texto = f.read()

        fatias = fatiar_texto(texto)
        print(f"Indexando {nome_arquivo}: {len(fatias)} fragmentos gerados.")

        for fatia in fatias:
            # Gera o vetor matematico correspondente ao trecho
            vetor = modelo_embeddings.encode(fatia).tolist()
            vetor_binario = serializar_vetor(vetor)

            # Insere o texto legivel e recupera o identificador sequencial
            cursor.execute(
                "INSERT INTO documentos (origem, conteudo) VALUES (?, ?)",
                (nome_arquivo, fatia)
            )
            id_gerado = cursor.lastrowid

            # Vincula o identificador as coordenadas na tabela virtual
            cursor.execute(
                "INSERT INTO indice_vetorial (rowid, vetor_conteudo) VALUES (?, ?)",
                (id_gerado, vetor_binario)
            )

    conexao.commit()
    print("Base local de vetores atualizada com sucesso!")


if __name__ == "__main__":
    pasta_documentos = "./meus_documentos"
    os.makedirs(pasta_documentos, exist_ok=True)

    banco = sqlite3.connect("conhecimento_local.db")
    inicializar_banco(banco)
    processar_diretorio(pasta_documentos, banco)
    banco.close()