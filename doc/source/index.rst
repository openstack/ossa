.. :Copyright: 2015, OpenStack Vulnerability Management Team
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode

====================
 OpenStack Security
====================

.. toctree::
   :hidden:

   repos-overseen
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

* Check the project's documentation to determine where it receives bug reports.
  If on https://storyboard.openstack.org/ then log in and create a new story,
  making sure to check both the **Private** and **Vulnerability or
  Security-related** checkboxes, and selecting the relevant project for the
  initial task before saving. If on https://bugs.launchpad.net/ then find the
  project there, log in click the 'Report a bug' link at the right, fill in the
  'Summary' and 'Further information' fields describing the issue, then click
  the 'This bug is a security vulnerability' checkbox near the bottom of the
  page before submitting it. This will make the bug Private and only accessible
  to the Vulnerability Management Team.

* If the issue is extremely sensitive or you're otherwise unable to use the
  bug tracker directly, please send an E-mail message to one or more of the
  `Vulnerability Management Team`_'s members. You're encouraged to encrypt
  messages to their OpenPGP keys.

.. note::

  All private reports of suspected vulnerabilities are embargoed for a maximum
  of 90 days. Unless unusual circumstances arise, any defect reported in
  private will be made public within 90 calendar days from when it is received,
  even if a solution has not been identified.


.. _openstack security project:
.. _vulnerability management:
.. _vulnerability management team:

Vulnerability Management Team
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

To directly reach members of the VMT, contact them at the following addresses
(optionally encrypted for the indicated OpenPGP keys):

.. Static key files are generated with the following command:
   ( gpg2 --fingerprint 0x97ae496fc02dec9fc353b2e748f9961143495829
   gpg2 --armor --export-options export-clean,export-minimal \
   --export 0x97ae496fc02dec9fc353b2e748f9961143495829 ) > \
   doc/source/_static/0x97ae496fc02dec9fc353b2e748f9961143495829.txt

* Jeremy Stanley <fungi@yuggoth.org>:
  `key 0x97ae496fc02dec9fc353b2e748f9961143495829
  <_static/0x97ae496fc02dec9fc353b2e748f9961143495829.txt>`_
* Gage Hugo <gage.hugo@gmail.com>:
  `key 0x59ad76e5c2c722ebfa7a4a1fe7a8fd2b76febd11
  <_static/0x59ad76e5c2c722ebfa7a4a1fe7a8fd2b76febd11.txt>`_
* Matthew Thode <mthode@mthode.org>:
  `key 0x14b91caaf68c4849f90ca41333ed3fd25afc78ba
  <_static/0x14b91caaf68c4849f90ca41333ed3fd25afc78ba.txt>`_

See :doc:`vmt-process` for details on our open process.

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
    the StoryBoard or Launchpad report comments.

After a patch for the reported bug has been developed locally, you the patch author need to share that with the community. This is a simple process, but it is different than the normal OpenStack workflow.

* Export it using the `format-patch` command::

    git format-patch --stdout HEAD~1 >path/to/local/file.patch

  Now you have the patch saved locally and you can attach it in a comment
  on the bug page.

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

