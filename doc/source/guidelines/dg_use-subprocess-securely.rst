.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Use subprocess securely
=======================

Many common tasks involve interacting with the operating system - we write a
lot of code that configures, modifies, or otherwise controls the system, and
there are a number of pitfalls that can come along with that.

Shelling out to another program is a pretty common thing to want to do. In most
cases, you will want to pass parameters to this other program. Here is a simple
function for pinging another server.

Incorrect
~~~~~~~~~

.. code:: python

    def ping(myserver):
        return subprocess.check_output('ping -c 1 %s' % myserver, shell=True)

    >>> ping('8.8.8.8')
    64 bytes from 8.8.8.8: icmp_seq=1 ttl=58 time=5.82 ms

This program just supplies a string as a command to the shell, which runs it
without thinking too hard about it. There's no semantic separation between the
input parameters, i.e. the shell cannot tell where the command is supposed to
end, and where the parameters start.

If the ``myserver`` parameter is user controlled, this can be used to execute
arbitrary programs, such as rm:

.. code:: python

    >>> ping('8.8.8.8; rm -rf /')
    64 bytes from 8.8.8.8: icmp_seq=1 ttl=58 time=6.32 ms
    rm: cannot remove `/bin/dbus-daemon': Permission denied
    rm: cannot remove `/bin/dbus-uuidgen': Permission denied
    rm: cannot remove `/bin/dbus-cleanup-sockets': Permission denied
    rm: cannot remove `/bin/cgroups-mount': Permission denied
    rm: cannot remove `/bin/cgroups-umount': Permission denied
    ...

If you choose to test this, we recommend that you pick a command that is less
destructive than 'rm -rf /', such as 'touch helloworld.txt'.

Correct
~~~~~~~

This function can be re-written safely:

.. code:: python

    def ping(myserver):
        args = ['ping', '-c', '1', myserver]
        return subprocess.check_output(args, shell=False)

Rather than passing a string to subprocess, our function passes a list of
strings. The ping program gets each argument separately (even if the argument
has a space in it), so the shell does not process other commands that are
provided by the user after the ping command terminates. You do not have to
explicitly set shell=False - it is the default.

If we test this with the same input as before, the ping command interprets the
``myserver`` value correctly as a single argument, and complains because that
is a really weird hostname to try and ping.

.. code:: python

    >>> ping('8.8.8.8; rm -rf /')
    ping: unknown host 8.8.8.8; rm -rf /

This program is now much safer, even if it has to allow user-provided input.

Consequences
~~~~~~~~~~~~

-  If you use shell=True, your code is extremely likely to be vulnerable
-  Even if *your* code is not vulnerable, the next person who maintains
   can easily introduce a vulnerability.
-  Shell injections are arbitrary code execution - a competent attacker
   will use these to compromise the rest of your system.
