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
    with os.fdopen(os.open('testfile.txt', flags, 0600), 'w') as fout:
        fout.write("secrets!")

Note that it is also important to verify the owner and group of the
file. It is particularly important to note which other users are part of a
group that you grant access to. The best practice is that if group access is
not needed, do not grant it. This is the principle of least privilege.

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
