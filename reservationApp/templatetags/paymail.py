# -*- coding: cp1251 -*-
import smtplib
import img2pdf
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
import qrcode
from PyPDF2 import *
from PIL import Image


def pqr(code):
    data = code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.jpg")
    # Открываем изображени
    background = Image.open("media/default/2.png")
    overlay = Image.open("qrcode.jpg")

    width, height = overlay.size
    new_width = int(width * 0.6)
    new_height = int(height * 0.6)
    overlay = overlay.resize((new_width, new_height))

    # Наложение одной картинки на другую
    background.paste(overlay, (71, 273), overlay)

    # Сохраняем результат
    background.save("output.png")

def mkpdf(code,avtonum,date,name,seats,summa):
    # Создаем объект PDF
    pdf = FPDF('L', 'mm', 'A4')

    # Добавляем новую страницу
    pdf.add_page()
    background = Image.open("media/default/2.png")
    width, height = background.size
    # Вставляем изображение
    pdf.image('output.png',-8, -10, width*0.35, height*0.4)  # параметры: путь к изображению, x, y, ширина, высота
    pdf.add_font('DejaVu','','media/default/DejaVuSansCondensed-Bold.ttf', uni=True)
    pdf.set_font('DejaVu', '',12)
    text = code
    text1 = avtonum
    text2 = date
    text3 = name
    n=65
    h=15
    text4 = f'{seats}'
    text5 = f'{summa}'
    pdf.cell(210, h, txt=' '*n + 'Номер билета: '+text, ln=1, align="L")
    pdf.cell(210, h, txt=' '*n + 'Номер автобуса: '+text1, ln=1, align="L")
    pdf.cell(210, h, txt=' '*n + 'Дата поездки: '+text2, ln=1, align="L")
    pdf.cell(210, h, txt=' '*n + 'ФИО: '+text3, ln=1, align="L")
    pdf.cell(210, h, txt=' '*n + 'Количество мест: '+text4, ln=1, align="L")
    pdf.cell(210, h, txt=' '*n + 'Общая стоимость: '+text5, ln=1, align="L")
    # Сохраняем PDF в файл
    pdf.output('media/default/example.pdf')

def mailk(mail):
    fromaddr = "bebranuh2002@mail.ru"
    toaddr = mail
    password = "GKFAMRKdyCAripp47bKb"
    # Создаем письмо
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Отправка PDF файла"
    # Прикрепляем PDF файл
    filename = "example.pdf"
    attachment = open("media/default/example.pdf", "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    # Подключаемся к серверу и отправляем письмо
    server = smtplib.SMTP('smtp.mail.ru', 2525)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def ultrasender(mail, code, avtonum, date, name, seats, summa):
     pqr(code)
     mkpdf(code,avtonum,date,name,seats,summa)
     #mailk(mail)
