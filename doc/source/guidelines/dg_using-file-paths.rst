.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Restrict path access to prevent path traversal
==============================================

Often we will refer to a file on disk or other resource using a path. A path
traversal attack is when an attacker supplies input that gets used with our
path to access a file on the file system that we did not intend. The input
usually attempts to break out of the application's working directory and access
a file elsewhere on the file system. This category of attack can be mitigated
by restricting the scope of file system access and reducing attack surface by
using a restricted file permission profile.

Incorrect
~~~~~~~~~

A typical remote vector for path traversal in web applications might involve
serving or storing files on the file system. Consider the following example:

.. code:: python


    import os
    from flask import Flask, redirect, request, send_file

    app = Flask(__name__)

    @app.route('/')
    def cat_picture():
        image_name = request.args.get('image_name')
        if not image_name:
            return 404
        return send_file(os.path.join(os.getcwd(), image_name))


    if __name__ == '__main__':
        app.run(debug=True)

As the attacker controls the input that is used directly in constructing a path
they are able to access any file on the system. For example consider what
happens if an attacker makes a request like:

::

    curl http://example.com/?image_name=../../../../../../../../etc/passwd

Path traversal flaws also can happen when unpacking a compressed archive of
files. An example of where this has happened within OpenStack is
`OSSA-2011-001 <http://security.openstack.org/ossa/OSSA-2011-001.html>`__. In
this case a tar file from an untrusted source could be unpacked to overwrite
files on the host operating system.

.. code:: python


    import tarfile

    def untar_image(path, filename):
        tar_file = tarfile.open(filename, 'r|gz')
        tar_file.extract_all(path)
        image_file = tar_file.get_names()[0]
        tar_file.close()
        return os.path.join(path, image_file)

Correct
~~~~~~~

The following example demonstrates how you can use python code to restrict
access to files within a specific directory. This can be used as a mechanism to
defeat path traversal.

.. code:: python

    import os
    import sys

    def is_safe_path(basedir, path, follow_symlinks=True):
        # resolves symbolic links
        if follow_symlinks:
            matchpath = os.path.realpath(path)
        else:
            matchpath = os.path.abspath(path)
        return basedir == os.path.commonpath((basedir, matchpath))


    def main(args):
        for arg in args:
            if is_safe_path(os.getcwd(), arg):
                print("safe: {}".format(arg))
            else:
                print("unsafe: {}".format(arg))

    if __name__ == "__main__":
        main(sys.argv[1:])

Another approach to restricting file system access to maintain an indirect
mapping between a unique identifier and a file path that exists on the
operating system. This prevents users supplying malicious input to access
unintended files.

.. code:: python

    localfiles = {
      "01" : "/var/www/img/001.png",
      "02" : "/var/www/img/002.png",
      "03" : "/var/www/img/003.png",
    }

    # Will raise an error if an invalid key is used.
    def get_file(file_id):
      return open(localfiles[file_id])

Consequences
~~~~~~~~~~~~

Not validating file paths allows the attacker to read or write to any file
that the application has access to. This can lead to information leakage and
can be used to pivot to other more serious attacks like remote code execution.

-  `OSSA-2011-001 <http://security.openstack.org/ossa/OSSA-2011-001.html>`__
-  `OSSA-2014-041 <http://security.openstack.org/ossa/OSSA-2014-041.html>`__
-  `OSSA-2015-002 <http://security.openstack.org/ossa/OSSA-2015-002.html>`__

References
~~~~~~~~~~

-  `CWE-22: Improper Limitation of a Pathname to a Restricted
   Directory <http://cwe.mitre.org/data/definitions/22.html>`__
-  `OWASP: Path
   Traversal <https://www.owasp.org/index.php/Path_Traversal>`__
-  `Wikipedia: Directory traversal
   attack <http://en.wikipedia.org/wiki/Directory_traversal_attack>`__
