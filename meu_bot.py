
from shutil import move
import telebot
from telebot import types
from credencials import chave_API
from PIL import Image


bot = telebot.TeleBot(chave_API)

@bot.message_handler(commands=["opcao1"])
def opcao1(mensagem):
    pass

@bot.message_handler(commands=["opcao2"])
def opcao2(mensagem):
    bot.send_message(mensagem.chat.id, 'Para enviar a reclamação, utilize o email: andreifelipe78@gmail.com \n ou o meu github https://github.com/AndreiFelipe78 ')

@bot.message_handler(commands=["opcao3"])
def opcao3(mensagem):
    bot.reply_to(mensagem, "Por favor, envie a(s) foto(s) para a conversão. Ao finalizar use o comando /gerar_pdf")

@bot.message_handler(content_types='text')
def resposta_padrao(mensagem):
    bot.send_message(mensagem.chat.id, 'Welcome {}. How you doing today?.'.format(mensagem.chat.first_name))
    texto = """
    Escolha um opção para continuar (clique no item):\n
    /opcao1 Fazer checklist\n
    /opcao2 Fazer reclamação/sugestão\n
    /opcao3 conversor de foto para PDF \n
    Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(content_types='photo')
def image_converter(mensagem):
    raw = mensagem.photo[2].file_id
    path = raw+".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path,'wb') as new_file:
        new_file.write(downloaded_file)   
    original = '/home/andrei/Documents/new_bot/{}'.format(path)
    target = '/home/andrei/Documents/new_bot/pictures/'
    move(original,target)
    original = '{}'.format(path)

    image_1 = Image.open(r'{}'.format(str(original)))
    im_1 = image_1.convert('RGB')
    im_1.save(r'{}'.format(target+raw+'.pdf'))
    
bot.polling()



# para responder um mensagem diretamente
# bot.send_message(mensagem.chat.id, <resposta desejada>)