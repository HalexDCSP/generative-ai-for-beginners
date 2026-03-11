import requests
import sys

if len(sys.argv) < 2:
    print("Uso: python send_teams_message.py <webhook_url> [message]")
    sys.exit(1)

webhook_url = sys.argv[1]
message = sys.argv[2] if len(sys.argv) > 2 else "Olá, esta é uma mensagem básica enviada via Power Automate!"

payload = {
    "text": message
}

response = requests.post(webhook_url, json=payload)

if response.status_code in [200, 202]:
    print("Mensagem enviada com sucesso!")
    print(f"Mensagem: {message}")
else:
    print(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")