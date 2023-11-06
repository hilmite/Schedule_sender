from datetime import datetime
from io import BytesIO
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# choice = int(input("Your year of study: "))
#
# while 1 > choice or 4 < choice:
#     print('Wrong, debil. Write normalnoe ChIsLo plz!!!')
#     choice = int(input())

browser = Chrome()

browser.get('https://wm.pollub.pl/studenci/plany-zajec')
sleep(3)

profession = browser.find_element(By.XPATH, f'/html/body/section[3]/div/div/div[1]/div/div[2]/div[10]/button/h3')
profession.click()
sleep(5)

schedule = browser.find_element(By.XPATH, f'/html/body/section[3]/div/div/div[1]/div/div[2]/div[10]/div/div/div[3]/div[2]/a')
schedule.click()
sleep(3)

current_day = datetime.now().weekday()

if current_day in (5, 6):
    text = MIMEText("Vihodnoy, spi brat")
else:
    top = 115
    height = 1000
    left = 350
    width = 510

    screenshot = browser.get_screenshot_as_png()
    img = Image.open(BytesIO(screenshot))
    img = img.crop((left, top, left + width, top + height))

    img.save("screenshot.png")

    text = MIMEText("Your schedule")

msg = MIMEMultipart()
msg['From'] = 'srukamnyami228@gmail.com'
msg['To'] = 'srukamnyami228@gmail.com'
msg['Subject'] = 'Schedule'
msg.attach(text)

with open("screenshot.png", "rb") as f:
    image = MIMEImage(f.read())
    msg.attach(image)


with open('password.txt', 'r') as file:
    sender_password = file.read().strip()

sender_email = 'srukamnyami228@gmail.com'
recipient_email = 'srukamnyami228@gmail.com'

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = 'Schedule'

text = MIMEText("Your schedule")
msg.attach(text)

with open("screenshot.png", "rb") as f:
    image = MIMEImage(f.read())
    msg.attach(image)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, sender_password)
server.sendmail(sender_email, recipient_email, msg.as_string())
server.quit()

browser.quit()
