import pytest
import re
import os
import inspect
import socket
from itertools import filterfalse

import app
import test_app
from testing.pretests import test_imports

# 1
def test_readme():
    assert os.path.isfile("README.md"), "README File Missing"

# 2
def test_readme_desc():
    READMELOOKGOOD = True
    f = open('README.md', "r", encoding='utf8')
    content = f.read().split()
    f.close()
    assert len(content) >= 500, "Make your README.md file interesting."

# 3
def test_readme_file_for_formatting():
    f = open("README.md", "r", encoding="utf8")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

# 4
def test_function_count():
    functions = inspect.getmembers(test_app, inspect.isfunction)
    assert len(functions) >= 50, 'Test cases seems to be low. Work harder man...'

# 5
def test_function_repeatations():
    functions = inspect.getmembers(test_app, inspect.isfunction)
    names = []
    for function in functions:
        names.append(function)
    assert len(names) == len(set(names)), 'Test cases seems to be repeating...'

# 6
def test_docstrings():
    function = inspect.getmembers(app, inspect.isfunction)
    for func in function:
        assert func[1].__doc__

# 7
def test_annotation():
    function = inspect.getmembers(app, inspect.isfunction)
    for func in function:
        if func[0] != 'namedtuple':
            assert func[1].__annotations__

# 8
def test_internet():
    try:
        _REMOTE_SERVER = "one.one.one.one"
        host = socket.gethostbyname(_REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        s.close()
        assert True
    except socket.gaierror:
        assert False, "NO Internet Connection Found"

# 9
def test_imports():
    try:
        import cv2 as cv
        import PIL
        import pytest

        assert True
    except:
        assert False, 'Proper Imports Not Found'

# 10
def test_dupl_certifcates():
    _, _, filenames = next(os.walk('generated_files'))
    files = list(map(lambda x: x.lower(), filenames))
    assert len(files) == len(set(files)), 'You have Duplicate Certificates'

# 11
def test_static_files():
    req_files = ['pass.html', 'fail.html', 'pass.txt', 'fail.txt']
    _, _, filenames = next(os.walk('static'))
    for file in req_files:
        assert file in filenames

# 12
def test_data_file():
    assert os.path.isfile("data.csv"), "Student Data CSV File Missing"

# 13
def test_template_certificate():
    assert os.path.isfile('certificates/CertificateTemplate.jpg'), "Template Certificate Missing"

# 14
def test_package():
    expected_packages = ['certificates', 'data_loader', 'mailing', 'mailing\\login', 'testing\\pretests']
    for package in expected_packages:
        _, _, filenames = next(os.walk(package))
        assert '__init__.py' in filenames

# 15
def test_package_import():
    import certificates
    import data_loader
    import mailing
    from mailing import login
    from testing import pretests

    for package in [certificates, data_loader, mailing, login, pretests]:
        try:
            package.__path__
            assert True
        except AttributeError:
            assert False, f'{package} is NOT a Package.'

# 16
def test_email():
    regex = r'^[a-zA-Z](\w|\.|\-)*[@](\w|\.|\-)+[.][a-zA-Z]{2,4}$'

    def data_gen():
        with open('data.csv') as csv_file:
            yield from csv_file

    def reg_check(data_row):
        if data_row.isspace(): #empty row
            return True
        *_, email = data_row.split(',')
        return re.match(regex, email.strip())

    assert not any(filterfalse(reg_check, data_gen())), 'Some Invalid email Address Present in Data'

# 17
def test_name():
    regex = r'^[a-zA-Z ]+$'

    def data_gen():
        with open('data.csv') as csv_file:
            yield from csv_file

    def reg_check(data_row):
        if data_row.isspace(): #empty row
            return True
        name, *_ = data_row.split(',')
        return re.match(regex, name.strip())

    assert not any(filterfalse(reg_check, data_gen())), 'Some Invalid Name Present in Data'

# 18
def test_score():

    def data_gen():
        with open('data.csv') as csv_file:
            yield from csv_file

    def range_check(data_row):
        if data_row.isspace(): #empty row
            return True
        _, score, _ = data_row.split(',')
        try:
            score = int(score.strip())
        except ValueError:
            return False

        return score in range(0,101)
        

    assert not any(filterfalse(range_check, data_gen())), 'Some Invalid Score Present in Data'

# 19
def test_certificates_names():

    def data_gen():
        with open('data.csv') as csv_file:
            yield from csv_file
    
    *_, filenames = next(os.walk('generated_files'))
    # data -> row string, split -> list, [0] -> name.
    names = {data.split(',')[0].strip().title() for data in data_gen() if not data.isspace()}
    for file in filenames:
        if file == 'Test.jpg':
            continue
        assert file.split('.')[0] in names, 'Additional Files found in Generated Files Folder'

# 20
def test_certificate_extension():
    *_, filenames = next(os.walk('generated_files'))
    for file in filenames:
        assert file.split('.')[-1] == 'jpg'

# 21
def test_printer_register():
    from certificates import Printer
    co_ord = ((0,0),(0,0),(0,0),(0,0))
    printer = Printer(('name', 'course', 'date', 'signature'), co_ord)
    regex = r'^(<function get_cord)'
    assert re.match(regex, str(printer().register))

# 22
def test_gen_certificate():
    from certificates import Printer

    co_ord = ((100,100),(100,100),(100,100),(100,100))
    ent = ('name', 'course', 'date', 'signature')

    printer = Printer(ent, co_ord)
    printer.template_img('certificates\\CertificateTemplate.jpg')

    for i in ent:
        img = printer('Test', 34, i)
    img.save(f'generated_files\\Test.jpg')
    *_, filenames = next(os.walk('generated_files'))
    print(filenames)

    assert 'Test.jpg' in filenames

# 23
def test_data_loader():

    def data_gen():
        with open('data.csv') as csv_file:
            yield from csv_file

    from data_loader import CSV_loader
    loader = CSV_loader('data.csv')
    act_loader = data_gen()
    for row in loader:
        assert row == next(act_loader).strip()

# 24
def test_send_mail(monkeypatch):
    from mailing import send_mail
    test_mail = 'tsaieva4@gmail.com'
    password = os.environ['GMAIL_PASSWORD']
    try:
        monkeypatch.setattr('builtins.input', lambda _: test_mail)
        monkeypatch.setattr('getpass.getpass', lambda prompt: password)
        send_mail(test_mail, test_mail, 'Test Mail', mail_type = 'credentials')
        assert True
    except:
        assert False, 'Error When Sending Mail, pleae check!'