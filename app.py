# main.py

from datetime import datetime
from collections import namedtuple
import argparse

import testing.pretests as pretest
from data_loader import CSV_loader
from utils import Print_certificate, mailer

Student = namedtuple('Student', 'name marks email')

def main(sender_mail: str, student_data: CSV_loader, printer: Print_certificate, course_name: str, date: str, fonts: [int,tuple]):
    '''

    '''
    try:
        data = pretest.data_validate(next(student_data))
        if data.check:
            stud = Student(*data.data)
        else:
            print(f'{data.data} is Invalid')
            return main(sender_mail, student_data, printer, course_name, date, fonts) # Next Recursion call.
        
        if int(stud.marks) > 70: #Passing Cutoff
            printer(stud, course_name, date, fonts)
            mailer(sender_mail, stud.email, 'Congratulations on Qualifying', 'static\\pass.html', 'static\\pass.txt', f'generated_files\\{stud.name}.jpg')
        else:
            mailer(sender_mail, stud.email, 'Sorry. You missed the Qualification', 'static\\fail.html', 'static\\fail.txt')
        
        return main(sender_mail, student_data, printer, course_name, date, fonts)
    
    except StopIteration:
        return 0


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="The File Path of Student CSV Data", default='data.csv')
    parser.add_argument("-s", "--sender", help="The sender email id", required= True)
    parser.add_argument('-date', help='Date to be printed on Certificate', default = datetime.today().strftime('%d-%b-%Y'))
    parser.add_argument('-t', '--temp', help='The Template Certificate Image', default="certificates\\CertificateTemplate.jpg")
    parser.add_argument('-c', '--course', help='The Name of the Course', default="Extensive Visual AI Program Phase 4")
    parser.add_argument('-x', '--co_ord', help='All Cordinates as Tuple to be Printed. Blank to Open Selection Box', default=None, type= tuple)

    args = parser.parse_args()
    student_data = CSV_loader(args.data) #args.data_file
    sender_mail = args.sender or "tsaieva4@gmail.com"
    date = args.date
    print_certificate = Print_certificate(args.temp, args.co_ord)
    course_name = args.course
    print(sender_mail)

    main(sender_mail, student_data, print_certificate, course_name, date, (48,48,30,30))