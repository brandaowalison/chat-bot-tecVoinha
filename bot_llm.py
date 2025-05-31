import telebot
from openai import OpenAI
import os
from dotenv import load_dotenv
from upstash_redis import Redis
from pymongo import MongoClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
REDIS_URL= os.getenv("REDIS_URL")

bot = telebot.TeleBot(TELEGRAM_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)
redis = Redis(url="https://correct-grub-25673.upstash.io", token=REDIS_URL)
redis.set("foo", "bar")
value = redis.get("foo")
mongo_client = MongoClient(MONGODB_URL)
db = mongo_client["bot_db"]
usuarios = db["usuarios"]

INSTRUÇÃO_SISTEMA = (
    "Olá! Eu sou o 'Mundo Conectado', seu assistente virtual especializado em tecnologia!"
    "Estou aqui para te ajudar com informações úteis e práticas sobre o mundo da tecnologia."
    "Posso tirar suas dúvidas sobre como usar aplicativos como WhatsApp e redes sociais, dar dicas de tecnologia para o seu dia a dia, contar um pouco da história da tecnologia,"
    "e te dar instruções sobre como instalar ou utilizar diversos aplicativos."
    "Se você tiver alguma pergunta que não seja sobre tecnologia (como programação avançada, matemática, política, etc.), com licença, mas não poderei responder."
    "Sou um assistente focado em apoio tecnológico. Pode me perguntar algo sobre tecnologia?"
    "Não usarei formatação Markdown, responderei em texto normal."
)

@bot.message_handler(commands=["Start","Iniciar"])
def iniciar_conversa(message):
    inicio_text = (
        "Olá! Eu sou o Assistente Mundo Conectado 🤖\n\n"
        "Estou aqui para ajudar você com tudo que envolve tecnologia — dicas, truques, informações e muito mais.\n\n"
        "Fique à vontade para perguntar!"
    )
    bot.reply_to(message, inicio_text)

def registrar_usuario(chat_id, message):
    user = usuarios.find_one({"chat_id": chat_id})
    if user:
        return user["nome"]
    else:
        bot.reply_to(message, "Qual é o seu nome?")
        bot.register_next_step_handler(message, mensagem_idade)
        return None

def mensagem_idade(message):
    chat_id = message.chat.id
    nome = message.text
    bot.reply_to(message, "Qual é a sua idade?")
    bot.register_next_step_handler(message, mensagem_sexo, nome)

def mensagem_sexo(message, nome,):
    chat_id = message.chat.id
    idade = message.text
    bot.reply_to(message, "Qual é o seu sexo?")
    bot.register_next_step_handler(message, mensagem_email, nome, idade)

def mensagem_email(message, nome, idade,):
    chat_id = message.chat.id
    sexo = message.text
    bot.reply_to(message, "Qual é o seu email?")
    bot.register_next_step_handler(message, salvar_cadastro, nome, idade, sexo)

def salvar_cadastro(message, nome, idade, sexo, *args):
    chat_id = message.chat.id
    email = message.text
    usuarios.insert_one({
        "chat_id": chat_id,
        "nome": nome,
        "idade": idade,
        "sexo": sexo,
        "email": email
    })
    bot.reply_to(message, f"Prontinho, {nome}! Seu cadastro foi concluído com sucesso. 😊 Agora é só me perguntar o que você gostaria de saber sobre tecnologia!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_question = message.text
    chat_id = message.chat.id

    nome = registrar_usuario(chat_id, message)
    if not nome:
        return

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
        bot.reply_to(message, f"{nome}, {resposta}")
    
    except Exception as e:
        print(f"Erro ao chamar API do OpenAI: {e}")
        error_message = (
            "Desculpe, não consegui processar sua pergunta no momento."
            "Por favor, tente novamente mais tarde."
        )
        bot.reply_to(message, error_message)

print("Bot de Mundo Conectado...")
bot.polling()