// Nucleo de inferencia local no Android com LiteRT-LM (Capitulo 6).
// A API exata segue a documentacao vigente em developers.google.com/edge.

import com.google.ai.edge.litert.lm.*

// 1. Cria a sessao de execucao do modelo UMA VEZ (pesos na memoria do app)
suspend fun criarSessao(caminhoDoModelo: String): LlmSession {
    val opcoes = SessionOptions(
        modelPath = caminhoDoModelo
    )
    return LlmSession.create(opcoes)
}

// 2. Gera a resposta token a token com callback de streaming
suspend fun gerarResposta(
    sessao: LlmSession,
    prompt: String,
    aoReceberFragmento: (String) -> Unit
) {
    // Despacha o prompt para o motor de inferencia local
    sessao.generateResponseAsync(prompt)
    // Consome cada fragmento emitido pelo callback de streaming
    for (fragmento in sessao.tokenStream()) {
        aoReceberFragmento(fragmento)
    }
}

// 3. Checagem anti-crash: recusa educada antes de carregar (logica identica em Swift)
fun podeCarregarModelo(caminho: String, memoriaLivreDoAparelho: Long): Boolean {
    val tamanhoArquivo = java.io.File(caminho).length()
    // Margem de seguranca para o cache KV e o restante do app (~512 MB em escala mobile)
    val margemSeguranca = 512L * 1024 * 1024
    return tamanhoArquivo + margemSeguranca <= memoriaLivreDoAparelho
}