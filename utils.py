# utils.py

from collections import namedtuple
from os import walk

import testing.pretests as pretest
from certificates import Printer
from mailing import compose_attachment, compose_message, send_mail


_, _, filenames = next(walk('generated_files'))

class Print_certificate():
    '''
    A Class which initializes Printer object and take co-ordinates for all 4 entitities.
    A call() class which run when the object is called, prints the Student Data on the Certificate,
    if the certificate is not present in the folder.
    '''
    def __init__(self, img_path: 'PATH', co_ord:str = None):
        self.printer = Printer(('name', 'course', 'date', 'signature'), co_ord)
        self.printer.template_img(img_path)
    
    def __call__(self, student_det: namedtuple, course_name: str, date:str, fonts: [int,tuple]):
        if student_det.name+'.jpg' in filenames:
            return 
        if isinstance(fonts, int):
            fonts = (fonts,)*4
        img = self.printer(student_det.name, fonts[0], 'name', new=True)
        img = self.printer(course_name, fonts[1], 'course')
        img = self.printer(date, fonts[2], 'date')
        img = self.printer('Rohan Shravan', fonts[3], 'signature')
        img.save(f'generated_files\\{student_det.name}.jpg')


@pretest.connection_test
def mailer(sender:str, receiver:str, subject:str, html_file: 'PATH', plain_file: 'PATH', file_name: 'PATH' = None, mail_type: str="credentials"):
    '''
    Use mailing package to Create Message Attachment and Sends out email using the mail_type OAuth2 or Credentials.
    The function is decored to test Internet Connection before sending emails.
    Arguments:
        sender - The email address of the sender.
        receiver - The email address of the reciver
        subject - The Subject of the mail.
        html_file - The HTML file to be rendered as the body of mail.
        plain_file - The alternate plain file of the body message.
        file_name - The file_name path of the attachment(Default = None)
        mail_type - The mailing way, either OAuth2 or using Credentials (Default = "credentials")

    Returns:
        200, 'Success' if There is no Error in sending the mail.
    '''
    mail_data = compose_message(sender, receiver, subject, html_file, plain_file)

    sender, receiver, message = mail_data.values()
    message = compose_attachment(sender, receiver, message, file_name)

    send_mail(sender, receiver, message.as_string(), mail_type = mail_type)

    return 200, 'SUCCESS'

def parse_tuple(string_tp:str):
    '''
    Parses the String of eah co-oridnate to Tuple

    Argument:
        string_tp - String of Tuple ex '100,120'
    Return:
        parsed_tp - Parsed Tuple, ex: (100,120) 
    '''
    try:
        x,y = map(int, string_tp.split(','))
    except:
        raise TypeError('The Format should be x,y x,y x,y')

    return x,y
