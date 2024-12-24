# Bot de Newsletter para Telegram

[Bot do Telegram](https://t.me/FDNewsletter_bot)

[Site do Filipe Deschamps](https://filipedeschamps.com.br/newsletter)

Este projeto é um bot desenvolvido para o Telegram que acessa uma conta de email, busca por newsletters específicas e envia o conteúdo dessas newsletters para um chat do Telegram. O bot utiliza a API do Telegram e o protocolo IMAP para acessar emails.

Este projeto foi desenvolvido com o intuito de facilitar o acesso a Newsletter do Filipe Deschamps, já que sua caixa de entrada pode estar muito cheia.

## Funcionalidades

- **Receber Newsletter**: O bot acessa a conta de email configurada e busca por mensagens de um remetente específico (ex: `newsletter@filipedeschamps.com.br`).
- **Extrair Conteúdo**: O conteúdo dos emails é extraído, processado e formatado para ser enviado ao Telegram.
- **Envio para o Telegram**: O conteúdo do email é enviado para o Telegram em partes, respeitando o limite de caracteres do Telegram (4096 caracteres).
- **Escapando Markdown**: O bot formata o conteúdo utilizando MarkdownV2, escapando caracteres especiais que poderiam gerar erros ao enviar a mensagem.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `telebot` (para interagir com a API do Telegram)
  - `imaplib` (para acessar emails via IMAP)
  - `beautifulsoup4` (para processar conteúdo HTML)
  - `python-dotenv` (para carregar variáveis de ambiente de um arquivo `.env`)
- configurar o email e senha tanto no site da Newsletter quanto no código

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/bot-newsletter-telegram.git
   cd bot-newsletter-telegram
