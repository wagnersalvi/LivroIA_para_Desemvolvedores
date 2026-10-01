"""
Conversor de audio para arquivo de legendas padronizado .srt (Capitulo 8).
Requisitos: pip install faster-whisper
"""

from faster_whisper import WhisperModel


def formatar_tempo_srt(segundos_totais: float) -> str:
    """Converte segundos para a marcacao estrita do padrao SRT: HH:MM:SS,mmm"""
    horas = int(segundos_totais // 3600)
    minutos = int((segundos_totais % 3600) // 60)
    segundos = int(segundos_totais % 60)
    milissegundos = int((segundos_totais - int(segundos_totais)) * 1000)
    # Observe a virgula obrigatoria antes dos milissegundos no padrao SubRip
    return f"{horas:02d}:{minutos:02d}:{segundos:02d},{milissegundos:03d}"


def exportar_legenda_srt(caminho_audio: str, caminho_saida_srt: str):
    print("Carregando o motor de transcricao...")
    modelo = WhisperModel("small", device="cpu", compute_type="int8")

    print(f"Transcrevendo {caminho_audio} para formato de legenda...")
    segmentos, _ = modelo.transcribe(caminho_audio, language="pt")

    # Abre o arquivo de saida garantindo a codificacao UTF-8
    with open(caminho_saida_srt, "w", encoding="utf-8") as arquivo_legenda:
        indice = 1
        for segmento in segmentos:
            inicio = formatar_tempo_srt(segmento.start)
            fim = formatar_tempo_srt(segmento.end)
            texto = segmento.text.strip()

            arquivo_legenda.write(f"{indice}\n")
            arquivo_legenda.write(f"{inicio} --> {fim}\n")
            arquivo_legenda.write(f"{texto}\n\n")
            indice += 1

    print(f"Arquivo de legendas salvo com sucesso em: {caminho_saida_srt}")


if __name__ == "__main__":
    exportar_legenda_srt("entrevista.mp3", "entrevista_legendada.srt")