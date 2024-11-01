# 1 - Libraries
import openai
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from config import OPENAI_API_KEY
from remove import remove
import schedule
import time
import pytz
from datetime import datetime
from pytz import timezone
import threading
import json
import random

# 2 - Configuration
client = openai.OpenAI()
name_bot = 'Lara'
name_profesional = 'Dra. Joana'
years_bot = '25'
country_bot = 'Brasil'
firm_bot = 'Hdrs Servicos Medicos S/S'
idiom_bot = 'Portugues Brasil'

startconversation_bot = (
    f'Olá, obrigada por entrar em contato 😊. Meu nome é {name_bot}, e faço parte da equipe da {name_profesional}. '
    'Será um prazer te atender hoje. Qual o seu nome? Como posso lhe servir hoje?'
)
end_conversation_bot = 'Qualquer dúvida até lá, estamos à disposição. Tenha um ótimo dia!'

product_bot = {
    "service_1": {
        "descrição": "Consulta médica nutrologia pediátrica para crianças de 0 a 15 anos.",
        "preço": "R$500",
        "desconto": "15% de desconto para 2 ou mais filhos"
    }
}

educacao = (
    f'A {name_profesional}, formada em pediatria e nutrologia...'
)

endereco = 'São Paulo'
atendimento = 'Presencial '
formas_pagamento = 'Pix, cartão de débito/crédito, parcelado em até 2 vezes sem juros'
tipo_atendimento = 'Consulta particular, com nota fiscal para reembolso pelo convênio'
tempo_consulta = '60 minutos'
nota_fiscal = '1 nota fiscal por cada serviço'
link_agendamento = 'link'
mensagem_encerramento = (
    'Obrigado por utilizar o bots'
)

# 3 - Context
contexto = (
    f" Contexto:\n"
    f" - Serviços: {product_bot}.\n"
    f" - Formação da {name_profesional}: {educacao}.\n"
    f" - Endereço: {endereco}.\n"
    f" - Forma de atendimento: {atendimento}.\n"
    f" - Agendamento: {link_agendamento}.\n"
    f" - Tipo de atendimento: {tipo_atendimento}.\n"
    f" - Forma de pagamento: {formas_pagamento}.\n"
    f" - Tempo da consulta: {tempo_consulta}.\n"
    f" - Emissão de Nota Fiscal: {nota_fiscal}.\n"
    " Instruções Adicionais:\n"
    " - Em caso de dúvidas, sinta-se à vontade para pedir esclarecimentos de forma gentil.\n"
    " - Mantenha uma linguagem acolhedora e amigável, com um tom positivo."
)

# 4 - Storage for User Conversations
user_conversations = {}
message_count = {}
limit_conversation = 20
removes = remove()

# Function to save user conversations
def save_conversations():
    timezone = pytz.timezone('America/Sao_Paulo')
    current_time = datetime.now(timezone)
    formatted_date = current_time.strftime('%d%m%Y')
    filename = f"/home/linoccm/03_bo_API_linux/env_bo_API_linux/chatbots_whatsapp_APIOFFICIAL/output/conver_{formatted_date}.json"
    try:
        with open(filename, 'w') as file:
            json.dump(user_conversations, file, indent=4)
        print("User conversations saved to", filename)
    except Exception as e:
        print("Error saving conversations:", e)
    finally:
        user_conversations.clear()

# Thread for Scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute

schedule.every().day.at("01:00", "America/Sao_Paulo").do(save_conversations)
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# 5 - Flask Application for Chatbot Interaction
app = Flask(__name__)

@app.route('/chatgpt', methods=['POST'])
def gpt():
    global user_conversations, removes, message_count

    # 5.1 Get incoming message from WhatsApp
    incoming_msg = request.values.get('Body', '').lower()
    sender_id = request.values.get('From', '')

    print("Question: ", incoming_msg)

    # 5.2 Count messages per user
    message_count[sender_id] = message_count.get(sender_id, 0) + 1

    # 5.3 Handle removal condition
    if sender_id in removes:
        send_message(" ")

    # 5.4 Initialize conversation for new users or retrieve existing conversation
    else:
        conversation = user_conversations.get(sender_id, [
            {"role": "system", "content": contexto},
            {"role": "user", "content": "Oi, tudo bem?"},
            {"role": "assistant", "content": startconversation_bot}
        ])

        conversation.append({"role": "user", "content": incoming_msg})

        # Check conversation limit
        if message_count[sender_id] < limit_conversation:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=conversation,
                temperature=0.7,
                max_tokens=200,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1,
                stop=["4.", "5.", "6."]
            )

            response_content = response.choices[0].message.content
            conversation.append({"role": "assistant", "content": response_content})
            conversation = conversation[:7] + conversation[-10:]
            user_conversations[sender_id] = conversation

            print("\nResponse: ", response_content, "\n")
            time.sleep(random.uniform(1, 4))

            bot_resp = MessagingResponse()
            msg = bot_resp.message()
            msg.body(response_content)
            return str(bot_resp)
        else:
            send_message(mensagem_encerramento)

# Start the Flask app
if __name__ == '__main__':
    app.run(host='x.x.x.x', debug=True, port=xxxx)  
