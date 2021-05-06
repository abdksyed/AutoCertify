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

i = 0
def send_mail(sender:str, receiver:str, message:str):
    '''
    Creates a Secure TSL-encrypted connection.
    Take User Input of email id and passwrod.
    (** The email id and Password are not stored and used directly for security purpose)
    '''
    if not isinstance(sender, str):
        raise TypeError('The sender email id must be a string')
    if not isinstance(receiver, str):
        raise TypeError('The receiver email id must be a string')
    if not isinstance(message, str):
        raise TypeError('The message must be a string')

    global port, _crediantials, i
    
    #Create a securte SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        try: 
            server.login(sender, _crediantials()) #Not storing user input email and password and directly using it to login
            i += 1
        except smtplib.SMTPAuthenticationError:
            # Allowing Renetering Password 3 times in Invalid
            if i < 3:
                print('Invalid Credentials. Please Enter Again')
                _crediantials = _gmail_crediantials() #Re initializing the gmail_credentials to erase closure vairalbles.
                return send_mail(sender, receiver, message)
            else:
                raise smtplib.SMTPAuthenticationError
        server.sendmail(sender, receiver, message)
