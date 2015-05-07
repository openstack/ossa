.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Unvalidated URL redirect
========================

It is common for web forms to redirect to a different page upon
successful submission of the form data. This is often done using a
*next* or *return* parameter in the HTTP request. Any HTTP parameter
can be controlled by the user, and could be abused by attackers to
redirect a user to a malicious site.

This is commonly used in phishing attacks, for example an attacker
could redirect a user from a legitimate login form to a fake,
attacker controlled, login form. If the page looks enough like the
target site, and tricks the user into believing they mistyped their
password, the attacker can convince the user to re-enter their
credentials and send them to the attacker.

Here is an example of a malicious redirect URL:

::

    https://good.com/login.php?next=http://bad.com/phonylogin.php

To counter this type of attack all URLs must be validated before being
used to redirect the user. This should ensure the redirect will take
the user to a page within your site.

Incorrect
~~~~~~~~~

This example just processes the 'next' argument with no validation:

.. code:: python

    import os
    from flask import Flask,redirect, request

    app = Flask(__name__)

    @app.route('/')
    def example_redirect():
        return redirect(request.args.get('next'))

Correct
~~~~~~~

The following is an example using the Flask web framework. It checks
that the URL the user is being redirected to originates from the same
host as the host serving the content.

.. code:: python

    from flask import request, g, redirect
    from urlparse import urlparse, urljoin


    def is_safe_redirect_url(target):
      host_url = urlparse(request.host_url)
      redirect_url = urlparse(urljoin(request.host_url, target))
      return redirect_url.scheme in ('http', 'https') and \
        host_url.netloc == redirect_url.netloc


    def get_safe_redirect():
      url =  request.args.get('next')
      if url and is_safe_redirect_url(url):
        return url

      url = request.referrer
      if url and is_safe_redirect_url(url):
        return url

      return '/'

The Django framework contains a `django.utils.http.is\_safe\_url <https://github.com/django/django/blob/93b3ef9b2e191101c1a49b332d042864df74a658/django/utils/http.py#L268>`__
function that can be used to validate redirects without implementing a custom version.

Consequences
~~~~~~~~~~~~

-  Unvalidated redirects can make your site a target for phishing
   attacks that can lead to users' credentials being stolen.
-  `OSSA-2012-012 <http://security.openstack.org/ossa/OSSA-2012-012.html>`__

References
~~~~~~~~~~

-  `CWE-601: URL Redirection to Untrusted
   Site <http://cwe.mitre.org/data/definitions/601.html>`__
-  `OWASP Top 10 2013 - Unvalidated redirects and
   forwards <https://www.owasp.org/index.php/Top_10_2013-A10-Unvalidated_Redirects_and_Forwards>`__
