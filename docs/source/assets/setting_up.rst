********************************
Setting up email ID for the App.
********************************

The App uses two ways to send email using the gmail id. 
First is using the crediantials, which is less secure but we can add an extra layer of security by using App bases passwords, and also the App never stores any password and takes the password from the user when ever required.
The second is the OAuth2 method, but is not yet Implemeneted, and will be implemented in the upcoming realease.

Setting up email for crediantials.
==================================

Goto https://myaccount.google.com/lesssecureapps
And turn on the less secure apps option

.. image :: ../imgs/less_secure.png

Than, go to https://myaccount.google.com/security
And click on 2 step Verification and activate it.

.. image :: ../imgs/2step.png

Now, Since 2 Step Verification is activated, using the App directly will fail, as the SMTP doesn't have option for 2 Step Authentication. So for our app we will add an App password in our gamil to create an exception, this password will be 16 characters unique, and you can use it for the App to send mails.

Select the type as Mail and device as Windows or Other.

.. image :: ../imgs/app_pass.png

This will generate a 16 digit password, you can copy this to use for the program and also as a secret key in Github secrets.

**Note: The app doesn't support copy and pasting when asked in the command prompt for security reasons, and needs to be manually typed.**