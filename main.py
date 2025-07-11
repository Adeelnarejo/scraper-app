import requests
import selectorlib
import smtplib, ssl
import os

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

user_email = "adeel.nariai96@gmail.com"

def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extractor.yaml')
    value = extractor.extract(source)['tours']
    return value

def send_email(user_email, message):
    host = "smtp.gmail.com"
    port = 465

    username = "###"
    password = "###"

    receiver_email = user_email

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver_email, message)


def stored(extracted):
    with open('stored.txt', 'a') as file:
        file.write(extracted + "\n")


def read(extracted):
    with open('stored.txt', 'r') as file:
        return file.read()

if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)

    content = read(extracted)

    if extracted != "No upcoming tours":
        if extracted not in content:
            stored(extracted)
            message = extracted
            send_email(user_email, message)
    else:
        print('no upcoming tours else......')