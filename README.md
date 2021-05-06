# AutoCertify
Automating Certificate Creation 

## Objective:
The application automates the entire task Creating Certificates and mailing each student indivdually based on marks from the Student's Database(.csv).

The app should be able to be run from command line or directly running the script.

The app can be provided with a template certificate Image, which will be used to print all the students details. The template which is used by default is:  


## Quick 5 minute Demo.
Click on the Image to go to the Demo Video!

<a href = "https://www.youtube.com/watch?v=9Mq26r7OAxs">
    <img src="certificates/CertificateTemplate.jpg" alt="Certificate" width="500"/>
</a>

## Data
The Student data, should be in .csv
```
name, marks, email
```
The marks should be between 0 to 100, rejects the record where the marks are not in the range.  
The Application will check for proper name format and email format, and reject the row with invalid details.

## Getting Started.

### Before Getting Started:
The Application requires to have Python 3 installed, preferably Python 3.9 and above.  
As this application was developed and tested on Python 3.9

To download Python:
[Download Python](https://www.python.org/downloads/)

Also the Script uses other Python libraries:
* numpy ```pip install numpy```
* open-cv ```pip install opencv-pytohn```
* Pillow ```pip install Pillow```
* Pytest ```pip install pytest```

The application automatically takes care of the libraries and ask user pemission to install them, if they are not present before running the application.  
Also, the application send mails to the students, so it check for Internet connection before procedding, and will raise an error it there is no active internet connection.

### Running from Command Line
To get help on the command line application, run the command:
```
python app.py -h
```
output

    usage: AutoCertify [-h] -s SENDER [-date DATE] [-t TEMP] [-c COURSE] [-x CO_ORD] {single,batch} ...

    optional arguments:
    -h, --help            show this help message and exit
    -s SENDER, --sender SENDER
                            The sender email id
    -date DATE            Date to be printed on Certificate
    -t TEMP, --temp TEMP  The Template Certificate Image
    -c COURSE, --course COURSE
                            The Name of the Course
    -x CO_ORD, --co_ord CO_ORD
                            All Cordinates as Tuple to be Printed. Blank to Open Selection Box

    Modes:
    Different Types of Creating Certificates & Sending Mails

    {single,batch}
        single              Create and Send certificates to single student.
        batch               Create and Send certificates to batch of student.


#### Lets drill down on each variable:
```
-s SENDER, --sender SENDER The sender email id
```
This is a MANDATORY keyword argument, and it is the gmail id which is to be used to send the mails from. While running the program it will ask for your gmail passowrd.

```
-date
```
The date to be printed on the Certificate, it's optional and if not given it used Python Date Time module to take current date.

```
-t --temp
```
The Path of the Template Certificate, it is optional and if not given will take the template certificate from the project, in the certificate package.

```
-c --course
```
The name of the course, it's optional argument and if not given will take "Extensive Visual AI Program Phase 4" as name of the course.

```
-x --co_ord
```
The co ordinates of the points where the data is to be printed. This is also optional, if not given it will open a window to take user input.
The user will be prompted for each individual field to **double click at the bottom middle** point where the particular entity is to be printed.

#### Modes

This is mandatory argument which needs to selected after passing the main arguments (which are parent argument), select any one type of mode.
The two available modes are **single** and **batch**

To create and send certificate for one student, use **single** mode.  
To get help on single mode arguments run:
```
python app.py single -h
```
output

    usage: AutoCertify single [-h] -n NAME --score SCORE -r RECEIVER

    -h, --help            show this help message and exit
    -n NAME, --name NAME  The receiver email id
    --score SCORE         The score of the Student
    -r RECEIVER, --receiver RECEIVER
                            The name of the Student

```
-n --name
```
The name of the student, which need to be printed on the certificate. This is mandatory argument

```
--score
```
The score of the student, the program check based on this score if the student qualified or not for the course. This is also mandatory argument

```
-r --receiver
```
The email address of the student, to which the mail is not be send. This is also mandatory argument

To create and send certificates for a batch of students, use **batch** mode.
To get help on batch mode arguments run:
```
python app.py batch -h
```
output

    optional arguments:
        -d DATA, --data DATA  The File Path of Student CSV Data

The only required argument for batch mode, is the path to the CSV file of the database.
The argument is optional and if not given will take the default data.csv file present in the project directory.
