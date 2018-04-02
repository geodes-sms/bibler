To deploy this webservice, you need the current directory files and the BiBler source files.


In the application.py file, you will find two commented lines for which you must replace the
paths before uncommenting.

These paths are needed for the dependencies. First, you need to put the path to the web.py 
framework directory.

#abspath = os.path.dirname("Path to directory where web is located")

The second path is for the location of the BiBler source files. Beware, the webservice needs
BiBler-1.1 source files to work properly.

#abspath = os.path.dirname("Path to Bibler src")

The webservice, Bibler source files and the web.py folder are packaged together.

Once this setup is complete, you will need to deploy on an Apache 2.4 server. The server needs
mod_wsgi, a python module, to work properly. You are encouraged to read further on their
website: https://modwsgi.readthedocs.io/en/develop/

The current Python version used is Python 3.6, make sure your python path pis properly setup
with your Apache's config.

Once the webservice is up and running, you can make http Post requests to the webservice. We
encourage you tu use the php library located in the proxy folder in the current directory. 
This library encapsulates the queries to the webservice. You have to get an instance of the
BiBlerProxy class and use setURL to your webservice's deployment address. After that, you 
may use the other methods contained in BiBlerProxy to make queries by passing the data you
want to be processed. The data expected is a String containing a single BibTeX entry.
