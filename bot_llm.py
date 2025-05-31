import telebot
from openai import OpenAI
import os
from dotenv import load_dotenv
from upstash_redis import Redis

load_dotenv()

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
REDIS_URL= os.getenv("REDIS_URL")

bot = telebot.TeleBot(TELEGRAM_API_KEY)

client = OpenAI(api_key=OPENAI_API_KEY)

redis = Redis(url="https://correct-grub-25673.upstash.io", token=REDIS_URL)
redis.set("foo", "bar")
value = redis.get("foo")

INSTRUÇÃO_SISTEMA = (
    "Você é um assistente virtual especializado em tecnologia, chamado 'Mundo Conectado.' "
    "Sua função é exclusivamente fornecer informações úteis, práticas e detalhadas sobre temas relacionados à tecnologia. "
    "Você pode ajudar com dúvidas sobre o uso de aplicativos como WhatsApp, redes sociais, dicas de tecnologia do dia a dia, história da tecnologia, "
    "e instruções sobre como instalar ou utilizar aplicativos. "
    "Caso o usuário faça perguntas que não estejam relacionadas a tecnologia (como programação avançada, matemática, política ou qualquer outro tema fora do seu escopo), "
    "recuse educadamente a resposta. Apresente-se novamente como uma assistente voltada para apoio tecnológico e incentive o usuário a fazer uma pergunta relacionada à tecnologia."
)

@bot.message_handler(commands=["start","Iniciar"])
def send_welcome(message):
    welcome_text = (
        "Olá! Eu sou o Assistente Mundo Conectado 🤖\n\n"
        "Estou aqui para ajudar você com tudo que envolve tecnologia — dicas, truques, informações e muito mais.\n\n"
        "Fique à vontade para perguntar!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_question = message.text
    chat_id = message.chat.id

    redis.lpush(f"historico:{chat_id}", user_question)

    bot.send_chat_action(chat_id, 'typing')

    try:
        completion = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {"role": "system", "content": INSTRUÇÃO_SISTEMA},
                {"role": "user", "content": user_question}
            ]
        )
        resposta = completion.choices[0].message.content
        bot.reply_to(message, resposta)
    
    except Exception as e:
        print(f"Erro ao chamar API do OpenAI: {e}")
        error_message = (
            "Desculpe, não consegui processar sua pergunta no momento."
            "Por favor, tente novamente mais tarde."
        )
        bot.reply_to(message, error_message)



print("Bot de Mundo Conectado...")
bot.polling()