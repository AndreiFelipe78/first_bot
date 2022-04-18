from shutil import move
import telebot
from credencials import bot_token
from PIL import Image
import os


bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=["opcao1"])
def opcao1(mensagem):
    bot.reply_to(mensagem, "Por favor, envie a(s) foto(s) para a conversão. Ao finalizar, use o comando /gerar_pdf")
    @bot.message_handler(content_types='photo')
    def image_downloader(mensagem):
        raw = mensagem.photo[2].file_id
        path = raw+".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(path,'wb') as new_file:
            new_file.write(downloaded_file)   
        original = '/app/{}'.format(path)
        target = '/app/pictures/'
        move(original,target)
@bot.message_handler(commands=["gerar_pdf"])
def gerar_pdf(mensagem):
    dir = '/app/pictures/'
    file_names = os.listdir(dir)
    if len(file_names) == 0:
        bot.send_message(mensagem.chat.id, "Olhei aqui e acho que você não enviou nenhuma foto {}. \nPreciso de ovos para fazer omelete. \nEnvie as fotos e pressione /gerar_pdf".format(mensagem.chat.first_name))
    else:
        photo_list = []
        photo_rgb = []
        for photo in file_names:
            photo_list.append(Image.open(r'/app/pictures/{}'.format(photo)))
        for item in photo_list:
            photo_rgb.append(item.convert('RGB'))
        photo_rgb[0].save(r'{}my_file.pdf'.format(dir), save_all=True, append_images=photo_rgb)
        bot.send_message(mensagem.chat.id, 'Gerando PDF...')
        bot.send_document(mensagem.chat.id, document=open('/app/pictures/my_file.pdf', 'rb'))
        bot.send_message(mensagem.chat.id, 'As fotos enviadas e os dados gerados serão apagados agora.')
        file_names = os.listdir(dir)
        for item in file_names:
            os.remove('{}{}'.format(dir,str(item)))


@bot.message_handler(commands=["opcao2"])
def opcao2(mensagem):
    bot.send_message(mensagem.chat.id, 'Para enviar sugestão/reclamação, utilize \nemail: andreifelipe78@gmail.com \nGithub https://github.com/AndreiFelipe78 ')


@bot.message_handler(content_types='text')
def resposta_padrao(mensagem):
    bot.send_message(mensagem.chat.id, 'Welcome {}. How you doing today?.'.format(mensagem.chat.first_name))
    texto = """
    Escolha um opção para continuar (clique no item):\n
    /opcao1 conversor de foto para PDF\n
    /opcao2 Fazer reclamação/sugestão\n
    \n
    Responder qualquer outra coisa não vai funcionar, clique em uma das opções acima."""
    bot.send_message(mensagem.chat.id, texto)



bot.polling()
