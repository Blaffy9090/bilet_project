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
    # ��������� ����������
    background = Image.open("media/default/2.png")
    overlay = Image.open("qrcode.jpg")

    width, height = overlay.size
    new_width = int(width * 0.6)
    new_height = int(height * 0.6)
    overlay = overlay.resize((new_width, new_height))

    # ��������� ����� �������� �� ������
    background.paste(overlay, (71, 273), overlay)

    # ��������� ���������
    background.save("output.png")

def mkpdf(code,avtonum,date,name,seats,summa):
    # ������� ������ PDF
    pdf = FPDF('L', 'mm', 'A4')

    # ��������� ����� ��������
    pdf.add_page()
    background = Image.open("media/default/2.png")
    width, height = background.size
    # ��������� �����������
    pdf.image('output.png',-8, -10, width*0.35, height*0.4)  # ���������: ���� � �����������, x, y, ������, ������
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
    pdf.cell(210, h, txt=' '*n + '����� ������: '+text, ln=1, align="L")
    pdf.cell(210, h, txt=' '*n + '����� ��������: '+text1, ln=1, align="L")
    pdf.cell(210, h, txt=' '*n + '���� �������: '+text2, ln=1, align="L")
    pdf.cell(210, h, txt=' '*n + '���: '+text3, ln=1, align="L")
    pdf.cell(210, h, txt=' '*n + '���������� ����: '+text4, ln=1, align="L")
    pdf.cell(210, h, txt=' '*n + '����� ���������: '+text5, ln=1, align="L")
    # ��������� PDF � ����
    pdf.output('media/default/example.pdf')

def mailk(mail):
    fromaddr = "bebranuh2002@mail.ru"
    toaddr = mail
    password = "GKFAMRKdyCAripp47bKb"
    # ������� ������
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "�������� PDF �����"
    # ����������� PDF ����
    filename = "example.pdf"
    attachment = open("media/default/example.pdf", "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    # ������������ � ������� � ���������� ������
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
