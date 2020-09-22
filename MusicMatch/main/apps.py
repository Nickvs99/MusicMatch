from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        
        from main.email import send_email
        from main.util.util import get_env_var
        
        environment_check()

        # On not receiving the email, we know their was an error on the env variables
        send_email("Server start", "Server succesfully started", [get_env_var("EMAIL_SERVER_USER")])

def environment_check():
    """
    Checks if all environment variables have a correct value. An exception is raised when one
    of the variables does not have a value
    """
    from main.util.util import get_env_var

    # Check if each environment key has a value
    env_keys = ["DOMAIN", "SECRET_KEY", "CLIENT_ID", "CLIENT_SECRET", "FERNET_KEY",
                "EMAIL_NOREPLY_USER", "EMAIL_NOREPLY_PASSWORD", "EMAIL_SERVER_USER",
                "DEBUG"]

    for key in env_keys:
        get_env_var(key)

    