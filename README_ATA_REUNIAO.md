# 📋 Gerador Automático de Atas de Reunião

Uma aplicação web que automatiza a geração de atas profissionais a partir de transcrições de reuniões usando **Azure OpenAI**.

## ✨ Características

✅ **Suporta múltiplos formatos** - DOCX, TXT, MD  
✅ **Fluxo em duas etapas** - Prompt 1 analisa, Prompt 2 estrutura o payload final  
✅ **Prévia analítica visível** - Permite revisar a saída da análise antes de gerar o DOCX  
✅ **JSON final editável** - Você pode corrigir campos antes da geração  
✅ **Preenchimento de template** - Integra dados em documento DOCX profissional  
✅ **Nomenclatura automática** - Nomes baseados em Cliente_Data_Hora  
✅ **Interface intuitiva** - Streamlit com upload de arquivos  
✅ **Integração com Azure OpenAI** - Usa o deployment configurado no seu ambiente

## 🚀 Como Usar

### Instalação

```bash
# Clonar ou navegar para o diretório
cd c:\Users\halex.amorim\generative-ai-for-beginners

# Instalar dependências (se não estiverem instaladas)
pip install streamlit python-docx openai python-dotenv

# Verificar que o .env está configurado com suas credenciais Azure
```

### Executar a Aplicação

```bash
streamlit run ata_reuniao_app.py
```

Abra o navegador em: `http://localhost:8501`

### Fluxo de Uso

#### **Passo 1: Prepare a Transcrição**

- **Exportar do Teams:**
  1. Acesse a reunião gravada no Teams
  2. Acesse o **Recap** ou exporte a transcrição
  3. Salve como `.docx` (como vem do Teams)

- **Ou converter áudio:**
  - Otter.ai
  - Google Transcribe
  - Microsoft Copilot
  - Veed.io

**Formatos suportados:** `.docx`, `.txt`, `.md`

#### **Passo 2: Carregue os Arquivos**

1. **Transcrição**: Clique em "Faça upload do arquivo de transcrição"
   - Aceita DOCX (do Teams), TXT ou MD
   - A IA extrai automaticamente o texto

2. **Template**: Clique em "Faça upload do template DOCX"
   - Use `EAS010-ATA-Template-v3.docx`

#### **Passo 3: Analise**

- Clique em **"1. Analisar transcrição"**
- Aguarde a execução de dois prompts:
  1. O Prompt 1 produz uma análise preliminar com evidências, lacunas e itens detectados
  2. O Prompt 2 converte essa análise em um JSON final normalizado para o documento
- Revise a análise e, se necessário, ajuste manualmente o JSON final

#### **Passo 4: Gere o documento**

- Clique em **"2. Gerar ata em DOCX"**
- O app tentará:
  1. Substituir placeholders explícitos do template
  2. Popular seções como Convocados, Pauta, Definições, Pendências e Plano de Ação
  3. Acrescentar um resumo gerado automaticamente se o template não tiver pontos de preenchimento compatíveis

#### **Passo 5: Baixe**

- Clique em **"⬇️ Baixar Ata (DOCX)"**
- Arquivo é salvo com nome: `Cliente_Data_Hora.docx`
- Exemplo: `Alimentos_Naturale_15-Jan-2026_09h00.docx`

## 📊 O que a IA Extrai

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| **Cliente** | Nome da empresa cliente | Senior Sistemas |
| **Projeto** | Nome e código do projeto | WMS - WMS001 |
| **Data/Hora** | Data e horário da reunião | 15-Jan-2026 / 09:00 |
| **Participantes** | Lista com nome, setor, ausências | João Silva \| TI \| Não |
| **Pauta** | Tópicos discutidos | Implementação WMS; Testes de carga; |
| **Definições** | Decisões e conclusões tomadas | Foi decidido usar banco PostgreSQL |
| **Pendências** | Tarefas com responsável e prazo | Setup do banco \| João \| 20-Jan-2026 |
| **Plano de Ação** | Ações futuras planejadas | Iniciar testes UAT \| Maria \| 25-Jan-2026 |

