import sys
import logging
import smtplib
import configparser

config = configparser.ConfigParser()
config.read("smtp_config.ini")


def conn_smtp(server: str, port: int) -> smtplib.SMTP:
    """The goal of this function is to connect to smtp server"""
    try:
        smtpObj = smtplib.SMTP(server, port)
        return smtpObj
    except smtplib.socket.error:
        logging.info("Error: unable to connect to smtp server")
        return None


def login(smtpObj: smtplib.SMTP, email: str, password: str) -> int:
    """Function to login with sender credentials"""
    try:
        smtpObj.login(email, password)
        return 0
    except smtplib.SMTPAuthenticationError:
        logging.info(
            "Error: unable to login using sender email id and password")
        return 1


def create_message(subject: str, msg: str) -> str:
    """This functions takes the subject and message of the mail"""
    message = 'Subject: {}\n\n{}'.format(subject, msg)
    return message


def send_mail(smtpObj: smtplib.SMTP, sender: str, reciever: str, message: str) -> int:
    try:
        smtpObj.sendmail(sender, reciever, message)
        logging.info("Mail Send successfully")
        return 0
    except smtplib.SMTPRecipientsRefused:
        logging.info("Error: unable to send mail")
        return 1


def main():
    """main function i.e. The driver code"""
    smtpObj = conn_smtp(config['DETAILS']['smtp_server'],
                        config['DETAILS']['smtp_port'])
    if smtpObj == None:
        sys.exit()
    smtpObj.starttls()
    status = login(smtpObj, config['DETAILS']['sender_email_id'],
                   config['DETAILS']['sender_email_pass'])
    if status == 1:
        sys.exit()
    message = create_message(
        config['DETAILS']['subject'], config['DETAILS']['message'])
    status = send_mail(smtpObj, config['DETAILS']['sender_email_id'],
                       config['DETAILS']['reciever_email_id'], message)
    if status == 1:
        sys.exit()
    smtpObj.quit()


if __name__ == "__main__":
    main()
