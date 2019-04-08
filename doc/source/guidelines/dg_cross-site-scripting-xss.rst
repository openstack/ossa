.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Escape user input to prevent XSS attacks
========================================

These days, almost every service we create has some form of web
interface, be it for administration, monitoring or for the core
functionality of the service. These interfaces are becoming ever
more complex and dynamic, and increasingly interactive. There is
a risk however, when increasing interactivity of these web services,
that we inadvertently allow a user to supply data which can corrupt,
or disrupt the normal running of that service.

Cross-Site Scripting (XSS) is a class of vulnerability whereby an attacker
is able to present active web content to a web service, which is
subsequently echoed back to a user and executed by the browser.
This content can be as seemingly benign as an embarrassing image or
text, or as malign as browser based exploits intended to steal and
utilize the user's web session, or even compromise the user's web browser
and take control of their client system.

There are three main classes of XSS issue: Persistent, Reflected and
DOM-Based. Persistent XSS issues are those where user input is stored
by the server, either in a database or server files, which is later
presented to any user visiting the affected web page. Reflected XSS
issues are those where user input in a request is immediately
reflected to the user without sanitization.

DOM-Based issues are less common, and are present in web applications
with rich client-side JavaScript clients which generate dynamic code or web
content using user controllable data (i.e. URL parameters).

When developing web applications, we must be extremely careful to
protect against all these classes of issue. To do so, we must never trust any
data that originates from, or can be controlled by, the client. All data
must be sanitized in a way suitable for how that data is going to be used. To
do so, many languages provide built-in functionality to make sure any
potentially dangerous control characters are encoded in a way to render them
inactive. The following is a PHP example of this.

Incorrect
~~~~~~~~~

The following is a contrived example of how a reflected XSS exploit may
occur. If an attacker were to submit a request to
'http://example.com/?name=<script>alert(1)</script>' then any user viewing that
url would have the javascript executed within the context of their browser. This can
be used for malicious purposes.

.. code:: python

    # flask example
    @app.route("/")
    def hello():
        name = request.args.get('name')
        return "Hello %s" % name


Most modern Python web frameworks will escape any input that is rendered
via templates which mitigates the majority of these types of attacks.
However there are ways that this can be disabled.

<!-- by default flask will html escape var -->
<p>{{ var }}</p>

<!-- in this instance it will not! -->
<p>{{ var | safe }}</p>


Correct
~~~~~~~

The correct way to prevent XSS attacks is to validate user input and ensure
that data rendered by templates is escaped. Using templates in the way
they are intended is preferable:

.. code:: python

    # flask example
    @app.route("/")
    def hello():
        name = request.args.get('name')
        return render('hello.html', name=name)

    # where hello.html is:
    # <html>Hello {{ name }}</html>


Any HTML content that is generated directly within a request handler
should use the appropriate escaping function:

.. code:: python

    from flask import escape
    @app.route("/")
    def hello():
        name = request.args.get('name')
        return "Hello %s" % escape(name)



Allowing certain special characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The issue is made more complex when we encounter situations where we
need to allow a specific set of special characters, such as the ability to
post content containing HTML tags. In this situation we can either accept only
known good data, or we can deny all known bad data. Both approaches have pros and
cons, with the specific choice of implementation being dependent on the
given application. In general however, the following should be the list of
priorities:

#. Encoding - Replace ALL control characters with known safe
   alternatives
#. Positive validation (whitelist) - Only allow a specific set of values
#. Negative validation (blacklist) - Block a specified list of dangerous
   values

In cases where positive validation is used, it should also be coupled
with additional sanitization. For example, when allowing certain HTML tags,
certain attributes of those tags should be removed, such as event handlers.
e.g.:

.. code:: html

    <img src='someimage.jpg' onload='do_evil()'/>

Again, the preferable approach is to only allow known safe attributes,
and sanitize the content of those attribute values. If the content is not
sanitized, the following vulnerable code could occur:

.. code:: none

    function add_image(link) {
      document.write('<img src="' + link + '"'></img>'');
    }

If the preceding JavaScript function is called with the link parameter
containing the following value, the function can be exploited to execute
arbitrary code:

::

    x" onerror="do_evil()

A more secure implementation of the above would be:

.. code:: none

    function add_image(link) {
      clean = link.replace(/"/g, '&quot;');
      document.write('<img src="' + clean + '"'></img>'');
    }

Note, this is a very specific example for illustration. A more
comprehensive approach to sanitization should be taken for larger applications.

Consequences
------------

-  Hijack of legitimate user sessions
-  Disclosure of sensitive information
-  Access to privileged services and functionality
-  Delivery of malware and browser exploits from our trusted domain

References
----------

-  `OWASP XSS
   Guide <https://www.owasp.org/index.php/Cross-site_Scripting_%28XSS%29>`__
-  `OWASP Data Validation
   Guide <https://www.owasp.org/index.php/Data_Validation>`__