## 🎯 Arquivos Necessários

### 1. Transcrição da Reunião
```
Cliente: Senior Sistemas
Projeto: WMS - WMS001
Data: 15-Jan-2026
Participantes: João Silva (TI), Maria (Funcional), etc...
Conversa completa da reunião...
```

### 2. Template DOCX
Arquivo: `EAS010-ATA-Template-v3.docx`
- Contém placeholders em cinza
- Formatação profissional com logos e footer
- Tabelas dinâmicas para dados variáveis

## 💡 Dicas para Melhor Resultado

✅ **Transcrição completa** - Quanto mais detalhada, melhor  
✅ **Nomes completos** - Use nomes completos dos participantes  
✅ **Prazos claros** - Indique datas de conclusão  
✅ **Responsáveis definidos** - Atribua tarefas a pessoas específicas  
✅ **Contexto** - Mencione cliente e projeto explicitamente  
⚠️ **Édição manual** - Se algo não for reconhecido, edite depois no Word

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=sua_chave_aqui
AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

### Verificar Conexão

```bash
# Executar teste de conexão
python test_azure_connection.py
```

Resultado esperado:
```
✅ CONEXÃO BEM-SUCEDIDA!
Resposta do Azure OpenAI: Sim, estou funcionando!
```

## 📁 Estrutura de Arquivos

```
generative-ai-for-beginners/
├── ata_reuniao_app.py              # Aplicação Streamlit (PRINCIPAL)
├── test_azure_connection.py         # Teste de conexão
├── simple_chatbot.py                # Chatbot de exemplo
├── .env                             # Credenciais Azure (não commit)
└── requirements.txt                 # Dependências Python
```

## 🚨 Troubleshooting

### Nada foi preenchido no template
**Causa:** O template não usava placeholders compatíveis ou só tinha títulos de seção  
**Solução:** A nova versão tenta preencher tanto placeholders quanto o conteúdo abaixo de títulos como Convocados, Pauta e Definições. Se ainda assim não houver área compatível, o app adiciona uma seção final com o conteúdo gerado.

### O JSON final saiu incorreto
**Causa:** A transcrição tem ambiguidade ou informação faltante  
**Solução:** Revise a saída do Prompt 1, ajuste o JSON final no editor lateral da Etapa 2 e gere o DOCX novamente.

### Erro: "Connection refused"
**Causa:** Streamlit não consegue conectar ao Azure OpenAI  
**Solução:** Verifique `.env` com credenciais corretas

### Erro: "DOCX file cannot be read"
**Causa:** Arquivo DOCX corrompido ou formato inválido  
**Solução:** Re-exporte do Teams ou converta para TXT

### Resultado vazio
**Causa:** Transcrição muito curta ou sem informações estruturadas  
**Solução:** Adicione mais contexto na transcrição (cliente, projeto, nomes completos)

### Nome do arquivo está "Documento_00-Jan-0000_00h00"
**Causa:** IA não conseguiu extrair dados  
**Solução:** Verifique se transcrição contém cliente, data e hora

## 📈 Próximas Melhorias

- [ ] Suporte para upload em batch (múltiplas transcrições)
- [ ] Integração com OneDrive/SharePoint para salvar automaticamente
- [ ] Customização de template via UI
- [ ] Histórico de atas geradas
- [ ] Exportação para PDF além de DOCX

## 📞 Suporte

- **Documentação completa:** Ver arquivo `Prompts Copilot para Ata de Reunião Senior Sistema.md`
- **Conexão Azure:** Consulte `test_azure_connection.py`
- **Chatbot simples:** Experimente `simple_chatbot.py`

## 📄 Licença

Desenvolvido internamente para Senior Sistemas

---

**Versão:** 3.0  
**Última atualização:** 10-Mar-2026  
**Desenvolvido com:** Azure OpenAI + Streamlit + Python-Docx
