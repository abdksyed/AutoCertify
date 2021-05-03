import cv2 as cv
from functools import wraps, partial
from PIL import Image

# To Store co-ordinates of certificates for each entity
co_ordinates = {}

# Mouse callback function
def _dclick_event(event,x,y,flags,param):
    '''
    Gets the co-ordinates of the points where ever 
    there was a Left Mouse Double Click, and added
    it to global co_ordinates.
    Note:
        The function is not called directly, this is passed to
        cv.setMouseCallback method, and the method expects 5 parameters
        in the function which is passed
    Arguments:
        event - The type of event(mouse click)
        x - The x co-ordinate of click
        y - the y co-ordinate of click
        flags - Additional evens (drag, shift key, ctrl key etc.)
        params - The extra paramets passed when calling
    Returns:
        None
    '''
    if event == cv.EVENT_LBUTTONDBLCLK:
        co_ordinates[param] = (x,y)
        cv.destroyAllWindows()

def _open_cv_box(cv_img:'CV Image', entity_key: str):
    '''
    Open a Image window, to store the Left Double Click of user as cor_ordinate for printing.
    The function internally calls _dclick_event function to get Mouse Callback.
    The Window automatically closes after Double click by user.

    Argumetns:
        cv_img - OpenCV Image file
        entity_key - the key in co_ordinates dict, to store co-ordinates for that entity.
    '''
    cv.namedWindow('Image')
    cv.setMouseCallback('Image', _dclick_event, entity_key)
    cv.imshow('Image',cv_img)
    cv.waitKey(0)

def get_cord(fn:callable):
    '''
    A Decorator which takes in a function and decorates it as a Register.
    This Register can is used to take in multiple functions and call those functions using the register itself.
    Ex:
        fn.register('some_func'):
        def some_func():
            #code

        fn(....., 'some_func') will call the some_func internally. 
    '''
    
    # Regsitry of differnet functions
    registry = dict()

    # Temporary Holding Image, can be changed by calling template_img attribute
    registry['cv_img'] = cv.imread("F:\\#Coding\\Capstone\\certificates\\CertificateTemplate.jpg")

    # Child Decorator
    def register(type_, co_ord=None):
        def inner(fn):
            if not co_ord:
                print(f'Double Left Click on the Middle Bottom Point on Template Where the "{type_}" is to be printed!')
                _open_cv_box(registry['cv_img'], type_)
            else:
                co_ordinates[type_] = co_ord
            registry[type_] = fn()
            return fn
            
        return inner

    @wraps(fn)
    def decorator(content, font_size, type_, new=False):
        fn = registry[type_]
        if new:
            template_img(registry['path']) # 
        registry['img'] = fn(registry['img'], co_ordinates.get(type_, 0), content, font_size)

        return registry['img']

    def dispatch(type_):
        return registry[type_]

    def template_img(img:'image path'):
        '''
        This function is called first to give the template Image of the Certificate.
        The functiuon than reads the file with OpenCV and also PIL Image and saves
        it(path, cv_img, pil_img) in the registry dict.
        
        Arguments:
            img - Image Path of the Template Certificate  
        '''
        registry['path'] = img
        cv_img = cv.imread(img)
        registry['cv_img'] = cv_img
        brg_rgb = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        pil_img = Image.fromarray(brg_rgb)
        registry['img'] = pil_img


    # Making Attributes for the Inner Function(function which is decorated)
    # Such that the function can call internal functions using . operator
    decorator.register = register
    decorator.registry = registry.keys()
    decorator.dispatch = dispatch
    decorator.template_img = template_img
    
    return decorator
