import telebot
import imaplib
from bs4 import BeautifulSoup
import os
import email
from email.header import decode_header  # Importando a função para decodificar o título

BOT_KEY = "7614138298:AAH6182fESdtShEPL42K4SE-qqImp0EsZZc"

EMAIL = "newsletterbot01@gmail.com" 
SENHA = "znpy uvwk jzvc kpum"

bot = telebot.TeleBot(BOT_KEY)

def buscar_email():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, SENHA)
        mail.select("inbox")

        status, data = mail.search(None, '(FROM "newsletter@filipedeschamps.com.br")')
        email_ids = data[0].split()
        if not email_ids:
            return None

        status, data = mail.fetch(email_ids[-1], "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        return msg
    except Exception as e:
        print(f"Erro ao buscar email: {e}")
        return None

def processar_email(msg):
    try:
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    return part.get_payload(decode=True).decode(), "text/plain"
                elif content_type == "text/html":
                    return part.get_payload(decode=True).decode(), "text/html"
        else:
            content_type = msg.get_content_type()
            return msg.get_payload(decode=True).decode(), content_type
    except Exception as e:
        print(f"Erro ao processar email: {e}")
        return None, None

def extrair_texto_html(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()
    except Exception as e:
        print(f"Erro ao extrair texto do HTML: {e}")
        return "Erro ao processar conteúdo HTML."

def escapar_markdown(texto):
    caracteres_especiais = r"*_[]()~>#+-=|{}.!"
    for char in caracteres_especiais:
        texto = texto.replace(char, f"\\{char}")
    return texto

def formatar_texto(texto, tipo):
    try:
        if tipo == "text/html":
            return texto
        
        texto_formatado = texto.replace('*', '')
        
        texto_formatado = escapar_markdown(texto_formatado)
        
        return texto_formatado
    except Exception as e:
        print(f"Erro ao formatar texto: {e}")
        return "Erro ao formatar o conteúdo do email."

def dividir_mensagem(conteudo, limite=4096):
    return [conteudo[i:i+limite] for i in range(0, len(conteudo), limite)]

def enviar_para_telegram(conteudo, chat_id):
    try:
        partes = dividir_mensagem(conteudo)
        for parte in partes:
            bot.send_message(chat_id=chat_id, text=parte, parse_mode='MarkdownV2')
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Telegram: {e}")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Bem Vindo à NewsLetter!")

    msg = buscar_email()
    if msg:
        titulo, encoding = decode_header(msg["Subject"])[0]
        if isinstance(titulo, bytes):
            titulo = titulo.decode(encoding or 'utf-8')
        bot.send_message(chat_id, f"{titulo}", parse_mode='MarkdownV2')

        conteudo, tipo = processar_email(msg)
        if conteudo:
            mensagem_formatada = formatar_texto(conteudo, tipo)
            enviar_para_telegram(mensagem_formatada, chat_id)
        else:
            bot.send_message(chat_id, "Não foi possível processar o conteúdo do email.", parse_mode='MarkdownV2')
    else:
        bot.send_message(chat_id, escapar_markdown("Nenhum Atualização Encontrada."), parse_mode='MarkdownV2')


bot.polling()
