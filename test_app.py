import pytest
import re
import os
import io
import inspect
import socket
from itertools import filterfalse
import subprocess

import app
import test_app

# 1
def test_readme():
    assert os.path.isfile("README.md"), "README File Missing"

# 2
def test_readme_desc():
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
    assert len(functions) >= 40, 'Test cases seems to be low. Work harder man...'

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
    expected_packages = ['certificates', 'data_loader', 'mailing', 'mailing/login', 'testing/pretests']
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
    # data -> row string, split -> list, [0] -> name. [1] -> score
    names = {(data.split(',')[0].strip().title(), int(data.split(',')[1]))
                            for data in data_gen() if not data.isspace()}
    for name,score in names:
        if score >  70:
            name = name+'.jpg'
            assert name in filenames, 'All the Qualified Students Certificates Not Present'

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
    printer.template_img('certificates/CertificateTemplate.jpg')

    for i in ent:
        img = printer('Test', 34, i)
    img.save(f'generated_files/Test.jpg')
    *_, filenames = next(os.walk('generated_files'))

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
    password = os.environ.get('GMAIL_PASSWORD')
    try:
        monkeypatch.setattr('getpass.getpass', lambda prompt: password)
        send_mail(test_mail, test_mail, 'Test Mail', mail_type = 'credentials')
        assert True
    except:
        assert False, 'Error When Sending Mail, pleae check!'

# 25
def test_message_text():
    from mailing import compose_message
    contents = compose_message('Test', 'Test', 'Test', 'static/pass.html', 'static/pass.txt')
    regex = r'^(Content-Type: multipart/alternative)'
    assert re.match(regex, contents['message'].as_string())

# 26
def test_message_attach():
    from mailing import compose_attachment
    contents = compose_attachment('Test', 'Test', attachment='static/pass.txt')
    regex = r'^(Content-Type: multipart/alternative)'
    assert re.match(regex, contents.as_string())

## Invalid Check

# 27
def test_printer_invalid_types():
    from certificates import Printer
    with pytest.raises(TypeError):
        Printer('name')

# 28
def test_printer_invalid_co_ord():
    from certificates import Printer
    with pytest.raises(TypeError):
        Printer(('name','score'), co_ordinates=0)

# 29   
def test_printer_invalid_co_ord_value():
    from certificates import Printer
    with pytest.raises(ValueError):
        Printer(('name','score'), co_ordinates=(120,100))

# 30
def test_printer_unequal_co_ord_value():
    from certificates import Printer
    with pytest.raises(ValueError):
        Printer(('name','score', 'signature'), co_ordinates=((120,100),(120,650)))

# 31
def test_printer_call_invalid_content():
    from certificates import Printer
    co_ordinates=((0,0),(0,0),(0,0),(0,0))
    printer = Printer(('name','score','date','signature'), co_ordinates)
    with pytest.raises(TypeError):
        printer(311, 36, 'name', True)

# 32
def test_printer_call_invalid_font():
    from certificates import Printer
    co_ordinates=((0,0),(0,0),(0,0),(0,0))
    printer = Printer(('name','score','date','signature'), co_ordinates)
    with pytest.raises(TypeError):
        printer('Ajay', '36', 'name', True)

# 33
def test_printer_call_invalid_type():
    from certificates import Printer
    co_ordinates=((0,0),(0,0),(0,0),(0,0))
    printer = Printer(('name','score','date','signature'), co_ordinates)
    with pytest.raises(TypeError):
        printer('Kumar', 36, ('name',), True)

# 34
def test_printer_call_invalid_new():
    from certificates import Printer
    co_ordinates=((0,0),(0,0),(0,0),(0,0))
    printer = Printer(('name','score','date','signature'), co_ordinates)
    with pytest.raises(TypeError):
        printer('Kumar', 36, 'name', 'True')

# 35
def test_printer_call_wrong_type():
    from certificates import Printer
    co_ordinates=((0,0),(0,0),(0,0),(0,0))
    printer = Printer(('name','score','date','signature'), co_ordinates)
    with pytest.raises(ValueError):
        printer('Kumar', 36, 'number', True)

# 36
def test_data_loader_invalid_path_type():
    from data_loader import CSV_loader
    with pytest.raises(TypeError):
        CSV_loader(0)

# 37
def test_data_loader_file_not_exist():
    from data_loader import CSV_loader
    with pytest.raises(FileExistsError):
        next(CSV_loader('data2.csv'))

