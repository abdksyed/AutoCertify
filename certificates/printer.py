# printer.py

from PIL import ImageFont, ImageDraw
from .co_ord_getter import get_cord
import cv2 as cv


__all__ = ['Printer']

def processing(img: 'PIL Image File', co_ord, print_content, font_size, new=False):
    '''
    The function is used to Draw the Text on the Image with the given font_size and ITCBLKAD font.

    Arguments:
        img - PIL Image
        co_ord - The co-ordinates of the bottom middle point where the content is to be printed.
        print_content - The content to print
        font_size - Font size of the content to be printed
        new - Takes a new empty PIL Image for processing.

    Returns:
        img - Processed PIL Image
    '''
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('C:\\Windows\\Fonts\\ITCBLKAD.ttf', font_size)
    draw.text(co_ord, print_content, font=font, fill='black', anchor='ms')

    return img


class Printer:

    def __init__(self, types_:tuple, co_ordinates:tuple = None):
        self.types_ = types_
        if not co_ordinates:
            self.co_ordinates = (None,)*len(types_)
        else:
            self.co_ordinates = co_ordinates

        @get_cord
        def printo(self, content, font_size, type_, new=False):
            '''
            The function is a Pseduo function which get's an internal decorator to attach 
            other function to it and call those function with the type_ variable

            Arguments:
                content - The content to be printed.
                font_size - Font size of the content to be printed
                type_ - This decides which sub-function and which co-ordinates to use for printing.
                new - Takes a new empty PIL Image for processing. (Defaulted to False)
            Return:
                'This is Default' string which the type_ doesn't match with any of the predefined types.
            '''
            return 'This is Default!'

        @printo.register(self.types_[0],self.co_ordinates[0])
        def print_name():
            '''
            The function is wrapped with the main printo function's Register, where this function
            is assigned to the type 'name'.

            Return:
                The function Processeing which Prints content on Image(certificate). 
            '''
            return processing

        @printo.register(self.types_[1],self.co_ordinates[1])
        def print_course():
            '''
            The function is wrapped with the main printo function's Register, where this function
            is assigned to the type 'course'.

            Return:
                The function Processeing which Prints content on Image(certificate). 
            '''
            return processing

        @printo.register(self.types_[2],self.co_ordinates[2])
        def print_date():
            '''
            The function is wrapped with the main printo function's Register, where this function
            is assigned to the type 'date'.

            Return:
                The function Processeing which Prints content on Image(certificate). 
            '''
            return processing

        @printo.register(self.types_[3],self.co_ordinates[3])
        def print_signature():
            '''
            The function is wrapped with the main printo function's Register, where this function
            is assigned to the type 'signature'.

            Return:
                The function Processeing which Prints content on Image(certificate). 
            '''
            return processing

        self.printo = printo
        self.template_img = printo.template_img
    
    def __call__(self, content=None, font_size=None, type_=None, new=False):
        if not all((content, font_size, type_)):
            return self.printo
        return self.printo(content, font_size, type_, new)