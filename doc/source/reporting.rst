.. :Copyright: 2015, OpenStack Vulnerability Management Team
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode

============================================
 How to report security issues to OpenStack
============================================

If you think you've identified a vulnerability, please work with us to rectify
and disclose the issue together. We provide two ways to report issues to the
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
  :doc:`vmt`'s members. You're encouraged to encrypt messages to their OpenPGP
  keys.

.. note::

  All private reports of suspected vulnerabilities are embargoed for a maximum
  of 90 days. Unless unusual circumstances arise, any defect reported in
  private will be made public within 90 calendar days from when it is received,
  even if a solution has not been identified.
