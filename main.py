import sys
import smtplib
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def conn_smtp() -> smtplib.SMTP:
    """The goal of this function is to connect to smtp server"""
    try:
        smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
        return smtpObj
    except smtplib.socket.error:
        print("Error: unable to connect to smtp server")
        return None


def login(smtpObj: smtplib.SMTP) -> int:
    """Function to login with sender credentials"""
    try:
        smtpObj.login(config['DETAILS']['sender_email_id'],
                      config['DETAILS']['sender_email_pass'])
        return 0
    except smtplib.SMTPAuthenticationError:
        print("Error: unable to login using sender email id and password")
        return 1


def create_message() -> str:
    """This functions takes the subject and message of the mail"""
    message = 'Subject: {}\n\n{}'.format(
        config['DETAILS']['subject'], config['DETAILS']['message'])
    return message


def send_mail(smtpObj: smtplib.SMTP, message: str) -> int:
    try:
        smtpObj.sendmail(config['DETAILS']['sender_email_id'],
                         config['DETAILS']['reciever_email_id'], message)
        print("Mail Send successfully")
        return 0
    except smtplib.SMTPRecipientsRefused:
        print("Error: unable to send mail")
        return 1


def main():
    """main function i.e. The driver code"""
    smtpObj = conn_smtp()
    if smtpObj == None:
        sys.exit()
    smtpObj.starttls()
    status = login(smtpObj)
    if status == 1:
        sys.exit()
    message = create_message()
    status = send_mail(smtpObj, message)
    if status == 1:
        sys.exit()
    smtpObj.quit()


if __name__ == "__main__":
    main()
