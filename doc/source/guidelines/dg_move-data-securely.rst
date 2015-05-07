.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Use secure channels for transmitting data
=========================================

Data in transit over networks should be protected wherever possible.
Although some data may not appear to have strong confidentiality or
integrity requirements it is best practice to secure it.

When building any application that communicates over a network we have
to assume that we do not control the network that the data travels
over. We should consider that the network may have hostile actors who will
attempt to view or change the data that we are transmitting.

 Clear Example
~~~~~~~~~~~~~~

OpenStack API calls often contain credentials or tokens that are very
sensitive. If they are sent in plaintext they may be modified or
stolen.

It is very important that API calls are protected from malicious third
parties viewing them or tampering with their content - even for
communications between services on an internal network.

 Less Obvious Example
~~~~~~~~~~~~~~~~~~~~~

Consider a server process that reports the current number of stars in
the sky and sends the data over the network to clients using a simple
webpage. There is no strong confidentiality requirement for this; the
data is not secret. However integrity is important. An attacker on the
network could alter the communications going from the server to
clients and inject malicious traffic such as browser exploits into the HTTP
stream, thus compromising vulnerable clients.

Incorrect
~~~~~~~~~

.. code:: python

    cfg.StrOpt('protocol',
               default='http',
               help='Default protocol to use when connecting to glance.'),

Correct
~~~~~~~

.. code:: python

    cfg.StrOpt('protocol',
               default='https',
               help='Default protocol to use when connecting to glance.'),

Consequences
~~~~~~~~~~~~

-  Unencrypted secrets can be stolen
-  Unsecured connections can lead to system compromise
-  A man-in-the-middle attacker can alter data over unsecure connections
-  A less knowledgeable deployer of OpenStack may inadvertently use
   unsecure connections on a public network.

References
~~~~~~~~~~

-  `Securing Rest
   APIs <https://stormpath.com/blog/secure-your-rest-api-right-way/>`__
-  `Further reasons to encrypt web
   traffic <http://chapterthree.com/blog/why-your-site-should-be-using-https>`__
