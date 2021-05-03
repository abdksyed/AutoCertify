# test_data.py

import re
from collections import namedtuple

def _test_email(email):
    '''
    Regex for Testing Valid email address
    '''
    regex = r'^[a-zA-Z](\w|\.|\-)*[@](\w|\.|\-)+[.][a-zA-Z]{2,4}$'
    return bool(re.search(regex, email.strip()))


def _test_name(name):
    '''
    Regex for Testing Valid name
    '''
    regex = r'^[a-zA-Z ]+$'
    return bool(re.search(regex, name.strip()))


def _test_score(score):
    '''
    Testing Valid Score
    '''
    try:
        score = int(score.strip())
    except ValueError:
        return False

    return score in range(0,101)


def data_validate(student_details):
    '''
    The function will check all the Student Details are Valid.
    If all the data is valid, it creates and returns a named tuple
    with .check as True and data as tuple,
    else send nametuple with .check as False.

    Arguments:
        student_details - The string of data seperated by ','
    Return
        data - Named Tuple with attributes check and data.
    '''
    data = namedtuple('data', 'check, data')

    if not student_details: #Empty
        return data(False, 'Empty String " "')
    
    name, score, email = student_details.split(',')

    if _test_email(email) and  _test_name(name) and _test_score(score):
        return data(True, (name.title(),score,email))
    else:
        return data(False, student_details)