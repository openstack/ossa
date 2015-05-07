.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Validate certificates on HTTPS connections to avoid man-in-the-middle attacks
=============================================================================

When developing a module that makes secure HTTPS connections, use a library
that verifies certificates. Many such libraries also provide an option to ignore
certificate verification failures. These options should be exposed to the
OpenStack deployer to choose their level of risk.

Although the title of this guideline calls out HTTPS, verifying the identity of
the hosts you are connecting to applies to most protocols (SSH, LDAPS, etc).

Incorrect
~~~~~~~~~

.. code:: python

    import requests
    requests.get('https://www.openstack.org/', verify=False)

The example above uses verify=False to bypass the check of the certificate
received against those in the CA trust store.

It is important to note that modules such as httplib within the Python
standard library *did not* verify certificate chains until it was fixed
in 2.7.9 release. For more specifics about the modules affected refer
to `CVE-2014-9365 <https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2014-9365>`.

Correct
~~~~~~~

.. code:: python

    import requests
    requests.get('https://www.openstack.org/', verify=CONF.ca_file)

The example above uses the variable CONF.ca\_file to store the location of the
CA trust store, which is used to confirm that the certificate received is from
a trusted authority.

Consequences
~~~~~~~~~~~~

A main-in-the-middle (MITM) attack can allow a party to monitor, copy, and
manipulate all data transferred between the parties. The impact of this depends
on what data is sent. Customer satisfaction survey data will be less valuable
than banking passwords and account information.

-  `OSSA-2014-005 <http://security.openstack.org/ossa/OSSA-2014-005.html>`__

References
~~~~~~~~~~

-  `OSSN-0033 <https://wiki.openstack.org/wiki/OSSN/OSSN-0033>`__
-  https://wiki.openstack.org/wiki/SecureClientConnections
