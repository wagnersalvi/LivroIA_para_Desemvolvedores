// Nucleo de inferencia local no iOS com MLX Swift (Capitulo 6).
// Dependencia (Swift Package Manager): https://github.com/ml-explore/mlx-swift-examples
// Confira a URL e as versoes vigentes na documentacao oficial antes de compilar.

import MLXLMCommon
import MLXLLM

// 1. Carrega os pesos do modelo UMA VEZ e guarda a referencia
//    (o caminho aponta para o modelo quantizado de 1-4B do app)
func carregarModelo(caminho: String) async throws -> ModelContainer {
    let configuracao = ModelConfiguration(id: caminho)
    // A chamada real de carregamento segue a documentacao vigente do MLX Swift
    let container = try await LLMModelFactory.shared.loadContainer(
        configuration: configuracao
    )
    return container
}

// 2. Gera a resposta token a token (streaming) usando o container
func gerarResposta(container: ModelContainer, prompt: String) async throws {
    // Abre uma sessao de contexto com os pesos ja na memoria
    let resultado = try await container.perform { contexto in
        let entrada = try await contexto.prepare(
            input: .init(prompt: prompt)
        )
        // Itera sobre cada token gerado pelo modelo
        for await pedaco in contexto.generate(confirmation: entrada) {
            let texto = Tokenizer.decode(pedaco)
            print(texto, terminator: "")
        }
    }
}