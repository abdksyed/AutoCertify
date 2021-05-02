# login

from . import mail_crediantials
from . import mail_OAuth2 

__all__ = ['send_mail']



def send_mail(sender:str, receiver:str, message:str, *, mail_type):
    '''
    Sends mail based on mail_type using either credentials or OAuth.

    When selected Credentials, ask for user input of email addressa and password
    (** The email id and Password are not stored and used directly for security purpose)

    Arguments:
        sender - Sender's email address
        receiver - Receiver's email address
        message - The Body of the mail
        mail_type - (Mandatory Keyword Argument) 'credentails' or 'oauth'
    Returns:
        None
    '''
    if mail_type.lower() == 'credentials':
        mail_crediantials.send_mail(sender, receiver, message)
    elif mail_type.lower() == 'oauth':
        mail_OAuth2.send_mail(sender, receiver, message)
    else:
        raise ValueError('Invalid mail type option selected. Use either Credentials or OAuth')