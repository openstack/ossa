.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Avoid dangerous file parsing and object serialization libraries
===============================================================

Many common libraries that are often used for reading configuration
files and deserializing objects are very dangerous because they can
allow execution of arbitrary code. By default, libraries such as
PyYAML and pickle do not provide strong separation of data and code, and thus
allow code to be embedded inside the input.

Often the input to these libraries is untrusted or only partially
trusted. These unsafe inputs can come from configuration files or be
provided via REST APIs. For example, we often use YAML for
configuration files but YAML files can also contain embedded Python code.
This may provide an attacker with a method to execute code.

Many, but not all, of these libraries, offer safe interfaces that
disable features that enable code execution. You always want to use
the safe functions to load input. Often the obvious function to use is not
the safe one and we should check the documentation for libraries not covered
here.

Python Libraries
~~~~~~~~~~~~~~~~

We often use YAML, pickle, or eval to load data into our Python
programs, but this is dangerous. PyYAML has a safe way to load code,
but pickle and eval do not.

+----------+---------------------------------------------+-------------------+-----------------------------+
| Module   | Problem                                     | Use               | Avoid                       |
+==========+=============================================+===================+=============================+
| PyYAML   | Allows creating arbitrary Python objects.   | yaml.safe\_load   | yaml.load                   |
+----------+---------------------------------------------+-------------------+-----------------------------+
| pickle   | Allows creating arbitrary Python objects.   | Do not use        | pickle.load, pickle.loads   |
+----------+---------------------------------------------+-------------------+-----------------------------+
| cPickle  | Allows creating arbitrary Python objects.   | Do not use        | cPickle.load, cPickle.loads |
+----------+---------------------------------------------+-------------------+-----------------------------+
| eval     | Runs all input as Python code               | Do not use        | eval                        |
+----------+---------------------------------------------+-------------------+-----------------------------+
| exec     | Runs all input as Python code (Python 3.x)  | Do not use        | exec                        |
+----------+---------------------------------------------+-------------------+-----------------------------+


Incorrect
~~~~~~~~~

yaml.load is the obvious function to use but it is dangerous:

.. code:: python

    import yaml
    import pickle
    conf_str = '''
    !!python/object:__main__.AttackerObj
    key: 'value'
    '''
    conf = yaml.load(conf_str)

Using pickle or cPickle with untrusted input can result in arbitrary
code execution.

.. code:: python

    import pickle
    import cPickle

    user_input = "cos\nsystem\n(S'cat /etc/passwd'\ntR.'\ntR."
    cPickle.loads(user_input) # results in code execution
    pickle.loads(user_input)  # results in code execution

Similarly eval and exec are difficult to use safely with
input that comes from an untrusted source.

.. code:: python

    user_input = "os.system('cat /etc/passwd')"
    eval(user_input) # execute python expressions

    user_input = "import os; os.system('cat /etc/passwd')"
    exec(user_input) # execute _any_ python code


Correct
~~~~~~~

Here we use PyYAMLs safe YAML loading function:

.. code:: python

    import yaml
    conf_str = '''
    - key: 'value'
    - key: 'value'
    '''
    conf = yaml.safe_load(conf_str)

There is no safe alternative for pickle.load. However in most cases using
pickle for serialization of data objects is something that can be avoided
altogether.

Consequences
------------

-  Anyone that can control the input passed to dangerous libraries can
   gain arbitrary code execution on the system running the dangerous
   library.

References
----------

-  `PyYAML: Loading
   YAML <http://pyyaml.org/wiki/PyYAMLDocumentation#LoadingYAML>`__
-  `Why Python Pickle is
   Insecure <http://michael-rushanan.blogspot.com/2012/10/why-python-pickle-is-insecure.html>`__
-  `Exploiting misuse of Python's
   "pickle" <https://blog.nelhage.com/2011/03/exploiting-pickle/>`__
