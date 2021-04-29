# simple_inventory

A simple webapp for managing the stock and sales information for an imaginary fruit shop.

You can do the following:
* add, edit, and delete stock information;
* add, edit, and delete sales information;
* batch upload sales information using a csv file; and
* view statistics for the last three days or three months.

[Live demo](https://jjl-simple-inventory.herokuapp.com)

## To run
* Clone this repo into a location of your choosing.<br>
`git clone https://github.com/4ka0/simple_inventory.git`
* Move into the project folder.<br>
`cd simple_inventory`
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
<img src="screenshots/home.png"></br>

Stock list:</br>
<img src="screenshots/stock-list.png"></br>

Sale list:</br>
<img src="screenshots/sale-list.png"></br>

Sale create:</br>
<img src="screenshots/sale-create.png"></br>

Sale upload:</br>
<img src="screenshots/sale-upload.png"></br>

Statistics:</br>
<img src="screenshots/stats.png"></br>
