# message.py

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

__all__ = ['compose_message', 'compose_attachment']

def compose_message(sender:str, receiver:str, subject:str, 
                html_file:'Static HTML File', plain_file: 'Plain-text file') -> MIMEMultipart:
    '''
    Create a multipart message with both HTML and Plain-Text.
    The HTML is primary message, and plain-text message is alternate
    if the email client doesn't support HTML.

    Arguments:
        sender > The email id of the sender.
        receiver > The email id of the receiver.
        subject > The Subject of the mail.
        html_file > The HTML file which is to be rendered.
        plain_file > The plain file which is to be read and send as alternative to HTML.

    Retuns:
        content > a MIMEMultipart object which is the message we need to send.
    '''

    # Create a multipart message and set headers
    content = MIMEMultipart("alternative")
    content["From"] = sender
    content["To"] = receiver
    content["Subject"] = subject

    # Creating Plain-Text and HTML version of message
    with open(plain_file) as plain:
        text_msg = ''.join(plain.readlines())

    with open(html_file) as html:
        html_msg = ''.join(html.readlines())


    # Turn these into plain/html MIMEText objects
    plain_part = MIMEText(text_msg, "plain")
    html_part = MIMEText(html_msg, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the LAST PART FIRST
    content.attach(plain_part)
    content.attach(html_part)

    return {'sender': sender, 'receiver': receiver, 'message':content}


def compose_attachment(sender:str, receiver:str, content: MIMEMultipart = None, attachment: 'File Path'= None) -> MIMEMultipart:
    '''
    This function is used to create an attachment of file and join it to the message and returns combined
    message body and the attachment.
    If the content (message) is None, if creates a default message and attach the attachment.
    If attachment in None, it just returns the message which it received as fallback.

    Arguments:
        sender - The email address of sender
        receiver - The email address of recevier
        content - The message content to which the attachment is to be attached. (Default = None)
        attachment - Path to the file which is to be attached. (Default = None) 

    Returns
        content - The MIMEMultipart object which not has both message content and attachment.      
    '''
    if not content: #message is none -> compose Generic Content
        
        content = MIMEMultipart("alternative")
        content["From"] = sender
        content["To"] = receiver
        content["Subject"] = 'Attachment'

        text_msg = 'Please find the attached file. \n \n Regards'
        text_msg = MIMEText(text_msg, "plain")
        content.attach(text_msg)

    if attachment: # If attachment is present (not None) 

        # Opening attachment in binary mode
        with open(attachment, 'rb') as att:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            attach_part = MIMEBase('application', 'octet-stream')
            attach_part.set_payload(att.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(attach_part)
        
        # Add header as key/value pair to attachment part
        # Attachment Name if is inside folder, split with '\'
        # and ues the file name only.
        attach_part.add_header('Content-Disposition', 'attachment',
                                filename= attachment.split('/')[-1])

        content.attach(attach_part)

    return content

