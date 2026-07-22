.. :Copyright: 2026, OpenStack Vulnerability Management Team
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
 Guide for Project Security Maintainers
=========================================

This guide is for OpenStack project maintainers (PTLs, core
reviewers, and security liaisons) who need to work with the
:ref:`Vulnerability Management Team` on security reports.
For the VMT's own internal process, see :doc:`vmt-process`.

Initial Setup
-------------

These steps are required for VMT oversight. See
:ref:`repositories overseen` for full requirements and the
`project tracker configuration guide`_ for Launchpad setup.

1. **Create a security review team.** Register a
   ``{project}-coresec`` group in Launchpad. This is the small
   circle of trusted reviewers (conventionally called the project's
   coresec group) who will see private security reports and review
   embargoed patches. They need not all be core reviewers. Keep
   this group small: only people who need to confirm, fix, and
   review the reports.

2. **Configure bug tracker sharing.** In your project's Launchpad
   sharing settings, grant the VMT the ``All private security``
   policy so that every private security report defaults to being
   visible only to the VMT. (Launchpad's ``Some private security``
   grant is used to share individual reports more widely, and
   ``All private`` covers non-security private bugs; see the
   `project tracker configuration guide`_ for specifics.) The VMT
   will add your security review team to individual reports after
   initial triage.

Recurring Maintenance
---------------------

Review these items at the start of each release cycle.

1. **Keep security review team membership current.** Remove
   inactive members. Add new reviewers who will be working on
   security-sensitive areas. Stale membership weakens the embargo.

2. **Designate a security liaison.** Identify one person as the
   VMT's escalation point. If not explicitly designated, the PTL
   is the implicit liaison. Designating a liaison is already
   mandatory for teams under Distributed Project Leadership (DPL).
   Record your liaison in your project's entry in `projects.yaml`_
   in the governance repository.

.. _project tracker configuration guide: https://docs.openstack.org/project-team-guide/project-trackers.html
.. _projects.yaml: https://opendev.org/openstack/governance/src/branch/master/reference/projects.yaml

When a Bug Is Reported
----------------------

The reporter has taken extra care to make a responsible disclosure
of an issue that may impact a large segment of the OpenStack user
base. Treat every report with the attention it deserves.

1. The VMT triages every private security report filed against
   OpenStack projects. The VMT will subscribe your security review
   team and post an initial triage comment.

2. **Reproduce and confirm.** Verify that the reported behavior
   exists. If you cannot reproduce it, say so on the bug with
   details of your test environment.

3. **Classify.** Work with the VMT to assign a class per the
   :ref:`incident report taxonomy`. The classification determines
   the outcome (OSSA, OSSN, or public fix).

4. **Identify affected versions.** Once a report is classified as
   something the VMT will publish, this becomes critical. Determine
   the commit that first introduced the defect, and which
   maintained stable branches contain that code. The VMT needs
   the earliest affected version (full history, not just currently
   supported branches) and the version ranges for the OSSA and
   CVE request.

   Keep in mind that defects are sometimes introduced by a
   backport, so the commit that first introduced the defect may
   not be on the oldest branch. Check each maintained branch
   rather than assuming the earliest branch is affected.

   Use ``git log`` and ``git blame`` to trace the introducing
   commit across branches. For example, if the vulnerable code
   was introduced in ``12.0.0`` and is present on ``stable/2025.1``
   (current version ``26.0.1``) and ``stable/2025.2`` (current
   version ``27.0.0``), the affected versions string would be:
   ``>=12.0.0 <26.0.2, >=27.0.0 <27.0.1``. See the
   :doc:`vmt-process` for full conventions on version ranges.

Evaluating Embargo
------------------

Not all Class A vulnerabilities need to be embargoed. The VMT
and the project maintainer jointly decide whether coordinated
disclosure is warranted. Consider:

* **Is the feature enabled by default?** Vulnerabilities in
  features that require explicit opt-in affect fewer deployments
  and may not justify the cost of an embargo.

* **How severe is the impact for cloud operators?** Issues that
  allow tenant escape, data exfiltration, or denial of service
  across tenants are strong candidates for embargo.

* **Is there a viable workaround?** If operators can mitigate by
  disabling a feature or adjusting configuration, the urgency of
  coordinated disclosure is reduced.

* **How complex is the fix?** Simple fixes that can be developed
  quickly may not need a long embargo window. Complex fixes that
  require extended development are often better handled in the
  open (see :ref:`incident report taxonomy` Class B cases).

If an embargo is not warranted, the bug can be made public and
patches submitted through normal code review. The VMT may still
coordinate the OSSA and CVE assignment if it is determined to be
a Class A vulnerability.

Developing the Fix
------------------

For embargoed vulnerabilities:

1. **All discussion stays on the private bug.** Do not mention the
   vulnerability in any public or untrusted forum: IRC channels,
   mailing lists, Gerrit, Slack, or downstream organization chat
   tools that may be auditable by others. The bug report is the
   only safe place to discuss details.

2. **Do not push patches to Gerrit.** Attach patches to the
   Launchpad bug as files. Coordinate with the VMT before making
   anything public.

3. **Prepare patches for all branches.** Create patches for master
   and every applicable maintained stable branch. Use
   ``git format-patch`` to generate them.

4. **Test locally.** CI cannot be used under embargo. Run unit
   tests, functional tests, and any relevant integration tests
   in your local environment. Document what you tested.

5. **Get a non-author review.** Have another security review team
   member review the patch directly on the bug. Pre-approval from a
   core reviewer makes disclosure day smoother.

Preparing for Disclosure
------------------------

1. The VMT requests a CVE identifier for Class A vulnerabilities
   and drafts an OSSA (OpenStack Security Advisory). You can
   review and refine the OSSA text on the bug.

2. **Agree on a disclosure date.** The VMT will propose dates
   (Tuesday, Wednesday, or Thursday at 1500 UTC). Pick a date
   when you and at least one other core reviewer will be
   available. Make sure that you or the other core reviewer have
   approval permission on the stable branches.

3. The VMT sends a downstream stakeholder notification with the
   patches attached. You can request a copy for your records.

4. After stakeholders are notified, you may loop in additional
   people who need to prepare (e.g., release liaisons), but they
   must respect the embargo until disclosure.

Disclosure Day
--------------

On the agreed date:

1. **Be available at 1400 UTC** (one hour before the OSSA is
   published).

2. **Push patches to Gerrit** with ``Closes-Bug: #NNNNNN`` in
   the commit message. Push to master and all maintained stable
   branches.

3. **Fast-track review and merge.** The patches have already been
   reviewed on the bug. Approve and merge promptly.

4. **Review the OSSA** that the VMT publishes for accuracy.
   Provide the Gerrit review URLs to the VMT for inclusion in
   the OSSA.

After Disclosure
----------------

1. Monitor that patches merge on all branches. If a patch fails
   CI, fix it promptly.

2. Request point releases from the release management team.
   Reference the OSSA number and CVE in your release request to
   flag it as a security release.
