import smtplib
from collections import namedtuple
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.config import get_setting

CommunityInfos = namedtuple(
    typename="CommunityInfos",
    field_names=["name", "reference", "creation_date"],
)


async def send_email(
    subject: str, body: str, attachment_path: str, destination: str
) -> bool:
    """Send an email

    Args:
        subject (str): subject
        body (str): body
        attachment_path (str): path of file to attach
        destination (str): destination email

    Returns:
        bool: True if email is sent
    """
    sender_email = get_setting("sender_email")
    sender_password = get_setting("sender_password")
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            "attachment",
            filename=attachment_path.split("/")[-1],
        )

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = destination
        html_part = MIMEText(body)
        msg.attach(html_part)
        msg.attach(part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            return True


async def send_email_without_attachment(
    subject: str, body: str, destination: str
) -> bool:
    """Send an email without attached file.

    Args:
        subject (str): subject
        body (str): body
        destination (str): destination email


    Returns:
        bool: True if email is sent
    """
    sender_email = get_setting("email_sender")
    sender_password = get_setting("email_password")

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = destination
    html_part = MIMEText(body)
    msg.attach(html_part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        return True
