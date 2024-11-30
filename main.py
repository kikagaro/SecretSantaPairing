#!/usr/bin/python3

import datetime
import os
import random
import smtplib
import uuid
import yaml

from email.mime.text import MIMEText

ID = str(uuid.uuid4())

# Built for use with a gmail account.
email_sender = ""
# Google App Password is required. https://myaccount.google.com/apppasswords
email_app_pass = ""


email_subject = f"Secret Santa {datetime.datetime.today().year}-{ID}"
msg = []
output_file = f"./output-{ID}.yml"
santas = []
santa_list = []
santa_file = "./santa.yml"
send_email = True

#Retry function for when list fails to create usable pairings.
def retry(func):
    def inner(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except RuntimeError as e:
                print(e)
    return inner


def import_file(file_name, chmod):
    with open(file_name, chmod) as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
        stream.close()
    return data

def update_list(out_file, data_to_append):
    try:
        append_data = yaml.load(data_to_append, Loader=yaml.FullLoader) or {}
        with open(out_file, "a+") as file:
            yaml.dump(append_data, file, default_flow_style=False)
            file.close()
    except all:
        print("Failed to write out yaml file.")


@retry
def generate_list():
    santa = import_file(santa_file, "r")
    print("Imported the following for pairings:\n" + str(santa))
    for x in santa.keys():
        santas.append(x)

    gifted = santas[:]
    for x in santa.keys():
        gift = random.choice(gifted)
        if gift is x and len(gifted) == 1:
            if os.path.exists(output_file):
                os.remove(output_file)
            raise RuntimeError("Single person left in list, regenerating.")
        while gift is x:
            gift = random.choice(gifted)
        message = f"{x} will draw for {gift}"
        update_data = f"""
        {x}:
            email: {santa[x]["email"]}
            gift: {gift}
        """
        update_list(output_file, update_data)
        santa_list.append(message)
        gifted.remove(gift)
    if send_email:
        email_data = import_file(output_file, "r")
        for x in email_data.keys():
            email_body = f"{x}, you will be santa for {email_data[x]['gift']}."
            send_email(email_subject, email_sender, email_data[x]["email"], email_body, email_app_pass)
    return


def send_email(subject, sender, recipient, body, password):
    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            try:
                smtp_server.login(email_sender, password)
            except all:
                print("Failed to login.")
            try:
                smtp_server.sendmail(email_sender, recipient, msg.as_string())
            except all:
                print("Failed to send Email.")
        print("Message Sent")
    except all:
        print("smtp failed.")

result = generate_list()
