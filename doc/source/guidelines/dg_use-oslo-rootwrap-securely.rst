.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Use oslo rootwrap securely
==========================

Rootwrap provides a mechanism in which a caller may execute a command line with
escalated privileges (typically as root). Special care must be taken to ensure
this use of code does not permit a lesser privileged user to run commands as
root.

Rootwrap provides a series of filters to restrict command usage to limit the
exposure. The most commonly used filter is CommandFilter, but it also provides
the least amount of restriction on how the command is called.

Consider the following before using rootwrap:

-  Evaluate whether running the command as root is necessary. In some
   cases, another user may be more appropriate.
-  Try to avoid using rootwrap. Look for Python native implementations
   of the required functionality rather than running operating system
   commands.
-  If rootwrap is required, use the most restrictive filter possible
   (typically RegExpFilter).

Incorrect
~~~~~~~~~

An example of insecure usage:

.. code:: python

    # nova/virt/disk/vfs/localfs.py: 'chmod'
    chmod: CommandFilter, chmod, root

This filter is too permissive because it allows the chmod command to be run as
root with any number of arguments, on any file.

Correct
~~~~~~~

An example of more secure usage:

.. code:: python

    # nova/virt/libvirt/utils.py: 'blockdev', '--getsize64', path
    # nova/virt/disk/mount/nbd.py: 'blockdev', '--flushbufs', device
    blockdev: RegExpFilter, blockdev, root, blockdev, (--getsize64|--flushbufs), /dev/.*

Consequences
~~~~~~~~~~~~

-  A user of the API could potentially inject input that might be executed at
   high privileges due to an in-effective rootwrap configuration.

References
~~~~~~~~~~

-  https://wiki.openstack.org/wiki/Rootwrap
