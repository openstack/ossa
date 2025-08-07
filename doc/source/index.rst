.. :Copyright: 2015, OpenStack Vulnerability Management Team
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode

====================
 OpenStack Security
====================

.. toctree::
   :hidden:

   reporting
   repos-overseen
   vmt
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

For detailed vulnerability reporting instructions, see :doc:`reporting`.


.. _openstack security project:
.. _vulnerability management:
.. _vulnerability management team:

Vulnerability Management Team
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :doc:`vmt` for the list of OpenStack Vulnerability Managers.

Security information for OpenStack deployers
--------------------------------------------

There are four main sources of security guidance for OpenStack deployers:

* OpenStack Security Advisories (OSSA)
* OpenStack Security Notes (OSSN)
* OpenStack Security Guide


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


Release Artifact Signatures
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Deliverable artifacts for OpenStack releases, primarily Git tags and Python
package files (``.tar.gz`` sdists and ``.whl`` wheels), are signed by our
release automation. You can find more details in `the Cryptographic Signatures
section of the OpenStack Releases site
<https://releases.openstack.org/#cryptographic-signatures>`_.


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

