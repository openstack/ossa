..
  This work is licensed under a Creative Commons Attribution 3.0
  Unported License.
  http://creativecommons.org/licenses/by/3.0/legalcode

.. _repositories overseen:

=======================
 Repositories Overseen
=======================

Reports of suspected vulnerabilities for all OpenStack source
repositories officially fall under direct VMT oversight as long as
they meet the expectations enumerated below.

Requirements
------------

1. Embargoes for privately-submitted reports of suspected
   vulnerabilities shall not last more than 90 days, except under
   unusual circumstances. Following the embargo expiration, reports
   will be made publicly visible regardless of whether any advisory
   has been issued or patch provided.

2. The VMT will not track or issue advisories for external software
   components. Only source code provided by official OpenStack
   project teams is eligible for oversight by the VMT. For example,
   base operating system components included in a server/container
   image or libraries vendored into compiled binary artifacts are
   not within the VMT's scope.

3. Repositories must have versioned releases to qualify for VMT
   oversight. Vulnerabilities warrant advisories if they appear in
   official releases or on *maintained* stable branches (see `Stable
   Branch Maintenance Phases`_). Vulnerabilities only present in
   master since the last release, or only on *unmaintained*
   branches, will not have their disclosure coordinated by the VMT.
   Pre-releases, release candidates and milestones are not
   considered official releases for the purpose of this policy.

4. The defect tracker for each overseen repository must be
   configured to initially only provide access for the VMT for
   privately-submitted reports. It is the responsibility of the VMT
   to determine whether suspected vulnerabilities are reported
   against the correct repository and redirect them when possible,
   since reporters are often unfamiliar with our project structure
   and may choose incorrectly. It implies some loss of control for
   the project team over initial triage of bugs reported privately
   as suspected vulnerabilities, but helps minimize the number of
   people who have unnecessary knowledge of them prior to public
   disclosure and so reduces the risk of prematurely ending an
   embargo.

5. The team must have a dedicated point of contact for security
   issues, so that the VMT can engage them to triage reports of
   potential vulnerabilities. Teams with more than five core
   reviewers should (so as to limit the unnecessary exposure of
   private reports) settle on a subset of these to act as security
   core reviewers whose responsibility it is to be able to confirm
   whether a bug report is accurate/applicable or at least know
   other subject matter experts they can in turn subscribe to
   perform those activities in a timely manner. They should also be
   able to review and provide pre-approval of patches attached to
   private bugs, which is why at least a majority are expected to be
   core reviewers for their repositories. These should be members of
   a group contact in the team's defect tracker so that the VMT can
   easily subscribe them to new reports.

6. The team must identify a `security liaison`_, serving as a point
   of escalation for the VMT in situations where severe or lingering
   vulnerability reports are failing to gain traction toward timely
   and thorough resolution. If one is not explicitly delegated, the
   PTL is that team's implicit liaison.

7. Repositories should have automated testing for important
   features. Tests need to be feasible for the VMT and security
   reviewers to run locally while evaluating patches under embargo,
   and must also run within the context of OpenStack's official
   continuous integration infrastructure. This helps reduce the risk
   of approved security fixes creating new bugs when rushed through
   public code review at the time of disclosure, and also decreases
   the chance of creating additional work for the VMT issuing errata
   later.

8. Projects are encouraged to undertake a review, audit, or threat
   analysis of their software in order to proactively identify
   likely security weaknesses. In the event the project team
   performs it, the results should ideally also be validated by a
   third party (which could just be other members of the community
   not involved directly in that project). Refreshing the analysis
   immediately following each major release is suggested, but an
   outdated analysis is still more useful than none at all. This is
   a recommendation in order to keep the VMT's workload to a
   necessary minimum, but is not a strict requirement.

.. _security liaison: https://wiki.openstack.org/wiki/CrossProjectLiaisons#Vulnerability_management
.. _stable branch maintenance phases: https://docs.openstack.org/project-team-guide/stable-branches.html#maintenance-phases
