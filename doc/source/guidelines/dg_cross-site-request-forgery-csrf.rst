.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Use CSRF tokens to avoid CSRF attacks
=====================================

Cross-Site Request Forgery (CSRF) a.k.a. session riding
occurs when sensitive web services have no protection to prevent
attackers arbitrarily submitting data and commands on a website a
user trusts. For example, an attacker may be able to cause an
authorized user to submit form data to a web service which performs
administrative functionality, or modifies personal settings.


Incorrect
~~~~~~~~~

In a typical attack scenario a victim with an existing session of
a legitimate site is tricked into visiting a malicious site
that leverages this session to trigger some action. The snippet below
provides an example of how an attacker might execute such an attack
on a site that doesn't have CSRF token protection in place. The code
below would be hosted on a attackers site, but execute a transfer
on a legitimate users site.

.. code:: html

    <!-- bank.evil.com site -->
    <html>
        <head>
            <title>Malicious website</title>
        </head>
        <body>
            <!-- hehe i'm gonna be rich -->
            <h1>Enter your name to find out your funny nickname:</h1>
            <form action="http://legitimate-site.com/transferfunds" method="POST">
                Your name: <input type="text"><br/>
                <input type="submit">
                <input type="hidden" name="amount" value="10000">
                <input type="hidden" name="recipient" value="evil_hacker">
            </form>
        </body>
    </html>


To protect against this issue, a cryptographically secure nonce or
hash must be included with each request, which must be verified prior to
performing sensitive functionality.

Correct
~~~~~~~

Most web frameworks will provide middleware that is capable of generating
secure CSRF tokens for you. Some of the major ones are summarized below.

Django
^^^^^^

1. Add 'django.middleware.csrf.CsrfViewMiddleware' to MIDDLEWARE_CLASSES in
your configuration *BEFORE* any other middleware that assumes that CSRF
attacks have been dealt with.

2. In any template that user can submit POST data you need to add a special
csrf_token tag.

.. code:: html

    <form action="." method="POST">
        {% csrf_token %}
        <!-- other form fields -->
    </form>

3. Ensure that the csrf context is being passed into any views
being rendered. Is you are not using a RequestContext you will
need to do this manually.

Refer to the `Django documentation <https://docs.djangoproject.com/en/1.8/ref/csrf/#using-csrf>` for more detailed instructions.

Flask-WTF
^^^^^^^^^

Without any configuration, a flask_wtf.Form will be a session secure form
with csrf protection.

Given the following form definition:

.. code:: python

    # form.py
    from flask_wtf import Form
    from wtforms import StringField
    from wtforms.validators import DataRequired

    class PersonForm(Form):
        name = StringField('name', validators=[DataRequired()])


You need only include the form.hidden_tag() in your template definition:

.. code:: html

    <!-- view.html -->
    <form method="POST" action="{{ url_for('submit') }}">
        {{ form.hidden_tag() }}
        {{ form.name.label }} {{ form.name(size=20 }}
        <input type="submit" value="ok">
    </form>

The CSRF token will be validated automatically in any place
you are validating the form submission.

.. code:: python

    # view.py
    from form import PersonForm

    @app.route("/submit", methods=("GET", "POST"))
    def submit():
        f = PersonForm()
        if form.validate_on_submit():
            # csrf token also validated
            return redirect("/")
        return render_template("view.html", form=f)


Consequences
------------

-  Legitimate user sessions can be hijacked
-  Privileged services and functionality can be accessed
-  Protected data can be modified

References
----------

-  `OWASP CSRF Guide <https://www.owasp.org/index.php/CSRF>`__
