.. :Copyright: 2017, OpenStack Vulnerability Management Team
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode

==================================
 Vulnerability Management Process
==================================

The OpenStack vulnerability management team (VMT_) is responsible
for coordinating the progressive disclosure of a vulnerability.

Members of the team are independent and security-minded folks who
ensure that vulnerabilities are dealt with in a timely manner and
that downstream stakeholders are notified in a coordinated and fair
manner. Where a member of the team is employed by a downstream
stakeholder, the member does not give their employer prior notice of
any vulnerabilities. In order to reduce the disclosure of
vulnerability in the early stages, membership of this team is
intentionally limited to a small number of people.

.. _VMT: https://launchpad.net/~openstack-vuln-mgmt

Supported versions
------------------

The Vulnerability Management team coordinates patches fixing
vulnerabilities in supported stable branches (corresponding to
previous major releases) of OpenStack, in addition to the master
branch (next version under development), for all `security supported
projects`_.

.. _security supported projects: http://governance.openstack.org/reference/tags/vulnerability_managed.html

Process
-------

Each security bug is assigned a VMT *coordinator* (member from the
vulnerability management team) that will drive the fixing and
disclosure process. Here are the steps we follow.

.. image:: vmt-process.png
   :width: 100 %
   :alt: VMT Process
   :target: _images/vmt-process.png

Reception
^^^^^^^^^

A report can be received either as a private encrypted email to one
of the VMT members, or as a Launchpad security bug (check the box
marked "this is a security issue").

The first steps performed by the VMT are to confirm the validity of
the report, create a Launchpad bug if necessary, prefix the
description with an `embargo reminder`_, add an ossa bugtask and
subscribe the project's core security review team for confirmation
of impact and determination of affected branches. Reports starting
with an *Incomplete* ossa bugtask should have a corresponding
`incomplete reception`_ message added in a comment. Once the VMT
confirms an OSSA is warranted, the ossa bugtask status will be set
to *Confirmed*. If the need for an OSSA is challenged, the ossa
bugtask status should be set back to *Incomplete* until that
question is resolved.

For some lower-risk issues or problems which may only be easy to
solve in future releases, the ossa bugtask will be set to *Opinion*
and the core security reviewers for the OpenStack Security team will
be subscribed to determine whether they wish to issue an OSSN (these
reports may still sometimes remain under embargo until the OSSN is
issued). If no OSSA is warranted and there is no benefit to an OSSN_
then the ossa bugtask will be set to *Won't Fix* or *Invalid*
(depending on the specific situation) and the bug state switched
from *Private Security* to *Public*, optionally adding the
*security* bug tag if the report concerns a potential security
hardening opportunity. The specifics are indexed in the `report
taxonomy`_ and `task status`_ tables.

.. _embargo reminder: #reception-embargo-reminder-private-issues
.. _incomplete reception: #reception-incomplete-message-unconfirmed-issues
.. _OSSN: https://wiki.openstack.org/wiki/Security_Notes
.. _report taxonomy: #incident-report-taxonomy
.. _task status: #ossa-task-status

Patch development
^^^^^^^^^^^^^^^^^

For a private report, the reporter (automatic if reported directly
as a bug) and the affected projects' core security review teams plus
anyone they deem necessary to develop and validate a fix are added
to the bug's subscription list. A fix is proposed as a patch to the
current master branch (as well as any affected supported branches)
and attached to the private bug report, **not sent to the public
code review system**.

For public reports, there is no need to directly subscribe anyone
and patches can be submitted directly to the code review system
instead of as bug attachments (though the bug should be referenced
in any commit messages so it will be updated automatically).

If project-side delays are encountered at this or any subsequent
stage of the process, the VMT and other interested parties may reach
out to that project's `Vulnerability Management Liaison`_ requesting
more immediate attention to the issue.

.. _Vulnerability Management Liaison: https://wiki.openstack.org/wiki/CrossProjectLiaisons#Vulnerability_management

Patch review
^^^^^^^^^^^^

For a private report once the initial patch has been attached to the
bug, core reviewers on the subscription list from the project in
question should review it and suggest updates or pre-approve it for
merging. Privately-developed patches need to be pre-approved so that
they can be fast-tracked through public code review later at
disclosure time.

For public reports, OpenStack's usual public code review and
approval processes apply.

Draft impact description
^^^^^^^^^^^^^^^^^^^^^^^^

In the mean time, the VMT coordinator prepares a vulnerability
description that will be communicated to downstream stakeholders,
and will serve as the basis for the Security Advisory that will be
finally published.

