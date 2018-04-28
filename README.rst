===================
Channeled Dashboard
===================

Proof-of-concept dashboard with realtime notifications

Branches
========

* ``channels1``: `Channels 1 version`_
* ``channels2``: `Channels 2 version`_


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
.. _Channels 1 version: https://speakerdeck.com/yakky/building-real-time-applications-with-django
.. _Channels 2 version: https://speakerdeck.com/yakky/building-real-time-applications-with-django-and-channels-2
