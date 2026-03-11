#!/usr/bin/env python3
"""
Script de teste: Verifica se está conectado ao Azure OpenAI
Este script é MUITO simples - só testa a conexão!
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Carregar variáveis do arquivo .env
load_dotenv()

print("=" * 60)
print("TESTANDO CONEXÃO COM AZURE OPENAI")
print("=" * 60)

# Pegar as credenciais do .env
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

print(f"\n✓ Chave da API: {api_key[:20]}...***")
print(f"✓ Endpoint: {endpoint}")
print(f"✓ Deployment: {deployment}")
print(f"✓ Versão API: {api_version}")

try:
    # Criar cliente Azure OpenAI
    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )
    
    print("\n🔄 Enviando teste de mensagem para o Azure OpenAI...")
    
    # Fazer uma chamada simples
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "user", "content": "Responda em uma frase: Você está funcionando?"}
        ],
        max_completion_tokens=50
    )
    
    # Se chegou aqui, funcionou!
    print("\n✅ CONEXÃO BEM-SUCEDIDA!")
    print(f"\nResposta do Azure OpenAI:")
    print(f"{response.choices[0].message.content}")
    print("\n" + "=" * 60)
    print("ÓTIMO! Você está pronto para usar as funcionalidades!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    print("\nVerifique:")
    print("1. A chave da API está correta?")
    print("2. O endpoint está correto?")
    print("3. Sua conexão com a internet está funcionando?")
