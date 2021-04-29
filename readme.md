# simple_inventory


A self-study project to satisfy my own curiosity regarding user sign-in functionality in Django and how to deploy an app as an AWS EC2 instance.

The app itself is essentially a simple Django app for handling user sign-in, sign-out, register, password change, and password reset operations. AWS SES is used to deliver email for user password resets.

The app is deployed as an AWS EC2 instance using Nginx, Gunicorn, and PostgreSQL on a Ubuntu AMI, and also uses Certbot (Let’s Encrypt) for SSL certification.

Possible improvements: Implement social authentication and allow users to upload profile images, download personal data, and delete their accounts.

[Live demo](https://www.simple-sign-in.app


## To run
* Clone this repo into a location of your choosing.<br>
`git clone https://github.com/4ka0/kudamonoya.git`
* Move into the project folder.<br>
`cd kudamonoya`
* Activate a virtual environment<br>
(Example using venv:)<br>
`python3 -m venv venv`<br>
`source venv/bin/activate`
* Install the dependencies.<br>
`pip install -r requirements.txt`
* Run the tests.<br>
`python manage.py test`
* Run the local server.<br>
`python manage.py runserver`
* Access "localhost:8000" in your browser.<br>
* Go to the home page and log in.<br>

* The project directory contains a file called "sales_data.csv" that can be used for bulk uploading of test sales information.


### Built using:

* Python 3.7.9
* Django 3.1.7
* Bootstrap 4
* Black 20.8b1
* Doverage 5.5
* django-crispy-forms 1.11.1
* Environs 9.3.2
* Freezegun 1.1.0
* Python-dateutil 2.8.1
* Visual Studio Code 1.55.2

### Screenshots:

Home page:</br>
<img src="screenshots/home.png" width="700"></br>

Stock list:</br>
<img src="screenshots/stock-list.png" width="700"></br>

Sale list:</br>
<img src="screenshots/sale-list.png" width="700"></br>

Sale create:</br>
<img src="screenshots/sale-create.png" width="700"></br>

Sale upload:</br>
<img src="screenshots/sale-upload.png" width="700"></br>

Statistics:</br>
<img src="screenshots/stats.png" width="700"></br>
