"""
Transcricao de audio local com marcacao temporal (Capitulo 8).
Requisitos: pip install faster-whisper
"""

from faster_whisper import WhisperModel


def transcrever_arquivo_local(caminho_audio: str):
    # Opcoes comuns de tamanho: 'tiny', 'base', 'small', 'medium'
    print("Carregando o modelo de transcricao na memoria...")
    modelo = WhisperModel("medium", device="cpu", compute_type="int8")

    print(f"Iniciando a transcricao de: {caminho_audio}")
    segmentos, informacoes = modelo.transcribe(caminho_audio, language="pt")

    print(f"Idioma detectado com probabilidade de {informacoes.language_probability:.2f}")
    print("--- Transcricao em andamento ---")

    for segmento in segmentos:
        tempo_inicio = f"{segmento.start:.2f}s"
        tempo_fim = f"{segmento.end:.2f}s"
        print(f"[{tempo_inicio} -> {tempo_fim}]: {segmento.text}")


if __name__ == "__main__":
    # Substitua pelo caminho de uma gravacao em .mp3, .wav ou .m4a
    transcrever_arquivo_local("reuniao_equipe.mp3")