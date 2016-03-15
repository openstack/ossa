.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode

Apply Restrictive File Permissions
==================================

Files should be created with restrictive file permissions to prevent
vulnerabilities such as information disclosure and code execution. In
particular, any files which may contain confidential information
should be set to only permit access by the owning user/service and group
(i.e. no world/other access).

Discretion should be used when granting write access to files such as
configuration files to prevent vulnerabilities including denial of
service and remote code execution.

Incorrect
~~~~~~~~~

Consider the configuration file for a service "secureserv" which stores
configuration including passwords in "secureserv.conf".

.. code:: sh

    ls -l secureserv.conf
    -rw-rw-rw-   1 secureserv  secureserv   6710 Feb 17 22:00 secureserv.conf

Here the file permissions are set to 666 (read and write access for
owner, group, and others). This will allow all users on the system to
have access to the sensitive information contained within the
configuration file.

When writing to a file on a \*NIX operating system using Python, the file
output will be written using the umask that is set for the application.
Depending on your operating system configuration this could be too
permissive when writing sensitive data to file.

Given this program:

.. code:: python

    with open('testfile.txt', 'w') as fout:
        fout.write("secrets!")

The file permissions will default to the environment settings. Here
the umask allows file content to be read by other users on the system.

::

    ls -l testfile.txt
    -rw-r--r--  1 user  staff  4 Feb 19 10:59 testfile.txt

Correct
~~~~~~~

It is preferable to set restrictive permissions for files containing
sensitive information. To fix the example above you would need to set
permissions to make the file only readable and writeable by the user
that created it.

.. code:: sh

    chmod 0600 securesev.conf
    ls -l secureserv.conf
    -rw-------   1 secureserv  secureserv   6710 Feb 17 22:00 secureserv.conf

Below is an example of how you could securely create a file in Python
which is only readable and writable by the owner of that file.

.. code:: python

    import os

    flags = os.O_WRONLY | os.O_CREAT | os.EXLC
    with os.fdopen(os.open('testfile.txt', flags, 0o600), 'w') as fout:
        fout.write("secrets!")

Note that it is also important to verify the owner and group of the
file. It is particularly important to note which other users are part of a
group that you grant access to. The best practice is that if group access is
not needed, do not grant it. This is the principle of least privilege.


Testing guide
~~~~~~~~~~~~~

It should be possible to test anything that performs file creation to make sure
that permissions are being set correctly. The following example inspects that the
file is created with expected permissions and that an exception is raised if the
file already exists.

.. code:: python

    import stat
    import os
    import unittest


    def do_something(path, mode):
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        return os.fdopen(os.open(path, flags, 0o600), mode)

    class TestFileCreation(unittest.TestCase):

        def test_correct_permissions(self):
            """
            Make sure that a file can be created with specific permissions
            """
            test_file = "demo.txt"
            with do_something(test_file, "w") as fout:
                fout.write("blah blah blah")

            finfo = os.stat(test_file)
            assert(finfo.st_mode & stat.S_IRUSR)
            assert(finfo.st_mode & stat.S_IWUSR)
            assert(not finfo.st_mode & stat.S_IXUSR)
            assert(not finfo.st_mode & stat.S_IRGRP)
            assert(not finfo.st_mode & stat.S_IWGRP)
            assert(not finfo.st_mode & stat.S_IXGRP)
            assert(not finfo.st_mode & stat.S_IROTH)
            assert(not finfo.st_mode & stat.S_IWOTH)
            assert(not finfo.st_mode & stat.S_IXOTH)

            os.remove(test_file)

        def test_file_exists(self):
            """
            If the file already exists an OSError should be raised.
            """
            test_file = "demo2.txt"

            # simulate file already placed at location by attacker
            with open(test_file, "w") as fout:
                fout.write("nasty attacker stuff")

            # ensure that we can't open the file
            with self.assertRaises(OSError):
                with do_something(test_file, "w") as fout:
                    fout.write("this should never happen..")

            os.remove(test_file)



You can also use mock to ensure that any calls to os.open are made with
restrictive permissions.

.. code:: python

    import os
    import mock
    import unittest

    def do_something(dummy_file):
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        with os.fdopen(os.open(dummy_file, flags, 0o600), "w") as fout:
            fout.write("blah blah")

        print("doing something")


    class TestUsingMock(unittest.TestCase):

        def test_do_something(self):
            """
            Make sure that any file created is done with sufficiently secure permissions.
            """
            with mock.patch('os.open') as os_open, mock.patch('os.fdopen') as os_fdopen:

                # setup test call
                dummy_file = "dummy.txt"
                os_open.return_value = 123
                do_something(dummy_file)

                # ensure the file is being created with specific flags
                # and permission set
                flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
                os_open.assert_called_with(dummy_file, flags, 0o600)
                os_fdopen.assert_called_with(123, "w")



Consequences
------------

-  Reading passwords from the config file - A malicious user can read
   sensitive information (such as passwords) from the file.
-  Setting a new password - A malicious user can write a new password
   into the file, potentially granting access.
-  Code execution - If the config file stores commands or parameters, a
   malicious user could tamper with the config file to achieve code
   execution.
-  Denial of service - An attacker could delete the contents of the file
   to
   prevent the service from running properly.

References
----------

-  File system controls should be implemented according to `least
   privilege <http://en.wikipedia.org/wiki/Principle_of_least_privilege>`__.
-  More information about setting securing file system permissions in
   Linux can be found
   `here <http://www.linuxsecurity.com/docs/SecurityAdminGuide/SecurityAdminGuide-8.html>`__.
