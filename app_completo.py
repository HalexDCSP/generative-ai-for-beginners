#!/usr/bin/env python3
"""
App completo: Chat IA + Gera resumo + Envia para Teams
"""

import os
import requests
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# Criar cliente Azure
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

print("=" * 60)
print("APP COMPLETO: CHAT + TEAMS")
print("=" * 60)

# Guardar o histórico da conversa
conversation_history = []

def chatbot(user_message):
    """Função que envia mensagem para IA e recebe resposta"""
    try:
        # Adicionar mensagem do usuário
        conversation_history.append({
            "role": "user", 
            "content": user_message
        })
        
        # Chamar Azure OpenAI
        response = client.chat.completions.create(
            model=deployment,
            messages=conversation_history,
            max_completion_tokens=300
        )
        
        # Pegar resposta
        ai_response = response.choices[0].message.content
        
        # Guardar resposta no histórico
        conversation_history.append({
            "role": "assistant", 
            "content": ai_response
        })
        
        return ai_response
        
    except Exception as e:
        return f"Erro: {e}"


def send_to_teams(message, webhook_url):
    """Envia uma mensagem para o Teams"""
    try:
        payload = {"text": message}
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code in [200, 202]:
            return "✅ Enviado para Teams com sucesso!"
        else:
            return f"❌ Erro ao enviar: {response.status_code}"
            
    except Exception as e:
        return f"❌ Erro: {e}"


# MENU PRINCIPAL
print("\nOpcões:")
print("1. Conversar com a IA")
print("2. Gerar resumo da conversa e enviar para Teams")
print("3. Sair")

while True:
    choice = input("\nEscolha uma opção (1-3): ").strip()
    
    if choice == "1":
        user_input = input("Você diz: ").strip()
        if user_input:
            response = chatbot(user_input)
            print(f"IA: {response}\n")
    
    elif choice == "2":
        if not conversation_history:
            print("Nenhuma conversa ainda!\n")
        else:
            # Gerar resumo
            print("⏳ Gerando resumo...")
            resume_prompt = "Faça um resumo breve (2-3 linhas) da conversa anterior:"
            resume = chatbot(resume_prompt)
            
            # Perguntar URL do Teams
            webhook = input("Cole a URL do webhook do Teams: ").strip()
            
            # Enviar
            result = send_to_teams(f"📄 Resumo da Conversa:\n{resume}", webhook)
            print(result)
    
    elif choice == "3":
        print("Até logo! 👋\n")
        break
    
    else:
        print("Opção inválida!")
