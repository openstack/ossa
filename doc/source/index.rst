====================
 OpenStack Security
====================

Security is a fundamental goal of the OpenStack architecture and needs to
be addressed at all layers of the stack. Like any complex, evolving system
security has to be vigilantly pursued, and exposures eliminated. We need
your help.

If you think you've identified a vulnerability, please work with us to
rectify and disclose the issue responsibly.

Recent OpenStack Security Advisories
------------------------------------

.. toctree::
   :maxdepth: 1
   :glob:

   ./ossa/*

You can find the complete list of published advisories here:

.. toctree::
   :maxdepth: 1
   :glob:

   ossalist

How to Report Security Issues to OpenStack
------------------------------------------

We provide two ways to report issues to the OpenStack Vulnerability Management
Team depending on how sensitive the issue is:

* Open a bug in Launchpad and mark it as a 'security bug'. This will make the
  bug Private and only accessible to the Vulnerability Management Team.

* If the issue is extremely sensitive, please send an encrypted email to one
  of the Team's members. Their GPG keys can be found below, and are also
  available from popular public GPG key servers.

  * Jeremy Stanley (jeremy@openstack.org): `GPG key for Jeremy`_
  * Tristan Cacqueray (tristan.cacqueray@enovance.com): `GPG key for Tristan`_
  * Thierry Carrez (thierry@openstack.org): `GPG key for Thierry`_
  * Grant Murphy (grant.murphy@hp.com): `GPG key for Grant`_

.. _`GPG key for Jeremy`: http://keyserver.ubuntu.com:11371/pks/lookup?search=0x48f9961143495829

.. _`GPG key for Tristan`: http://keyserver.ubuntu.com:11371/pks/lookup?search=0x925CC5D8

.. _`GPG key for Thierry`: http://keyserver.ubuntu.com:11371/pks/lookup?search=0x22A7943050DB1E67EC2B641A507AF89025B10423&op=index

.. _`GPG key for Grant`: http://keyserver.ubuntu.com:11371/pks/lookup?search=0x551a2252

OpenStack Vulnerability Management Team
---------------------------------------

The OpenStack Vulnerability Management team is a very small group of experts
in vulnerability management drawn from the OpenStack community. Our job is
facilitating the reporting of vulnerabilities, coordinating security fixes
and handling progressive disclosure of the vulnerability information.
Specifically, we are responsible for the following functions:

* Vulnerability Management: All vulnerabilities discovered by community
  members (or users) can be reported to the Team.

* Vulnerability Tracking: The Team will curate a set of vulnerability related
  issues in the issue tracker. Some of these issues will be private to the
  Team and the affected product leads, but once remediated, all vulnerabilities
  will be public.

* Responsible Disclosure: As part of our commitment to work with the security
  community, the Team will ensure that proper credit is given to security
  researchers who responsibly report issues in OpenStack.

.. seealso::

  See the Vulnerability_Management_ page in the wiki for details on our
  open process.

.. _Vulnerability_Management: https://wiki.openstack.org/wiki/Vulnerability_Management

Other Security Teams in OpenStack
---------------------------------

Other teams of security-conscious people in the OpenStack community work
together to improve security in OpenStack, in particular working on:

* Introduce security improvements - Brainstorm and implement security
  improvements for OpenStack core projects.

* Audits - Coordinate security auditing efforts between members.

* Facilitation - Support security products and vendors wanting to be part of
  the OpenStack community.

See the `Security Teams`_ wiki page for the full list of security-oriented
teams you can join.

.. _Security Teams: http://wiki.openstack.org/SecurityTeams
