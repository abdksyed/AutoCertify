import smtplib, ssl, getpass

__all__ = ['send_mail']

port = 465

def _gmail_crediantials():
    '''
    A Closure, to allow us to keep the input email id and password in memory 
    for multiple use, or ask for input for the first time.
    '''
    password = None
    def inner():
        '''
        
        '''
        nonlocal password
        if not password:
            #password = input('Type Password and press Enter: ')
            password = getpass.getpass(prompt='Type Password and press Enter: ')
            print('Checking Password.....Initiating Printing and Sending Mails. Please Wait..........')

        return password
    return inner

_crediantials = _gmail_crediantials()


def send_mail(sender:str, receiver:str, message:str):
    '''
    Creates a Secure TSL-encrypted connection.
    Take User Input of email id and passwrod.
    (** The email id and Password are not stored and used directly for security purpose)
    '''
    global port, _crediantials
    
    #Create a securte SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        try: 
            server.login(sender, _crediantials()) #Not storing user input email and password and directly using it to login
        except smtplib.SMTPAuthenticationError:
            print('Invalid Credentials. Please Enter Again')
            _crediantials = _gmail_crediantials() #Re initializing the gmail_credentials to erase closure vairalbles.
            return send_mail(sender, receiver, message)
        server.sendmail(sender, receiver, message)