# 38
def test_data_loader_file_not_found():
    from data_loader import CSV_loader
    with pytest.raises(FileNotFoundError):
        next(CSV_loader('docs'))
    
# 39
def test_data_loader_invalid_file():
    from data_loader import CSV_loader
    with pytest.raises(TypeError):
        next(CSV_loader('certificates/CertificateTemplate.jpg'))

# 40
def test_send_mail_invalid_sender():
    from mailing import send_mail
    with pytest.raises(TypeError):
        send_mail(909, 'my@gmail.com', 'Hi', mail_type='credentials')

# 41
def test_send_mail_invalid_receiver():
    from mailing import send_mail
    with pytest.raises(TypeError):
        send_mail('my@gmail.com', 909, 'Hi', mail_type='credentials')

# 42
def test_send_mail_invalid_msg():
    from mailing import send_mail
    with pytest.raises(TypeError):
        send_mail('my@gmail.com', 'my@gmail.com', 404, mail_type='credentials')

# 43
def test_send_mail_all_positional():
    from mailing import send_mail
    with pytest.raises(TypeError):
        send_mail('my@gmail.com', 'my@gmail.com', '404', 'credentials')

# 44
def test_send_mail_invalid_type():
    from mailing import send_mail
    with pytest.raises(ValueError):
        send_mail('my@gmail.com', 'my@gmail.com', '404', mail_type='credential')

# 45
def test_regex_email():
    from testing.pretests import data_validate
    data1 = 'Ajay, 97, ajay#@gmail.com'
    data1 =  data_validate(data1)
    assert data1.check == False, 'Not catching Invalid Email Address'

# 46
def test_regex_name():
    from testing.pretests import data_validate
    data1 = 'Aj@y, 97, ajay@gmail.com'
    data1 =  data_validate(data1)
    assert data1.check == False, 'Not catching Invalid Name'

# 47
def test_regex_score():
    from testing.pretests import data_validate
    data1 = 'Ajay, 103, ajay@gmail.com'
    data1 =  data_validate(data1)
    assert data1.check == False, 'Not catching Invalid Score'

## Main App Checks

# 48
def test_main_batch_mode(monkeypatch, capsys):
    from utils import Print_certificate
    from app import batch_mode
    from data_loader import CSV_loader

    loader = CSV_loader('data.csv')
    co_ord = ((100,100),(100,100),(100,100),(100,100))
    printer = Print_certificate('certificates/CertificateTemplate.jpg', co_ord)
    password = os.environ.get('GMAIL_PASSWORD')
    monkeypatch.setattr('getpass.getpass', lambda prompt: password)
    batch_mode('tsaieva4@gmail.com', loader, printer, 'Test Course', '05-May-2021', (24,24,24,24))
    captured_stdout, captured_stderr = capsys.readouterr()
    expected = 'All the Certificates of valid data has been generated and mailed Successfully.'
    result = captured_stdout.split('\n')[-2] # -1 is empty, -2 is batch_mode print statement
    assert result == expected, 'All the Mails were not sent!'

# 49
def test_main_single_mode(monkeypatch, capsys):
    from utils import Print_certificate
    from app import single_mode


    student_data = 'Andrew Stalt, 91, tsaieva4@gmail.com'
    co_ord = ((100,100),(100,100),(100,100),(100,100))
    printer = Print_certificate('certificates/CertificateTemplate.jpg', co_ord)

    password = os.environ.get('GMAIL_PASSWORD')
    monkeypatch.setattr('getpass.getpass', lambda prompt: password)
    single_mode('tsaieva4@gmail.com', student_data, printer, 'Test Course', '05-May-2021', (24,24,24,24))
    captured_stdout, captured_stderr = capsys.readouterr()
    expected = 'Certificate Created and Mailed!'
    result = captured_stdout.split('\n')[-2] # -1 is empty, -2 is batch_mode print statement
    assert result == expected, 'All the Mails were not sent!'

# 50
def test_comman_line():
    from app import single_mode

    subprocess.run('python3 app.py -s tsaieva4@gmail.com -x 100,100 100,100 100,100 100,100 single \
                    -n "Test Single Mode" --score 78 -r tsaieva4@gmail.com')
    _, _, filenames = next(os.walk('generated_files'))
    assert 'Test Single Mode.jpg' in filenames, 'Commnad Line execution is not working'