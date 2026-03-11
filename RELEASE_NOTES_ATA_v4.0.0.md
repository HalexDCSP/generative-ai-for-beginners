# Release Notes - v4.0.0-ata-senior-gpt53

Data: 2026-03-11

## Objetivo
Automatizar a geracao de atas com qualidade de preenchimento, fluxo revisavel e compatibilidade com deployment GPT-5.3-chat no Azure OpenAI.

## Escopo entregue
- App Streamlit com fluxo em duas etapas (pre-ata e gravacao no template).
- Prompt 1 alinhado ao formato oficial v4 para extracao estruturada.
- Prompt 2 oficial disponivel no app para uso no Copilot Word.
- Preenchimento deterministico do template EAS010-ATA-Template-v3.
- Tabelas dinamicas para Convocados, Pendencias e Plano de Acao.
- Aplicacao de estilo de dados (Calibri 11, preto, sem negrito).
- Nomeacao automatica do arquivo final no padrao Cliente_Data_Hora.docx.
- Compatibilidade com GPT-5.3-chat (uso de max_completion_tokens e parametros suportados).

## Arquivos principais
- ata_reuniao_app.py
- ata_reuniao_core.py
- test_ata_reuniao_core.py
- test_azure_connection.py
- app_completo.py
- README_ATA_REUNIAO.md
- GUIA_CONFIGURACAO.md

## Validacoes executadas
- Teste de conexao Azure OpenAI com sucesso.
- Suite local de testes de nucleo em verde.
- Compilacao Python dos arquivos alterados sem erros.
- App Streamlit ativo e respondendo via HTTP local.

## Observacoes de governanca
- O commit desta release esta no fork do usuario.
- O push para o repositorio upstream da Microsoft depende de permissao (403 esperado sem write access).
- Recomendado abrir PR do fork para upstream se desejado.
