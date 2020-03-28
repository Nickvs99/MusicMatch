"""
Set of functions used in views.py
"""

from django.core.mail import send_mail
from utils.utils import *

def send_email(subject, message, recipients):
    """
    Sends email
    Args:
        subject: str
        message: str
        recipients: list of str
    """

    try:
        send_mail(
                subject,
                message,
                get_env_var("EMAIL_HOST_USER"),
                recipients,
                fail_silently = False
            )
    except:
        print( '\n'.join((
            "Possible solutions:",
            " - Make sure your email and password are the right combination.",
            " - Turn on less secure apps on your google account, visit https://myaccount.google.com/lesssecureapps?pli=1 to turn the feature on.",
            " - Have a stable internet connection."
        )))

