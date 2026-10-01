"""
Gerador de relatorio de verificacao — o alvara de producao (Capitulo 12).
Percorre os itens de vistoria, registra os estados e emite o laudo final.
Python puro: nenhuma dependencia externa.
"""

ITENS_VISTORIA = [
    {
        "id": "MOD-01",
        "bloco": "Modelo",
        "descricao": "Licenca comercial da versao exata foi auditada e documentada",
        "estado": "PENDENTE"
    },
    {
        "id": "MOD-02",
        "bloco": "Modelo",
        "descricao": "Bateria de 20-50 evals proprios rodou no hardware e quantizacao finais",
        "estado": "PENDENTE"
    },
    {
        "id": "HW-01",
        "bloco": "Hardware",
        "descricao": "Memoria total (modelo + KV cache) calculada com margem de seguranca",
        "estado": "PENDENTE"
    },
    {
        "id": "HW-02",
        "bloco": "Hardware",
        "descricao": "Limite de contexto (num_ctx) configurado apenas para o necessario",
        "estado": "PENDENTE"
    },
    {
        "id": "APP-01",
        "bloco": "Aplicacao",
        "descricao": "Prompt de sistema testado contra tentativas basicas de abuso e injecao",
        "estado": "PENDENTE"
    },
    {
        "id": "APP-02",
        "bloco": "Aplicacao",
        "descricao": "Fluxo e retencao de dados validados junto ao juridico ou DPO",
        "estado": "PENDENTE"
    },
    {
        "id": "RAG-01",
        "bloco": "Pipeline",
        "descricao": "Chunking testado e validado com documentos reais da organizacao",
        "estado": "PENDENTE"
    },
    {
        "id": "OPS-01",
        "bloco": "Operacao",
        "descricao": "Procedimento de rollback de modelo e conteiner testado na pratica",
        "estado": "PENDENTE"
    },
    {
        "id": "OPS-02",
        "bloco": "Operacao",
        "descricao": "Monitoramento de tempo de fila, velocidade e taxa de erros ativo",
        "estado": "PENDENTE"
    },
    {
        "id": "PROD-01",
        "bloco": "Produto",
        "descricao": "Documento publico sobre limites e escopo do assistente elaborado",
        "estado": "PENDENTE"
    }
]


def coletar_respostas(itens: list) -> list:
    """Apresenta cada item pendente e registra a classificacao do operador."""
    print("=" * 70)
    print("VISTORIA DE PRODUCAO: IA LOCAL PARA DESENVOLVEDORES")
    print("Opcoes: [V] Verificado com sucesso | [N] Nao aplicavel | [Enter] Manter pendente")
    print("=" * 70)

    for item in itens:
        if item["estado"] == "PENDENTE":
            print(f"\n[{item['id']}] Bloco: {item['bloco']}")
            print(f"Item: {item['descricao']}")
            escolha = input("Situacao operacional (V/N/Enter): ").strip().upper()

            if escolha == "V":
                item["estado"] = "VERIFICADO"
            elif escolha == "N":
                item["estado"] = "NAO_APLICAVEL"
            else:
                item["estado"] = "PENDENTE"

    return itens


def emitir_relatorio(itens: list):
    """Calcula indices de prontidao e emite o laudo final de liberacao."""
    total = len(itens)
    verificados = sum(1 for i in itens if i["estado"] == "VERIFICADO")
    nao_aplicaveis = sum(1 for i in itens if i["estado"] == "NAO_APLICAVEL")
    pendentes = [i for i in itens if i["estado"] == "PENDENTE"]

    # Conforme regra editorial do livro, calculo realizado em texto simples
    # Percentual de prontidao = (verificados + nao_aplicaveis) dividido por total vezes 100
    prontos = verificados + nao_aplicaveis
    percentual_prontidao = (prontos / total) * 100 if total > 0 else 0

    print("\n" + "=" * 70)
    print("LAUDO CONCLUSIVO DE AUDITORIA OPERACIONAL")
    print("=" * 70)
    print(f"Total de itens vistoriados: {total}")
    print(f"Itens verificados em teste: {verificados}")
    print(f"Itens dispensados (N/A):    {nao_aplicaveis}")
    print(f"Itens pendentes de teste:   {len(pendentes)}")
    print(f"Indice de prontidao final:  {percentual_prontidao:.1f}%\n")

    if not pendentes:
        print("PARECER FINAL: [ALVARA DE PRODUCAO EMITIDO]")
        print("O sistema atende a todos os requisitos mandatorios de seguranca e estabilidade.")
    else:
        print(f"PARECER FINAL: [BLOQUEADO - {len(pendentes)} ITEM(NS) PENDENTE(S)]")
        print("A liberacao para usuarios finais permanece vedada ate a solucao das pendencias:\n")
        for p in pendentes:
            print(f" -> [{p['id']}] {p['bloco']}: {p['descricao']}")
    print("=" * 70)


if __name__ == "__main__":
    itens_atualizados = coletar_respostas(ITENS_VISTORIA)
    emitir_relatorio(itens_atualizados)