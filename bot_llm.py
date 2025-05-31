import telebot
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_API_KEY)

client = OpenAI(api_key=OPENAI_API_KEY)

redis_client = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

INSTRUÇÃO_SISTEMA = (
    "Você é uma assistente virtual especializada em tecnologia, chamada 'Tec Voinha'. "
    "Sua função é exclusivamente fornecer informações úteis, práticas e detalhadas sobre temas relacionados à tecnologia. "
    "Você pode ajudar com dúvidas sobre o uso de aplicativos como WhatsApp, redes sociais, dicas de tecnologia do dia a dia, história da tecnologia, "
    "e instruções sobre como instalar ou utilizar aplicativos. "
    "Caso o usuário faça perguntas que não estejam relacionadas a tecnologia (como programação avançada, matemática, política ou qualquer outro tema fora do seu escopo), "
    "recuse educadamente a resposta. Apresente-se novamente como uma assistente voltada para apoio tecnológico e incentive o usuário a fazer uma pergunta relacionada à tecnologia."
)

response = client.chat.completions.create(
    modal='gpt-4o',
    message=[
        {"role": "system", "content": INSTRUÇÃO_SISTEMA},
    ]
)

@bot.message_handler(commands=["start","Iniciar"])
def send_welcome(message):
    welcome_text = (
        "Olá! Eu sou a Assistente Tec Voinha 🤖\n\n"
        "Estou aqui para ajudar você com tudo que envolve tecnologia — dicas, truques, informações e muito mais.\n\n"
        "Fique à vontade para perguntar!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_question = message.text
    chat_id = message.chat.id

    bot.send_chat_action(chat_id, 'typing')

    try:
        response = modal.generate_content(user_question)

        bot.reply_to(message, response.text)