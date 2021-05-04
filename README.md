# AutoCertify
Automating Certificate Creation 

## Objective:
The application automates the entire task Creating Certificates and mailing each student indivdually based on marks from the Student's Database(.csv).

The app should be able to be run from command line or directly running the script.

The app can be provided with a template certificate Image, which will be used to print all the students details. The template which is used by default is:  
<img src="certificates/CertificateTemplate.jpg" alt="Certificate" width="500"/>

## Data
The Student data, should be in .csv
```
name, marks, email
```
The marks should be between 0 to 100, rejects the record where the marks are not in the range.  
The Application will check for proper name format and email format, and reject the row with invalid details.

## Getting Started.
The Application requires t ohave Python 3 installed, preferably Python 3.9 and above.  
As this application was developed and tested on Python 3.9

To download Python:
[Download Python](https://www.python.org/downloads/)

Also the Script uses other Python libraries:
* numpy ```pip install numpy```
* open-cv ```pip install opencv-pytohn```
* Pillow ```pip install Pillow```

## Under Development
The application is still under testing and test cases are being developed, and the README will be updated soon with entire How to Use.
