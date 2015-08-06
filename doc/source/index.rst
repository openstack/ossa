.. :Copyright: 2015, OpenStack Vulnerability Management Team
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode

====================
 OpenStack Security
====================

.. toctree::
   :hidden:

   vmt-process


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

* Search for the corresponding project at https://launchpad.net/ and after
  selecting it, click the 'Report a bug' link at the right. Fill in the
  'Summary' and 'Further information' fields describing the issue, then
  click the 'This bug is a security vulnerability' checkbox near the bottom
  of the page before submitting it. This will make the bug Private and only
  accessible to the Vulnerability Management Team.

* If the issue is extremely sensitive, please send an encrypted email to one
  of the Team's members. Their GPG keys can be found below, and are also
  available from popular public GPG key servers.

  * Jeremy Stanley (jeremy@openstack.org): `GPG key for Jeremy`_
  * Tristan Cacqueray (tdecacqu@redhat.com): `GPG key for Tristan`_
  * Grant Murphy (grant.murphy@hp.com): `GPG key for Grant`_

.. _`GPG key for Jeremy`: http://keyserver.ubuntu.com:11371/pks/lookup?search=0x48f9961143495829

.. _`GPG key for Tristan`: http://keyserver.ubuntu.com:11371/pks/lookup?search=0x925CC5D8

.. _`GPG key for Grant`: http://keyserver.ubuntu.com:11371/pks/lookup?search=0x551a2252


How to Propose and Review a Security Patch
------------------------------------------

.. note::

    The patch development and review process for security patches is different
    from normal patches in OpenStack. Because the gerrit review process is
    public, all security bugs must have patches proposed to and reviewed in
    the Launchpad bug report comments.

After a patch for the reported bug has been developed locally, you the patch author need to share that with the community. This is a simple process, but it is different than the normal OpenStack workflow.

* Export it using the `format-patch` command::

    git format-patch --stdout HEAD~1 >path/to/local/file.patch

  Now you have the patch saved locally and you can attach it in a comment
  on the Launchpad bug page.

* For reviewers, to review that attached patch, run the following command::

    git am <~path/to/local/file.patch

  This applies the patch locally as a commit, including the commit message,
  author, date, and all other metadata. However, if the patch author did
  not use `format-patch` to export the patch (perhaps they only used
  `git show >local.patch`), then the patch can be applied locally with::

    git apply path/to/local/file.patch


OpenStack Security Team
-----------------------

The OpenStack security team runs an number of initiatives aimed at improving
the overall security of OpenStack projects and ensuring that security incidents
are handled in a coordinated fashion.  Key initiatives that fall within the
security team's areas of responsibility are outlined below.


Vulnerability Management
~~~~~~~~~~~~~~~~~~~~~~~~

An autonomous subgroup of vulnerability management specialists with in the
security team make up the OpenStack vulnerability management team (VMT).
Their job is facilitating the reporting of vulnerabilities, coordinating
security fixes and handling progressive disclosure of the vulnerability
information. Specifically, they are responsible for the following functions:

* Vulnerability Management: All vulnerabilities discovered by community
  members (or users) can be reported to the Team.

* Vulnerability Tracking: The Team will curate a set of vulnerability related
  issues in the issue tracker. Some of these issues will be private to the
  Team and the affected product leads, but once remediated, all vulnerabilities
  will be public.

* Responsible Disclosure: As part of our commitment to work with the security
  community, the Team will ensure that proper credit is given to security
  researchers who responsibly report issues in OpenStack.

See :doc:`vmt-process` for details on our open process.


OpenStack Security Notes
~~~~~~~~~~~~~~~~~~~~~~~~

Security Notes advise users of security related issues. Security notes are
similar to advisories; they often address vulnerabilities in 3rd party tools
typically used within OpenStack deployments and provide guidance on common
configuration mistakes that can result in an insecure operating environment.

A list of `security notes <https://wiki.openstack.org/wiki/Security_Notes>`_
is available online, but are also published on the OpenStack mailing list as they
are released.

Security tool development
~~~~~~~~~~~~~~~~~~~~~~~~~

The security team are constantly looking at ways to introduce tooling and
automation to improve the overall security of OpenStack projects. Some of these
projects are outlined below.

Bandit - A security linter
^^^^^^^^^^^^^^^^^^^^^^^^^^

Bandit is a security linter for Python source code, utilizing the ast module
from the Python standard library. The **ast** module is used to convert source code
into a parsed tree of Python syntax nodes. Bandit allows users to define custom
tests that are performed against those nodes. At the completion of testing,
a report is generated that lists security issues identified within the
target source code.

Bandit is currently a stand-alone tool which can be downloaded by end-users and
run against arbitrary source code. Although early in development it is already
adding value to the OpenStack code base with several projects leveraging it
in their CI gate tests. As the project matures the desire is to see widespread
adoption of Bandit in the OpenStack community.

Bandit can be obtained by cloning the `repository <https://git.openstack.org/openstack/bandit.git>`_.
The README.rst file contains documentation regarding installation, usage,
and configuration.

* `Bandit Git Repository <https://git.openstack.org/cgit/openstack/bandit>`_
* `Bandit Gerrit <https://review.openstack.org/#/q/bandit,n,z>`_
* `Bandit Launchpad <https://bugs.launchpad.net/bandit>`_

Anchor - Ephemeral PKI
^^^^^^^^^^^^^^^^^^^^^^

Anchor is a lightweight, open source, Public Key Infrastructure (PKI), which
uses automated provisioning of short-term certificates to enable cryptographic
trust in OpenStack services. Certificates are typically valid for 12-24 hours
and are issued based on the result from a policy enforcing decision engine.
Short term certificates enable passive revocation, to bypass the issues with
the traditional revocation mechanisms used in most PKI deployments.

* `Anchor Git Repository <https://git.openstack.org/cgit/openstack/anchor>`_
* `Anchor Gerrit <https://review.openstack.org/#/q/anchor,n,z>`_
* `Anchor Launchpad <https://bugs.launchpad.net/anchor>`_


OpenStack Security Guide
~~~~~~~~~~~~~~~~~~~~~~~~

The OpenStack Security Guide provides best practices learned by cloud operators
while hardening their OpenStack deployments. This book was written by a close
community of security experts from the OpenStack Security Group in an intense
week-long effort at an undisclosed location. One of the goals for this book is
to bring together interested members to capture their collective knowledge
and give it to the OpenStack community.

Read `the guide <http://docs.openstack.org/sec/>`_ online today.


Secure development guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The OpenStack security team have collaboratively developed this set of
guidelines and best practices to help avoid common mistakes that lead
to security vulnerabilities within the OpenStack platform.

.. toctree::
   :maxdepth: 1
   :glob:

   ./guidelines/*
