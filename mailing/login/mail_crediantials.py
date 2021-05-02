import smtplib, ssl, getpass

__all__ = ['send_mail']

port = 465

def _gmail_crediantials():
    '''
    A Closure, to allow us to keep the input email id and password in memory 
    for multiple use, or ask for input for the first time.
    '''
    sender_email, password = None, None
    def inner():
        '''
        
        '''
        nonlocal sender_email, password
        if not (sender_email and password):
            sender_email = input("Enter the Sender's email address, leave empty if want to use default: ") or "tsaieva4@gmail.com"
            password = getpass.getpass(prompt='Type Password and press Enter: ', stream=None)

        return sender_email, password
    return inner

_gmail_crediantials = _gmail_crediantials()


def send_mail(sender:str, receiver:str, message:str):
    '''
    Creates a Secure TSL-encrypted connection.
    Take User Input of email id and passwrod.
    (** The email id and Password are not stored and used directly for security purpose)
    '''
    global port
    
    #Create a securte SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(*_gmail_crediantials()) #Not storing user input email and password and directly using it to login
        server.sendmail(sender, receiver, message)