The description should properly credit the reporter, specify
affected versions (including unsupported ones) and accurately
describe impact and mitigation mechanisms. The VMT coordinator
should use the template below. Once the description is posted, the
ossa bugtask status should be switched to *Triaged*.

Review impact description
^^^^^^^^^^^^^^^^^^^^^^^^^

The description is validated by the reporter and the PTL.

Send CVE request
^^^^^^^^^^^^^^^^

To ensure full traceability, we get a CVE assigned before the issue
is communicated to a larger public. This is generally done as the
patch gets nearer to final approval. The ossa bugtask status is set
to *In progress* and the approved description is sent to a CNA in
an encrypted+signed email in order to get a CVE assigned. If the
issue is already public, the CVE request should be sent to the
oss-security list instead, including links to public bugs.

Get assigned CVE
^^^^^^^^^^^^^^^^

The CNA returns the assigned CVE. It is added to the Launchpad bug
(see "link to CVE" at the top-right), and the bug is retitled to
"$TITLE ($CVE)".

Embargoed disclosure
^^^^^^^^^^^^^^^^^^^^

Once the patches are approved and the CVE is assigned, a signed
email with the vulnerability description is sent to the downstream
stakeholders. The disclosure date is set to 3-5 business days,
excluding Monday/Friday and holiday periods, at 1500 UTC. No
stakeholder is supposed to deploy public patches before disclosure
date.

Once the email is sent, the ossa bugtask status should be set to
*Fix committed*. At that point we can also add downstream
stakeholders to the Launchpad bug, if they use Launchpad for
security patches. This means adding  ~canonical-security to the bug
subscribers.

For non-embargoed, public vulnerabilities no separate downstream
advance notification is sent. Instead the OSSA bugtask is set to fix
committed status once the CVE assignment is received OSSA is
drafting begins immediately.

Open bug, Push patch
^^^^^^^^^^^^^^^^^^^^

In preparation for this, make sure you have a core developer and a
stable maintainer available to help pushing the fix at disclosure
time.

On the disclosure hour, open bug, push patches to Gerrit for review
on master and supported stable branches, fast-track approvals
(referencing the bug).

Embargo reminder can be removed at that point.

Publish OSSA
^^^^^^^^^^^^

Shortly after pushing the patches (potentially waiting for the first
test runs to complete), publish the advisory to the OpenStack ML.
Wait until all patches merged to supported branches before setting
the ossa bugtask status to *Fix released*.

All patches merged
^^^^^^^^^^^^^^^^^^

Patches approved in code review do not necessarily merge
immediately, but should be tracked closely until they do (if the bug
number is correctly identified in commit messages then it will be
automatically updated to reflect this as well). Subsequent security
point releases of affected software may then be tagged if warranted.

Incident Report Taxonomy
------------------------

The VMT is now using this classification list in order to assist
vulnerability report triage, especially whenever a bug does not
warrant an advisory.

+----------+-----------+-------------------------------------------+
| Classes  | Outcome   | Description                               |
+==========+===========+===========================================+
| Class A  | OSSA      | A vulnerability to be fixed in master and |
|          |           | all supported releases                    |
+----------+-----------+-------------------------------------------+
| Class B1 | OSSN      | A vulnerability that can only be fixed in |
|          |           | master, security note for stable          |
|          |           | branches, e.g., default config value is   |
|          |           | insecure                                  |
+----------+-----------+-------------------------------------------+
| Class B2 | OSSN      | A vulnerability without a complete fix    |
|          |           | yet, security note for all versions,      |
|          |           | e.g., poor architecture / design          |
+----------+-----------+-------------------------------------------+
| Class B3 | OSSN      | A vulnerability in experimental or        |
|          |           | debugging features not intended for       |
|          |           | production use                            |
+----------+-----------+-------------------------------------------+
| Class C1 | Potential | Not considered a practical vulnerability  |
|          | OSSN      | (but some people might assign a CVE for   |
|          |           | it), e.g. one depending on UUID guessing  |
+----------+-----------+-------------------------------------------+
| Class C2 | Potential | A vulnerability, but not in OpenStack     |
|          | OSSN      | supported code, e.g., in a dependency     |
+----------+-----------+-------------------------------------------+
| Class D  | Potential | Not a vulnerability, just a bug with      |
|          | OSSN      | (some) security implications, e.g.,       |
|          |           | strengthening opportunities               |
+----------+-----------+-------------------------------------------+
| Class E  |           | Neither a vulnerability nor hardening     |
|          |           | opportunity                               |
+----------+-----------+-------------------------------------------+
| Class Y  |           | Vulnerability only found in development   |
|          |           | release                                   |
+----------+-----------+-------------------------------------------+
| Class Z  |           | When due process fails                    |
+----------+-----------+-------------------------------------------+

