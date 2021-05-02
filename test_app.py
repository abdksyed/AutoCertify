import pytest
import re
import os
import inspect
import socket
from itertools import filterfalse

import app
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
def test_docstrings():
    function = inspect.getmembers(app, inspect.isfunction)
    for func in function:
        assert func[1].__doc__

# 5
def test_annotation():
    function = inspect.getmembers(app, inspect.isfunction)
    for func in function:
        if func[0] != 'namedtuple':
            assert func[1].__annotations__

# 6
def test_internet():
    try:
        _REMOTE_SERVER = "one.one.one.one"
        host = socket.gethostbyname(_REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        s.close()
        assert True
    except socket.gaierror:
        assert False, "NO Internet Connection Found"

# 7
def test_imports():
    try:
        import cv2 as cv
        import PIL
        import pytest

        assert True
    except:
        assert False, 'Proper Imports Not Found'

# 8
def test_dupl_certifcates():
    _, _, filenames = next(os.walk('generated_files'))
    files = list(map(lambda x: x.lower(), filenames))
    assert len(files) == len(set(files)), 'You have Duplicate Certificates'

# 9
def test_static_files():
    req_files = ['pass.html', 'fail.html', 'pass.txt', 'fail.txt']
    _, _, filenames = next(os.walk('static'))
    for file in req_files:
        assert file in filenames

# 10
def test_data_file():
    assert os.path.isfile("data.csv"), "Student Data CSV File Missing"

# 11
def test_template_certificate():
    assert os.path.isfile('certificates/CertificateTemplate.jpg'), "Template Certificate Missing"

# 12
def test_package():
    expected_packages = ['certificates', 'data_loader', 'mailing', 'mailing\\login', 'testing\\pretests']
    for package in expected_packages:
        _, _, filenames = next(os.walk(package))
        assert '__init__.py' in filenames

# 13
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

# 14
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

# 15
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

# 16
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

# 17
def test_certificates_names():

    def data_gen():
        with open('data.csv') as csv_file:
            yield from csv_file
    
    *_, filenames = next(os.walk('generated_files'))
    # data -> row string, split -> list, [0] -> name.
    names = {data.split(',')[0].strip().title() for data in data_gen()}
    for file in filenames:
        assert file.split('.')[0] in names 

# 18
def test_certificate_extension():
    *_, filenames = next(os.walk('generated_files'))
    for file in filenames:
        assert file.split('.')[-1] == 'jpg'

# 19
def test_data_loader():

    def data_gen():
        with open('data.csv') as csv_file:
            yield from csv_file

    from data_loader import CSV_loader
    loader = CSV_loader('data.csv')
    act_loader = data_gen()
    for row in loader:
        assert row == next(act_loader).strip()

# 20
def test_printer_register():
    from certificates import Printer
    printer = Printer(('name', 'course', 'date', 'signature'))
    regex = r'^(<function get_cord)'
    print(str(printer().register))
    assert re.match(regex, str(printer().register))