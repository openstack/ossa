..
  This work is licensed under a Creative Commons Attribution 3.0
  Unported License.
  http://creativecommons.org/licenses/by/3.0/legalcode

.. _repositories overseen:

=======================
 Repositories Overseen
=======================

While the Vulnerability Management Team (VMT) is available to assist
developers on request even if their projects are not explicitly
opted into this list, reports of suspected vulnerabilities for the
following OpenStack source repositories officially fall under direct
VMT oversight:

* `openstack/barbican <https://opendev.org/openstack/barbican>`_
* `openstack/castellan <https://opendev.org/openstack/castellan>`_
* `openstack/cinder <https://opendev.org/openstack/cinder>`_
* `openstack/glance <https://opendev.org/openstack/glance>`_
* `openstack/glance_store <https://opendev.org/openstack/glance_store>`_
* `openstack/heat <https://opendev.org/openstack/heat>`_
* `openstack/horizon <https://opendev.org/openstack/horizon>`_
* `openstack/ironic <https://opendev.org/openstack/ironic>`_
* `openstack/ironic-inspector <https://opendev.org/openstack/ironic-inspector>`_
* `openstack/ironic-lib <https://opendev.org/openstack/ironic-lib>`_
* `openstack/ironic-python-agent <https://opendev.org/openstack/ironic-python-agent>`_
* `openstack/keystone <https://opendev.org/openstack/keystone>`_
* `openstack/keystonemiddleware <https://opendev.org/openstack/keystonemiddleware>`_
* `openstack/networking-baremetal <https://opendev.org/openstack/networking-baremetal>`_
* `openstack/networking-generic-switch <https://opendev.org/openstack/networking-generic-switch>`_
* `openstack/neutron <https://opendev.org/openstack/neutron>`_
* `openstack/neutron-lib <https://opendev.org/openstack/neutron-lib>`_
* `openstack/nova <https://opendev.org/openstack/nova>`_
* `openstack/os-brick <https://opendev.org/openstack/os-brick>`_
* `openstack/oslo.config <https://opendev.org/openstack/oslo.config>`_
* `openstack/python-barbicanclient <https://opendev.org/openstack/python-barbicanclient>`_
* `openstack/python-cinderclient <https://opendev.org/openstack/python-cinderclient>`_
* `openstack/python-glanceclient <https://opendev.org/openstack/python-glanceclient>`_
* `openstack/python-heatclient <https://opendev.org/openstack/python-heatclient>`_
* `openstack/python-ironicclient <https://opendev.org/openstack/python-ironicclient>`_
* `openstack/python-ironic-inspector-client <https://opendev.org/openstack/python-ironic-inspector-client>`_
* `openstack/python-keystoneclient <https://opendev.org/openstack/python-keystoneclient>`_
* `openstack/python-neutronclient <https://opendev.org/openstack/python-neutronclient>`_
* `openstack/python-novaclient <https://opendev.org/openstack/python-novaclient>`_
* `openstack/python-swiftclient <https://opendev.org/openstack/python-swiftclient>`_
* `openstack/python-troveclient <https://opendev.org/openstack/python-troveclient>`_
* `openstack/sushy <https://opendev.org/openstack/sushy>`_
* `openstack/swift <https://opendev.org/openstack/swift>`_
* `openstack/trove <https://opendev.org/openstack/trove>`_

The `teams`_ responsible for maintenance of the source code within
these repositories have agreed to meet the expectations enumerated
below.

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

Updating
--------

Proposals to add or remove repositories in the oversight list will
be evaluated by the VMT following OpenStack's code review process.

Deprecation
-----------

A repository should only be removed from VMT oversight under extreme
circumstances, when the VMT is no longer able to adequately handle
its vulnerabilities. Care should be taken to only discontinue
vulnerability management for future non-patch releases, while
continuing to handle vulnerabilities on prior *maintained* branches
if at all possible until such time as they become *unmaintained* or
reach *end of life*. See the Project Team Guide section on `Stable
Branch Maintenance Phases`_ for detailed explanations of these terms.

.. _teams: https://governance.openstack.org/tc/reference/projects/
.. _security liaison: https://wiki.openstack.org/wiki/CrossProjectLiaisons#Vulnerability_management
.. _stable branch maintenance phases: https://docs.openstack.org/project-team-guide/stable-branches.html#maintenance-phases
