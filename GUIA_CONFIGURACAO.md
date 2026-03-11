# 🚀 GUIA RÁPIDO: Configuração Azure OpenAI para Dummies

## O que você tem até agora:

✅ **3 scripts prontos para usar:**
1. `test_azure_connection.py` - Testa se conecta ao Azure
2. `simple_chatbot.py` - Um chatbot interativo
3. `app_completo.py` - Chat + gera resumo + envia para Teams

✅ **.env configurado** com suas credenciais

---

## ⚠️ ERRO: 401 Access Denied

**Isso significa:**
- A chave da API (AZURE_OPENAI_API_KEY) está **errada ou expirada**
- OU o endpoint (AZURE_OPENAI_ENDPOINT) está **errado**

---

## ✅ Como resolver:

### Opção 1: Verificar no Portal do Azure
1. Acesse: https://portal.azure.com/
2. Procure por "Azure OpenAI" na barra de cima
3. Clique no seu recurso "halex-openai-agent"
4. No lado esquerdo, clique em **"Keys and Endpoint"**
5. Você vai ver:
   - **key1** e **key2** (escolha qualquer uma)
   - **Endpoint** (será algo como `https://halex-openai-agent.openai.azure.com/`)
6. Copie a **key1** e o **Endpoint**
7. Edite o arquivo `.env` e substitua:
   - `AZURE_OPENAI_API_KEY` = sua chave
   - `AZURE_OPENAI_ENDPOINT` = seu endpoint

### Opção 2: Verificar se a chave expirou
Se a chave está correta, pode ter expirado! Regenere:
1. No portal, em "Keys and Endpoint"
2. Clique em "Regenerate key1"
3. Copie a nova chave para o `.env`

---

## 📋 Checklist para tudo funcionar:

- [ ] Chave da API está no `.env`? ✓
- [ ] Endpoint está no `.env`? ✓
- [ ] Deployment é "gpt-35-turbo"? ✓
- [ ] A chave não está expirada? ← **Verifique isso!**
- [ ] Você tem conexão com internet? ✓

---

## 🎯 Próximos passos:

Depois de corrigir o `.env`:

```bash
# Teste novamente
python test_azure_connection.py

# Se funcionar, use o chatbot:
python simple_chatbot.py

# Para a app completa:
python app_completo.py
```

---

## 🎓 O que cada script faz:

| Script | Função | Como usar |
|--------|--------|-----------|
| `test_azure_connection.py` | Testa se conecta ao Azure | `python test_azure_connection.py` |
| `simple_chatbot.py` | Chat simples | `python simple_chatbot.py`<br>Digite suas perguntas |
| `app_completo.py` | Chat + Teams | `python app_completo.py`<br>Escolha opção 1 ou 2 |
| `send_teams_message.py` | Envia msg para Teams | `python send_teams_message.py <webhook>` |

---

## 💡 Dicas importantes:

1. **Nunca compartilhe sua chave de API!** (já está no `.env` que é seguro)
2. **Se der qualquer erro**, verifique se o `.env` tem as credenciais CORRIGIDAS
3. **Espaços em branco podem quebrar!** Se copiar/colar, verifique se não deixou espaços antes/depois

---

## ❓ Perguntas frequentes:

**P: A chave foi aceita, mas diz "Access Denied"?**
R: A chave pode ter expirado. Regenere no portal Azure.

**P: Como vejo meu deployment?**
R: `python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('AZURE_OPENAI_DEPLOYMENT'))"`

**P: Posso usar para gerar imagens?**
R: Sim! Você precisa fazer deploy de um modelo DALL-E e trocar o deployment, mas o chatbot com gpt-35-turbo já deve funcionar!

---

**Próximo passo: Corrija a chave/endpoint e rode novamente! 🚀**
