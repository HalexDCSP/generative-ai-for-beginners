#!/usr/bin/env python3
"""
Chatbot Simples com Azure OpenAI
Você digita, a IA responde!
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Carregar variáveis do .env
load_dotenv()

# Criar cliente
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

print("=" * 60)
print("CHATBOT COM AZURE OPENAI")
print("=" * 60)
print("Digite suas perguntas (ou 'sair' para encerrar)")
print("=" * 60 + "\n")

# Histórico de mensagens para manter contexto da conversa
messages = [
    {"role": "system", "content": "Você é um assistente amigável e prestativo que responde em português."}
]

while True:
    # Pedir input do usuário
    user_input = input("\nVocê: ").strip()
    
    # Se o usuário digitar 'sair', encerrar
    if user_input.lower() == 'sair':
        print("\nAdeus! 👋")
        break
    
    # Se estiver vazio, ignorar
    if not user_input:
        continue
    
    # Adicionar mensagem do usuário ao histórico
    messages.append({"role": "user", "content": user_input})
    
    try:
        # Chamar a API
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            max_tokens=500
        )
        
        # Pegar a resposta
        assistant_message = response.choices[0].message.content
        
        # Adicionar resposta ao histórico
        messages.append({"role": "assistant", "content": assistant_message})
        
        # Mostrar resposta
        print(f"\nIA: {assistant_message}")
        
    except Exception as e:
        print(f"\n❌ Erro na chamada da API: {e}")
        # Remover a mensagem do usuário se houve erro
        messages.pop()
