.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Python Pipes to Avoid Shells
============================

You should take a look at the :doc:`shell injection document <dg_use-subprocess-securely>` before this one.

A lot of the time, our codebase uses ``shell=True`` because it's
convenient. The shell provides the ability to pipe things around
without buffering them in memory, and allows a malicious user to chain
additional commands after a legitimate command is run.

Incorrect
~~~~~~~~~

Here is a simple function that uses curl to grab a page from a website, and
pipe it directly to the ``wordcount`` program to tell us how many
lines there are in the HTML source code.

.. code:: python

    def count_lines(website):
        return subprocess.check_output('curl %s | wc -l' % website, shell=True)

    #>>> count_lines('www.google.com')
    #'7\n'

(That output is correct, by the way - the google html source does have
7 lines.)

The function is insecure because it uses ``shell=True``, which allows
:doc:`shell injection <dg_use-subprocess-securely>`. A user to who instructs your
code to fetch the website ``; rm -rf /`` can do terrible things to what
used to be your machine.

If we convert the function to use ``shell=False``, it doesn't work.

.. code:: python

    def count_lines(website):
        args = ['curl', website, '|', 'wc', '-l']
        return subprocess.check_output(args, shell=False)

    # >>> count_lines('www.google.com')
    # curl: (6) Could not resolve host: |
    # curl: (6) Could not resolve host: wc
    # Traceback (most recent call last):
    #  File "<stdin>", line 3, in count_lines
    #  File "/usr/lib/python2.7/subprocess.py", line 573, in check_output
    #    raise CalledProcessError(retcode, cmd, output=output)
    # subprocess.CalledProcessError: Command
    # '['curl', 'www.google.com', '|', 'wc', '-l']' returned non-zero exit status 6

The pipe doesn't mean anything special when shell=False, and so curl
tries to download the website called '\|'. This does not fix the
issue, rather it causes it to be more broken than before.

If we can't rely on pipes if we have shell=False, how should we do this?

Correct
~~~~~~~

.. code:: python

    def count_lines(website):
        args = ['curl', website]
        args2 = ['wc', '-l']
        process_curl = subprocess.Popen(args, stdout=subprocess.PIPE,
                                        shell=False)
        process_wc = subprocess.Popen(args2, stdin=process_curl.stdout,
                                      stdout=subprocess.PIPE, shell=False)
        # Allow process_curl to receive a SIGPIPE if process_wc exits.
        process_curl.stdout.close()
        return process_wc.communicate()[0]

    # >>> count_lines('www.google.com')
    # '7\n'

Rather than calling a single shell process that runs each of our
programs, we run them separately and connect stdout from curl to stdin
for wc. We specify ``stdout=subprocess.PIPE``, which tells subprocess
to send that output to the respective file handler.

Treat pipes like file descriptors (you can actually use FDs if you want)
they may block on reading and writing if nothing is connected to the
other end. That's why we use ``communicate()``, which reads until EOF
on the output and then waits for the process to terminate. You should
generally avoid reading and writing to pipes directly unless you
really know what you're doing - it's easy to work yourself into a situation
that can deadlock.

Note that ``communicate()`` buffers the result in memory - if that's not
what you want, use a file descriptor for ``stdout`` to pipe that output
into a file.

Consequences
------------

-  Using pipes helps you avoid shell injection in more complex
   situations
-  It's possible to deadlock things with pipes (in Python or in shell)

References
----------

-  https://docs.python.org/2/library/subprocess.html#subprocess.Popen.stdin
