from django.contrib import messages
from django.core.mail import send_mail

from main.util.util import get_env_var

def send_email(subject, message, recipients, request=None):
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
            get_env_var("EMAIL_NOREPLY_USER"),
            recipients,
            fail_silently = False
        )

    except:
        
        if(request):
            messages.error(request, f"There was a problem with sending you an email. Please contact us at {get_env_var('EMAIL_CONTACT_USER')}.")

        import traceback
        print(traceback.format_exc())
        print('\n'.join((
            "Possible solutions:",
            " - Make sure your email and password are the right combination.",
            " - Turn on less secure apps on your google account, visit https://myaccount.google.com/lesssecureapps?pli=1 to turn the feature on.",
            " - Have a stable internet connection."
        )))
