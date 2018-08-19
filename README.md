## How to run 
* Clone this repo on your local device using *git clone https://github.com/JDTorresP/AgileDjango.git*

Follow the next command line expressions for the initial configuration on linux systems, commands may vary depending on your operating system

* pip install virtualenv
* cd gallery
* virtualenv -p /usr/bin/python2.7 env
* cd env
* source bin/activate
* pip install django
* pip install psycopg2
* cd ..
* python manage.py runserver

Now the server is runing at 
http://127.0.0.1:8000/admin
