"""
Construcao e formatacao do dataset de suporte (Capitulo 9).
Na pratica real, substitua a lista embutida por centenas de exemplos
reais e anonimizados lidos de um arquivo .jsonl no disco.
Requisitos: pip install datasets
"""

from datasets import Dataset

# Amostra ilustrativa no padrao da equipe de suporte interno
# REGRA DO LIVRO: todas as respostas seguem o mesmo esqueleto
# "Diagnostico / Acao / Observacoes" — consistencia rigida.
dados_suporte = [
    {
        "instrucao": "O servidor de arquivos storage01 parou de responder na porta 445 e o trafego de rede zerou.",
        "resposta": "Diagnóstico: Queda no serviço SMB ou falha de interface no host storage01.\nAção: Reiniciar o daemon smbd via console física e verificar integridade da interface eth0.\nObservações: Não forçar reboot do hardware sem antes validar o status do array RAID."
    },
    {
        "instrucao": "Alerta de uso de disco: particao /var/log no servidor db-replica atingiu 98% da capacidade.",
        "resposta": "Diagnóstico: Esgotamento iminente de armazenamento por acúmulo de logs operacionais.\nAção: Executar script de expurgo de rotinas antigas e truncar arquivos de log arquivados.\nObservações: Validar se o logrotate está habilitado no cron diário para evitar reincidência."
    },
    {
        "instrucao": "Usuarios relatam erro de autenticacao intermitente ao acessar a VPN corporativa.",
        "resposta": "Diagnóstico: Timeout de comunicação entre o concentrador VPN e o serviço LDAP.\nAção: Reiniciar o conector de sincronização de identidade e monitorar a fila de sockets.\nObservações: Verificar se houve alteração recente nas rotas de firewall do datacenter."
    }
]


def formatar_para_treino(exemplos):
    """Empacota as instrucoes no formato de mensagens com papeis definidos."""
    conversas_formatadas = []

    for instrucao, resposta in zip(exemplos["instrucao"], exemplos["resposta"]):
        mensagens = [
            {
                "role": "system",
                "content": "Você é o especialista de triagem de infraestrutura da empresa. Suas respostas devem conter estritamente os campos Diagnóstico, Ação e Observações."
            },
            {"role": "user", "content": instrucao},
            {"role": "assistant", "content": resposta}
        ]
        conversas_formatadas.append(mensagens)

    return {"mensagens": conversas_formatadas}


if __name__ == "__main__":
    dataset_bruto = Dataset.from_dict({
        "instrucao": [d["instrucao"] for d in dados_suporte],
        "resposta": [d["resposta"] for d in dados_suporte]
    })

    dataset_pronto = dataset_bruto.map(formatar_para_treino, batched=True)
    print(f"Dataset processado com sucesso: {len(dataset_pronto)} exemplos estruturados.")
    dataset_pronto.save_to_disk("dataset_suporte")