OSSA Task status
----------------

Here is a summary of the different OSSA task status meanings:

+---------------+--------------------------------------------------+
| Status        | Meaning                                          |
+===============+==================================================+
| Incomplete    | It is still unclear whenever the bug warrants an |
|               | advisory                                         |
+---------------+--------------------------------------------------+
| Confirmed     | The vulnerability is confirmed, impact           |
|               | description is in progress                       |
+---------------+--------------------------------------------------+
| Triaged       | Impact description has been submitted for review |
+---------------+--------------------------------------------------+
| In Progress   | CVE has been requested                           |
+---------------+--------------------------------------------------+
| Fix committed | Pre-OSSA has been communicated                   |
+---------------+--------------------------------------------------+
| Fix released  | All patches have been merged                     |
+---------------+--------------------------------------------------+
| Opinion       | Issue is likely a Class B/C/D, waiting for OSSN  |
+---------------+--------------------------------------------------+
| Won't Fix     | Doesn't fit with the project plans, sorry        |
+---------------+--------------------------------------------------+
| Invalid       | Class E and Z, not a bug or vulnerability. No    |
|               | further action to be taken                       |
+---------------+--------------------------------------------------+


Extent of Disclosure
--------------------

The science of vulnerability management is somewhere around being
able to assess impact and severity of a report, being able to design
security patches, being an obsessive process-following perfectionist
and respecting the rule of lesser disclosure.

Lesser disclosure is about disclosing the vulnerability details to
an increasing number of people over time, but only to the people
that are necessary to reach the next step. The diagram above shows
"disclosure extent" across the various steps of the process.

Vulnerability reporters retain final control over the disclosure of
their findings. If for some reason they are uncomfortable with our
process, their choice of disclosure terms prevails.

Embargo exceptions
^^^^^^^^^^^^^^^^^^

To keep the embargo period short and effective, the VMT may
choose to open bug reports. Issues that take too much time
to be fixed (e.g., more than 2 weeks) or issues that require
a complex patch are usually better solved in the open.

Whenever such a case occurs, the ossg-coresec group is
subscribed to the bug report in order to discuss whether or not
it's imperative to keep that particular bug private.

Downstream stakeholders
^^^^^^^^^^^^^^^^^^^^^^^

OpenStack as an upstream project is used in a number of
distributions, products, private and public service offerings that
are negatively affected by vulnerabilities. In the spirit of
responsible disclosure, this ecosystem, collectively known as the
downstream stakeholders, needs to be warned in advance to be able to
prepare patches and roll them out in a coordinated fashion on
disclosure day. The embargo period is kept voluntarily small (3-5
business days), as a middle ground between keeping the vulnerability
under cover for too long and not giving a chance to downstream
stakeholders to react.

If you're currently not a referenced stakeholder and think you
should definitely be included on that email distribution list,
please submit an email with a rationale to member(s) of the VMT_.

Templates
---------

Reception incomplete message (unconfirmed issues)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since this report concerns a possible security risk, an incomplete
security advisory task has been added while the core security
reviewers for the affected project or projects confirm the bug and
discuss the scope of any vulnerability along with potential
solutions.

Reception embargo reminder (private issues)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This issue is being treated as a potential security risk under
embargo. Please do not make any public mention of embargoed
(private) security vulnerabilities before their coordinated
publication by the OpenStack Vulnerability Management Team in the
form of an official OpenStack Security Advisory. This includes
discussion of the bug or associated fixes in public forums such as
mailing lists, code review systems and bug trackers. Please also
avoid private disclosure to other individuals not already approved
for access to this information, and provide this same reminder to
those who are made aware of the issue prior to publication. All
discussion should remain confined to this private bug report, and
any proposed fixes should be added to the bug as attachments.

Impact description ($DESCRIPTION)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    Title: $TITLE
    Reporter: $CREDIT
    Products: $PROJECT
    Affects: $AFFECTED_VERSIONS

    Description:
    $CREDIT reported a vulnerability in [project feature name].
    By doing [action] a [actor] may [impact] resulting in [consequence].
    Only [project deployment mode] are affected.

The AFFECTED_VERSIONS needs to stay valid after the fix is released.
For example, when kilo, liberty and mitaka are still security supported,
the AFFECTED_VERSIONS of keystone should read like this:

