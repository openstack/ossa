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

OpenStack has two mechanisms for communicating security information with
downstream stakeholders, "Advisories" and "Notes". OpenStack Security
Advisories (OSSA) are created to deal with severe security issues in OpenStack
for which a fix is available - OSSA's are issued by the OpenStack Vulnerability
Management Team (VMT). OpenStack Security Notes (OSSN) are used for security
issues which do not qualify for an advisory, typically design issues,
deployment and configuration vulnerabilities.


How to report security issues to OpenStack
------------------------------------------

If you think you've identified a vulnerability, please work with us to rectify
and disclose the issue responsibly. We provide two ways to report issues to the
OpenStack Vulnerability Management Team depending on how sensitive the issue
is:

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
  * Grant Murphy (grant.murphy@hpe.com): `GPG key for Grant`_
  * Morgan Fainberg (morgan.fainberg@gmail.com): `GPG key for Morgan`_

.. _`GPG key for Jeremy`: http://keyserver.ubuntu.com:11371/pks/lookup?search=0x48f9961143495829

.. _`GPG key for Tristan`: http://keyserver.ubuntu.com:11371/pks/lookup?search=0x925CC5D8

.. _`GPG key for Grant`: http://keyserver.ubuntu.com:11371/pks/lookup?search=0x551a2252

.. _`GPG key for Morgan`: http://keyserver.ubuntu.com:11371/pks/lookup?search=0x0D1A8C8423CF3C86BF420F7BB9A83CEFA07C6D8A


Security information for OpenStack deployers
--------------------------------------------

There are four main sources of security guidance for OpenStack deployers:

* OpenStack Security Advisories (OSSA)
* OpenStack Security Notes (OSSN)
* OpenStack Security Guide
* OpenStack Security Project blog


OpenStack Security Advisories (OSSA)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recent OSSAs:

.. toctree::
   :maxdepth: 1
   :glob:

   ./ossa/*

You can find the complete list of published advisories here:

.. toctree::
   :maxdepth: 1
   :glob:

   ossalist


OpenStack Security Notes
~~~~~~~~~~~~~~~~~~~~~~~~

Security Notes advise users of security related issues. Security notes are
similar to advisories; they often address vulnerabilities in third party tools
typically used within OpenStack deployments and provide guidance on common
configuration mistakes that can result in an insecure operating environment.

The complete set of `security notes <https://wiki.openstack.org/wiki/Security_Notes>`_
is available online, but they are also published on the OpenStack mailing list
when they are released.


OpenStack Security Guide
~~~~~~~~~~~~~~~~~~~~~~~~

The OpenStack Security Guide provides best practice information for OpenStack
deployers. This guide was written by a community of security experts from the
OpenStack Security Project, based on experience gained while hardening
OpenStack deployments. The guide covers topics including compute and storage
hardening, rate limiting, compliance, and cryptography; it is the starting
point for anyone looking to securely deploy OpenStack.

Read `the guide <http://docs.openstack.org/sec/>`_ online today.


OpenStack Security Project blog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Security Project also maintain a blog, with posts about current and future
projects, presentations and other information that doesnt fit in anywhere else:
`<http://openstack-security.github.io/>`_




Security information for OpenStack developers
---------------------------------------------


How to propose and review a security patch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


Secure development guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The OpenStack security team have collaboratively developed this set of
guidelines and best practices to help avoid common mistakes that lead to
security vulnerabilities within the OpenStack platform.

.. toctree::
  :maxdepth: 1
  :glob:

  ./guidelines/*


OpenStack Security Project
--------------------------

The OpenStack Security Project runs an number of initiatives aimed at improving
the overall security of OpenStack projects and ensuring that security incidents
are handled in a coordinated fashion.  Key initiatives that fall within the
security project's areas of responsibility are outlined below.


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


Security tool development
~~~~~~~~~~~~~~~~~~~~~~~~~

The Security project are constantly looking at ways to introduce tooling and
automation to improve the overall security of OpenStack projects. Some of these
projects are outlined below.

Bandit - static analysis for Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bandit is a security static analysis tool for Python source code, utilizing the
ast module from the Python standard library. The **ast** module is used to
convert source code into a parsed tree of Python syntax nodes. Bandit allows
users to define custom tests that are performed against those nodes. At the
completion of testing, a report is generated that lists security issues
identified within the target source code.

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

Anchor - ephemeral PKI
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
