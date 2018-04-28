===================
Channeled Dashboard
===================

Proof-of-concept dashboard with realtime notifications

Branches
========

* ``channels1``: Channels 1 version [`slides channels 1`_]
* ``channels2``: Channels 2 version [`slides channels 2`_]


Setup
=====

* Ensure `pipenv is installed`_
* Clone the repository::

    git clone https://github.com/yakky/channeled-dashboard

* Enter the project root::

    cd channeled-dashboard


* Create the environment::

    pipenv install

* Activate the environment::

    pipenv shell

* Create the database::

    cd dashboard
    ./manage.py migrate
    ./manage.py createsuperuser

* Run the project::

    ./manage.py runserver 0.0.0.0:8000

* Direct your browser to http://localhost:8000


.. _pipenv is installed: https://docs.pipenv.org/install/
.. _slides channels 1: https://speakerdeck.com/yakky/building-real-time-applications-with-django
.. _slides channels 2: https://speakerdeck.com/yakky/building-real-time-applications-with-django-and-channels-2
