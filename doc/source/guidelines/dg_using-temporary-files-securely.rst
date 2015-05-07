.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Create, use, and remove temporary files securely
================================================

Often we want to create temporary files to save data that we can't hold in
memory or to pass to external programs that must read from a file. The obvious
way to do this is to generate a unique file name in a common system temporary
directory such as /tmp, but doing so correctly is harder than it seems. Safely
creating a temporary file or directory means following a number of rules (see
the references for more details). We should never do this ourselves but use the
correct existing library function. We also must take care to cleanup our
temporary files even in the face of errors.

If we don't take all these precautions we open ourselves up to a number of
dangerous security problems. Malicious users that can predict the file name and
write to directory containing the temporary file can effectively hijack the
temporary file by creating a symlink with the name of the temporary file before
the program creates the file itself. This allows a malicious user to supply
malicious data or cause actions by the program to affect attacker chosen files.
The references have more extensive descriptions of potential dangers.

Most programming lanuages provide functions to create temporary files. However,
some of these functions are unsafe and should not be used. We need to be
careful to use the safe functions.

Despite the safer temporary file creation APIs we must still be aware of where
we are creating tempory files. Generally, temporary files should always be
created on the local filesystem. Many remote filesystems (for example, NFSv2)
do not support the open flags needed to safely create temporary files.

Python
~~~~~~

=========================== ===============
Use                         Avoid
=========================== ===============
tempfile.TemporaryFile      tempfile.mktemp
tempfile.NamedTemporaryFile open
tempfile.SpoolTemporaryFile
tempfile.mkstemp
tempfile.mkdtemp
=========================== ===============

tempfile.TemporaryFile should be used whenever possible. Besides creating
temporary files safely it also hides the file and cleans up the file
automatically.

Incorrect
~~~~~~~~~

Creating temporary files with predictable paths leaves them open to time of
check, time of use attacks (TOCTOU). Given the following code snippet an
attacker might pre-emptively place a file at the specified location.

.. code:: python

    import os
    import tempfile

    # This will most certainly put you at risk
    tmp = os.path.join(tempfile.gettempdir(), filename)
    if not os.path.exists(tmp):
        with open(tmp, "w") file:
            file.write("defaults")

There is also an insecure method within the Python standard library that cannot
be used in a secure way to create temporary file creation.

.. code:: python

    import os
    import tempfile

    open(tempfile.mktemp(), "w")

Finally there are many ways we could try to create a secure filename that will
not be secure and is easily predictable.

.. code:: python


    filename = "{}/{}.tmp".format(tempfile.gettempdir(), os.getpid())
    open(filename, "w")

Correct
~~~~~~~

The Python standard library provides a number of secure ways to create
temporary files and directories. The following are examples of how you can use
them.

Creating files:

.. code:: python

    import os
    import tempfile

    # Use the TemporaryFile context manager for easy clean-up
    with tempfile.TemporaryFile() as tmp:
        # Do stuff with tmp
        tmp.write('stuff')

    # Clean up a NamedTemporaryFile on your own
    # delete=True means the file will be deleted on close
    tmp = tempfile.NamedTemporaryFile(delete=True)
    try:
        # do stuff with temp
        tmp.write('stuff')
    finally:
        tmp.close()  # deletes the file

    # Handle opening the file yourself. This makes clean-up
    # more complex as you must watch out for exceptions
    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w') as tmp:
            # do stuff with temp file
            tmp.write('stuff')
    finally:
        os.remove(path)

We can also safely create a temporary directory and create temporary files
inside it. We need to set the umask before creating the file to ensure the
permissions on the file only allow the creator read and write access.

.. code:: python

    import os
    import tempfile

    tmpdir = tempfile.mkdtemp()
    predictable_filename = 'myfile'

    # Ensure the file is read/write by the creator only
    saved_umask = os.umask(0077)

    path = os.path.join(tmpdir, predictable_filename)
    print path
    try:
        with open(path, "w") as tmp:
            tmp.write("secrets!")
    except IOError as e:
        print 'IOError'
    else:
        os.remove(path)
    finally:
        os.umask(saved_umask)
        os.rmdir(tmpdir)

Consequences
~~~~~~~~~~~~

-  The program can be tricked into performing file actions against the
   wrong file or using a malicious file instead of the expected
   temporary
   file

References
~~~~~~~~~~

-  `Temporary File - CERT Secure Coding
   Standards <https://www.securecoding.cert.org/confluence/download/attachments/3524/07.5+Temporary+Files+v2.pdf>`__
-  `FIO21-C. Do not create temporary files in shared
   directories <https://www.securecoding.cert.org/confluence/display/seccode/FIO21-C.+Do+not+create+temporary+files+in+shared+directories>`__
-  `FIO03-J. Remove temporary files before
   termination <https://www.securecoding.cert.org/confluence/display/java/FIO03-J.+Remove+temporary+files+before+termination>`__
-  `CWE-377: Insecure Temporary
   File <http://cwe.mitre.org/data/definitions/377.html>`__
-  `CWE-379: Creation of Temporary File in Directory with Incorrect
   Permissions <http://cwe.mitre.org/data/definitions/379.html>`__
-  `CWE-459: Incomplete
   Cleanup <http://cwe.mitre.org/data/definitions/459.html>`__
-  `Python tempfile <https://docs.python.org/2/library/tempfile.html>`__
