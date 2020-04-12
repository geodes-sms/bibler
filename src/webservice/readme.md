# BiBler Web Service

## Dependencies
- [Apache sever](https://httpd.apache.org/) 2.4 or later
- [mod_wsgi](https://modwsgi.readthedocs.io/en/develop)

## Setup

To deploy this web service, you need the current directory files and the BiBler source files.
In the application.py file, you will find two commented lines for which you must replace the paths before uncommenting.
These paths are needed for the dependencies.
First, you need to put the path to the ```web.py`` framework directory.
```python
abspath = os.path.dirname("Path to directory where web is located")
```

The second path is for the location of the BiBler source files.
Beware, the webservice needs BiBler source files to work properly.
```python
#abspath = os.path.dirname("Path to Bibler src")
```

The webservice, Bibler source files and the `web.py` folder are packaged together.

Once this setup is complete, you will need to deploy on an Apache 2.4 server.
The server needs the Python module [`mod_wsgi`](https://modwsgi.readthedocs.io/en/develop) to work properly.
You are encouraged to read further on their website.

The current Python version used is Python 3.6, make sure your Python path is properly setup with your Apache's config.

## Usage
Once the web service is up and running, you can make HTTP Post requests to the web service.
We encourage you to use the PHP library [`proxy/bibler.php`](proxy/bibler.php). 
This library encapsulates the queries to the webservice.
You have to get an instance of the `BiBlerProxy` class and use `setURL` to the deployment address of your web service.
You may then use the other functions contained in `BiBlerProxy` to make queries by passing the data you want to be processed.
The expected data is a string containing a single BibTeX entry.