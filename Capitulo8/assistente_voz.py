"""
Assistente de Voz 100% Offline: Whisper + Ollama + Piper (Capitulo 8).
Requisitos: pip install faster-whisper openai | Requer binario do Piper + voz .onnx em portugues.
"""

import subprocess
from faster_whisper import WhisperModel
from openai import OpenAI


def inicializar_componentes():
    """Inicializa os motores de transcricao e a conexao com o LLM local."""
    print("Inicializando o motor Whisper (audicao local)...")
    modelo_stt = WhisperModel("small", device="cpu", compute_type="int8")

    print("Conectando ao modelo de linguagem local (porta 11434)...")
    cliente_llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    return modelo_stt, cliente_llm


def executar_pipeline_assistente(caminho_pergunta_audio: str):
    stt, llm = inicializar_componentes()

    # 1. Audicao: transcricao do arquivo de audio da pergunta
    print(f"\n[1/3] Transcrevendo a fala do usuario a partir de: {caminho_pergunta_audio}")
    segmentos, _ = stt.transcribe(caminho_pergunta_audio, language="pt")
    texto_usuario = " ".join([seg.text.strip() for seg in segmentos]).strip()

    if not texto_usuario:
        print("Nenhuma fala compreensivel identificada no arquivo.")
        return

    print(f"Usuario disse: \"{texto_usuario}\"")

    # 2. Raciocinio: consulta ao modelo local via API padronizada
    print("\n[2/3] Solicitando resposta ao modelo de linguagem local...")
    instrucao_sistema = (
        "Você é um assistente de voz sucinto. "
        "Responda à dúvida do usuário em no máximo duas frases claras e diretas."
    )

    resposta = llm.chat.completions.create(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": instrucao_sistema},
            {"role": "user", "content": texto_usuario}
        ],
        temperature=0.3
    )
    texto_resposta = resposta.choices[0].message.content.strip()
    print(f"Assistente respondeu: \"{texto_resposta}\"")

    # 3. Fala: sintese de audio da resposta utilizando o utilitario Piper
    print("\n[3/3] Sintetizando o audio da resposta...")
    arquivo_saida_audio = "resposta_assistente.wav"

    # Nota de verificacao: ajuste os caminhos do binario './piper' e da voz '.onnx'
    # conforme a instalacao realizada na sua maquina.
    comando_piper = (
        f'echo "{texto_resposta}" | ./piper '
        f'--model pt_BR-faber-medium.onnx '
        f'--output_file {arquivo_saida_audio}'
    )

    # Executa a geracao do som via processo de linha de comando no sistema
    processo = subprocess.run(comando_piper, shell=True, capture_output=True, text=True)

    if processo.returncode == 0:
        print(f"Sucesso! Arquivo de audio de retorno gerado: {arquivo_saida_audio}")
    else:
        print(f"Falha ao sintetizar voz: {processo.stderr}")


if __name__ == "__main__":
    executar_pipeline_assistente("pergunta_usuario.wav")