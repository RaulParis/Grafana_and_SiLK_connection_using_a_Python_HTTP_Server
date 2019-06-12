======================================================
Grafana and SiLK connection using a Python HTTP Server
======================================================


.. image:: https://img.shields.io/pypi/v/Grafana_and_SiLK_connection_using_a_Python_HTTP_Server.svg
        :target: https://pypi.python.org/pypi/Grafana_and_SiLK_connection_using_a_Python_HTTP_Server

.. image:: https://img.shields.io/travis/RaulParis/Grafana_and_SiLK_connection_using_a_Python_HTTP_Server.svg
        :target: https://travis-ci.org/RaulParis/Grafana_and_SiLK_connection_using_a_Python_HTTP_Server

.. image:: https://readthedocs.org/projects/Grafana-and-SiLK-connection-using-a-Python-HTTP-Server/badge/?version=latest
        :target: https://Grafana-and-SiLK-connection-using-a-Python-HTTP-Server.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/RaulParis/Grafana_and_SiLK_connection_using_a_Python_HTTP_Server/shield.svg
     :target: https://pyup.io/repos/github/RaulParis/Grafana_and_SiLK_connection_using_a_Python_HTTP_Server/
     :alt: Updates

.. image:: https://github.com/RaulParis/Grafana_and_SiLK_connection_using_a_Python_HTTP_Server/blob/master/EXAMPLE.png
        :target: https://github.com/RaulParis/Grafana_and_SiLK_connection_using_a_Python_HTTP_Server/blob/master/EXAMPLE.png

This poject contains all the files you need to establish a connection between Grafana and SiLK. The connection uses the Grafana's JSON Data Source and a Python HTTP Server which is shared in the project files.



Features
--------

* Types of panels aviable: Time Graphic, Single Data, Text, Heat Map, Pie chart, World Map.

* Different Grafana variables aviable (In the exported Grafana Dashboard).

* Add your desire SiLK variables at the "Filtro_SILK" just as if you write it on the terminal.

* This project requires to have SiLK and Grafana propertly installed, also Python modules should be installed and the geoip2 module of Python also needs to have downloaded the Database from their website.

* This proyect uses Python 3.6 and need to have installed PySiLK to enable the reading of the filtered files.



STEPS 
--------
* 1 Install Grafana and SilK

* 2 Install Python 3.6 and modules (don't forget to download geoip2 database)

* 3 Install PySiLK and Grafana's JSON datasource

* 4 Start the Grafana server

* 5 Configurate a JSON datasource with your ip or localhost and port 9000 (can be changed)

* 6 Import Grafana's Dashboard called "Grafana_SiLK" which is shared at project files.

* 7 run the server with superuser permission (sudo su).

* 8 Open the dashboard and test it, you can delete and create panels as you want (obviously, you need to have netflow data at SiLK database, if don't, it won't work).

* 9 Share your experience and what could be improved. email: raul.paris.murillo@gmail.com


* Free software: MIT license
* Documentation: https://Grafana-and-SiLK-connection-using-a-Python-HTTP-Server.readthedocs.io.



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
