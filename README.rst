Description
-----------

Breakdown is a lightweight python webserver that parses jinja2 templates.  It's intended to be used by designers for doing rapid prototyping.


Basic Usage
------------

Breakdown needs a ``templates`` directory and a ``static`` directory to serve from.  If your working directory contains these, you can simply run breakdown with no arguments::

    $ breakdown

Or, you can specify the path to a directory containing ``templates`` and ``static``::

    $ breakdown /path/to/project

Breakdown will also work with a django project structure.  If the project path contains an ``apps`` directory, breakdown will automatically detect this and combine the ``static`` and ``templates`` directories for each django app.  You'll also get a listing of the directories it found.  Here's the output of running breakdown on a django project with two apps: 'mainsite' and 'blog'::

    $ breakdown ~/django/myproject
    Serving templates from /Users/josh/django/myproject/apps/mainsite/templates
    Serving static files from /Users/josh/django/myproject/apps/mainsite/static
    Serving templates from /Users/josh/django/myproject/apps/blog/templates
    Serving static files from /Users/josh/django/myproject/apps/blog/static

Viewing Templates
-----------------

Once breakdown is running, it will print the local URL the webserver is listening on::

    Server running at http://127.0.0.1:5000 ...

You can now view templates in your browser by navigating to http://127.0.0.1:5000.  However, you won't see anything here unless one of your template directories contains a file named ``index.html``.  The URL of any template (besides ``index.html``) will be identical to its filename, with all relative paths preserved.  Below is an example of template filenames and their corresponding URL on the local server:

  ==================== ====================================
  **Template**         **URL**
  -------------------- ------------------------------------
  index.html           http://127.0.0.1:5000/
  article.html         http://127.0.0.1:5000/article
  blog/index.html      http://127.0.0.1:5000/blog
  blog/post.html       http://127.0.0.1:5000/blog/post
  ==================== ====================================

*Note: The server will accept template URL's with or without .html appended to them*
    
Advanced
--------

**Command line options**:
  -h, --help            show this help message and exit
  -p PORT, --port=PORT  run server on an alternate port (default is 5000)
  -m, --media           treat MEDIA_URL as STATIC_URL in templates
  -v, --version         display the version number and exit