::

    Affects: >=2015.1.0 <=2015.1.4, >=8.0.0 <=8.1.0 and ==9.0.0

Once kilo reaches end of life, that line becomes:

::

    Affects: >=8.0.0 <=8.1.0 and ==9.0.0

If the oldest version affected is not easily identified, leave it
open-ended:

::

    Affects: <=8.1.0 and ==9.0.0

CVE request email (private issues)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* *To:* CNA
* *Subject:* CVE request for vulnerability in OpenStack $PROJECT

::

    A vulnerability was discovered in OpenStack (see below). In order to
    ensure full traceability, we need a CVE number assigned that we can
    attach to private and public notifications. Please treat the
    following information as confidential until further public
    disclosure.

    $DESCRIPTION

    Thanks in advance,

    --
    $VMT_COORDINATOR_NAME
    OpenStack Vulnerability Management Team

Email must be GPG-signed and GPG-encrypted.

CVE request email (public issues)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* *To:* oss-security@lists.openwall.com
* *Cc:* cve-assign@mitre.org
* *Subject:* CVE request for vulnerability in OpenStack $PROJECT

::

    A vulnerability was discovered in OpenStack (see below). In order to
    ensure full traceability, we need a CVE number assigned that we can
    attach to further notifications. This issue is already public,
    although an advisory was not sent yet.

    $DESCRIPTION

    References:
    https://launchpad.net/bugs/$BUG

    Thanks in advance,

    -- 
    $VMT_COORDINATOR_NAME
    OpenStack Vulnerability Management Team

Email must be GPG-signed but not encrypted.

Downstream stakeholders notification email (private issues)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We send two separate emails, to avoid off-topic replies to linux-distros:

* *To:* embargo-notice@lists.openstack.org
* *To:* linux-distros@vs.openwall.org

Subject and content for both emails is identical:

* *Subject:* [pre-OSSA] Vulnerability in OpenStack $PROJECT ($CVE)

::

    This is an advance warning of a vulnerability discovered in
    OpenStack, to give you, as downstream stakeholders, a chance to
    coordinate the release of fixes and reduce the vulnerability window.
    Please treat the following information as confidential until the
    proposed public disclosure date.

    $DESCRIPTION

    Proposed patch:
    See attached patches. Unless a flaw is discovered in them, these
    patches will be merged to their corresponding branches on the public
    disclosure date.

    CVE: $CVE

    Proposed public disclosure date/time:
    $DISCLOSURE, 1500UTC
    Please do not make the issue public (or release public patches)
    before this coordinated embargo date.

    Original private report:
    https://launchpad.net/bugs/$BUG
    For access to read and comment on this report, please reply to me
    with your Launchpad username and I will subscribe you.
    -- 
    $VMT_COORDINATOR_NAME
    OpenStack Vulnerability Management Team

Proposed patches are attached, email must be GPG-signed. Use
something unique and descriptive for the patch attachment file
names, for example ``cve-2013-4183-master-havana.patch`` or
``cve-2013-4183-stable-grizzly.patch``.

OpenStack security advisories (OSSA)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The document is first submitted as a yaml description to the ossa
project using this template::

    date: YYYY-MM-DD

    id: OSSA-$NUM

    title: '$TITLE'

    description: '$DESCRIPTION_CONTENT'

    affected-products:

      - product: $PROJECT
        version: $AFFECTED_VERSIONS

    vulnerabilities:

      - cve-id: $CVE

    reporters:

      - name: '$CREDIT'
        affiliation: $CREDIT_AFFILIATION
        reported:
          - $CVE

    issues:

      links:
        - https://launchpad.net/bugs/$BUG

    reviews:

      kilo:
        - https://review.openstack.org/$MASTER_REVIEW

      juno:
        - https://review.openstack.org/$STABLE_REVIEW

      type: gerrit

    notes:
      - 'Optional note such as cross project version requirements'

Once approved, use the 'Show Source' button from the gate-ossa-docs output
to get the generated RST document. We send two separate emails, to
avoid off-topic replies to oss-security list:

* *To:* openstack-announce@lists.openstack.org, openstack@lists.openstack.org
* *To:* oss-security@lists.openwall.com

Subject and content for both emails is identical:

* *Subject:* [OSSA-$NUM] $TITLE ($CVE)
* *Body:* The generated RST document

Notes:

* Email must be GPG-signed.
* $CVE must always be of the form CVE-YYYY-XXXX
* $NUM is of the form YYYY-XX
