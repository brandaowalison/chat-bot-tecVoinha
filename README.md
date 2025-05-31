# Atividade de Assistente Virtual e Chatbot - Formação Tecnológica 4.0 - COMPET

Atividade proposta pelo professor de Assistente Virtual e Chatbot. Este repositório contém um projeto de um assistente virtual no Telegram especializado em tecnologia, feito em Python, com integração OpenAI, MongoDB e Redis.

## Funcionalidades
- **Atendimento personalizado:** O bot responde dúvidas sobre tecnologia, aplicativos, redes sociais e dicas do dia a dia.
- **Mini cadastro:** Solicita nome, idade, sexo e email do usuário e armazena no MongoDB.
- **Respostas inteligentes:** Utiliza a API OpenAI GPT-4o para gerar respostas naturais e contextualizadas.
- **Histórico de perguntas:** Armazena as últimas perguntas de cada usuário no Redis.

## Como usar
1. Inicie o bot no Telegram com `/start` ou `/iniciar`.
2. Faça o cadastro respondendo às perguntas (nome, idade, sexo, email).
3. Envie suas dúvidas sobre tecnologia!

## Requisitos
- Python 3.8+
- MongoDB (nuvem ou local)
- Upstash Redis
- Conta OpenAI (API Key)
- Bot Telegram (API Key)

## Instalação
1. Clone este repositório.
2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
3. Crie um arquivo `.env` com as variáveis:
   ```env
   MONGODB_URL=...
   TELEGRAM_API_KEY=...
   OPENAI_API_KEY=...
   REDIS_URL=...
   ```
4. Execute o bot:
   ```sh
   python bot_llm.py
   ```

## Estrutura
- `bot_llm.py` — Código principal do bot
- `requirements.txt` — Dependências do projeto
- `README.md` — Este arquivo


