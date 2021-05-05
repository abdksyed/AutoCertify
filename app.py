# main.py

from datetime import datetime
from collections import namedtuple
import argparse

import testing.pretests as pretest
from data_loader import CSV_loader
from utils import Print_certificate, mailer

Student = namedtuple('Student', 'name marks email')

def batch_mode(sender_mail: str, student_data: CSV_loader, printer: Print_certificate, course_name: str, date: str, fonts: [int,tuple]):
    '''

    '''
    try:
        data = pretest.data_validate(next(student_data))
        if data.check:
            stud = Student(*data.data)
        else:
            print(f'{data.data} is Invalid')
            return batch_mode(sender_mail, student_data, printer, course_name, date, fonts) # Next Recursion call.
        
        if int(stud.marks) > 70: #Passing Cutoff
            printer(stud, course_name, date, fonts)
            mailer(sender_mail, stud.email, 'Congratulations on Qualifying', 'static\\pass.html', 'static\\pass.txt', f'generated_files\\{stud.name}.jpg')
        else:
            mailer(sender_mail, stud.email, 'Sorry. You missed the Qualification', 'static\\fail.html', 'static\\fail.txt')
        
        return batch_mode(sender_mail, student_data, printer, course_name, date, fonts)
    
    except StopIteration:
        print('All the Certificates of valid data has been generated and mailed Successfully.')
        return 0

def single_mode(sender_mail: str, student_data: str, printer: Print_certificate, course_name: str, date: str, fonts: [int,tuple]):
    '''
    '''
    data = pretest.data_validate(student_data)
    print(data)
    if data.check:
        stud = Student(*data.data)
    else:
        raise ValueError(f'{data.data} is Invalid')

    if int(stud.marks) > 70: #Passing Cutoff
        printer(stud, course_name, date, fonts)
        mailer(sender_mail, stud.email, 'Congratulations on Qualifying', 'static\\pass.html', 'static\\pass.txt', f'generated_files\\{stud.name}.jpg')
    else:
        mailer(sender_mail, stud.email, 'Sorry. You missed the Qualification', 'static\\fail.html', 'static\\fail.txt')
    
    print('Certificate Created and Mailed!')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='AutoCertify')
    parser.add_argument("-s", "--sender", help="The sender email id", required= True)
    parser.add_argument('-date', help='Date to be printed on Certificate', default = datetime.today().strftime('%d-%b-%Y'))
    parser.add_argument('-t', '--temp', help='The Template Certificate Image', default="certificates\\CertificateTemplate.jpg")
    parser.add_argument('-c', '--course', help='The Name of the Course', default="Extensive Visual AI Program Phase 4")
    parser.add_argument('-x', '--co_ord', help='All Cordinates as Tuple to be Printed. Blank to Open Selection Box', default=None, type= tuple)

    sub_parser = parser.add_subparsers(title='Modes', description= 'Different Types of Creating Certificates & Sending Mails',  dest= 'mode')
    
    single_parser = sub_parser.add_parser('single', help='Create and Send certificates to single student.')
    single_parser.add_argument('-n', '--name', help='The receiver email id', required= True)
    single_parser.add_argument('--score', help='The score of the Student', required= True)
    single_parser.add_argument('-r', '--receiver', help='The name of the Student', required= True)

    batch_parser = sub_parser.add_parser('batch', help='Create and Send certificates to batch of student.')
    batch_parser.add_argument("-d", "--data", help="The File Path of Student CSV Data", default='data.csv')
    
    args = parser.parse_args()
    sender_mail = args.sender
    date = args.date
    print_certificate = Print_certificate(args.temp, args.co_ord)
    course_name = args.course
    print(args.mode)

    if args.mode == 'single':
        student_data = ', '.join((args.name, args.score, args.receiver))
        print(student_data)
        single_mode(sender_mail, student_data, print_certificate, course_name, date, (48,48,30,30))
    elif args.mode == 'batch':
        student_data = CSV_loader(args.data) #args.data_file
        batch_mode(sender_mail, student_data, print_certificate, course_name, date, (48,48,30,30))

    