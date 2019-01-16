.. :Copyright: 2015, OpenStack Foundation
.. :License: This work is licensed under a Creative Commons
             Attribution 3.0 Unported License.
             http://creativecommons.org/licenses/by/3.0/legalcode


Using Rootwrap in OpenStack
===========================

Most rootwrap filters are overly permissive, and allow running commands as root
with no additional filtering on the arguments given, and little sanitization is
done of the input commands.

Additionally, maintaining command filters is difficult. We have found that
unused filters are left in place after they should have been removed.

Finally, rootwrap cannot easily express precise semantics of the use cases of
privileged commands.

To Privilege or Not to Privilege, That is the Question
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before attempting to complete a privileged task with best practice, the task
should be analyzed to see if the task can be completed in an unprivileged
fashion. For example, using service accounts with file permissions and
ownership for access instead of running a command as root.

Additionally, files can be owned by the project group instead of the root
group. These cases are  preferred solutions where an architectural change is
preferred, and using privileged access can introduce security issues.

Do the Necessary
~~~~~~~~~~~~~~~~

Rootwrap currently has several deficiencies:

-  Auditing of rootwrap filters
-  Creation of new filter classes to reflect the semantics of the
   command
-  Existing CommandFilters replaced with RegExpFilters
-  Auditing the resulting complex regular expressions reliably

Instead, a better approach is multi-faceted:

-  Create an abstraction between the tasks being performed and the commands
   being run
-  Utilize available privilege separation mechanisms currently available
   in the Linux operating system
-  Move away from calling external commands where possible
-  Permit sanitization of input to privileged tasks
-  Increase ease of use around auditing privileged task implementations
-  Permit each project to have domain-specific tasks
-  Share common tasks with other projects
-  Place minimum burden on developers while still creating better
   privilege separation

These guidelines will allow better semantic filtering of arguments being passed
for each task. For example, if we need to mount an image or device in a
specific filesystem sub-tree the caller does not need to pass the full path of
the mount point. Additionally, each external command or library will have its
own interpretation of arguments, and we need to be able to sanitize those in
task-specific and use-specific ways.

Auditing the filtering and sanitization code is necessary as well, and this
needs to be easier to do so it can be done as needed. Sharing common tasks will
allow easier auditing as well as contribute to code centralization and re-use.

Looking Forward
~~~~~~~~~~~~~~~

Within the OpenStack project, understanding how to better limit the usage of
general commands is needed. For example, DeleteLink should not be able to
delete an arbitrary path. Discussions are converging around a privileged
daemon, similar to the one recently proposed for neutron. This would give
several advantages including better SELinux and AppArmor profiles as the
necessary privileges would be clearly stated in the code. Another area this
would help is in system calls, both direct and external. Unfortunately, this
would seemingly contradict the last bullet outlined above to build a better
approach. It is, however, necessary to secure the OpenStack project.

The alternative is to accept that projects (such as nova-compute) will need to
run as root, and as such will need to be fully audited - including rootwrap
filters. SELinux and AppArmor profiles will be the responsibility of the
deployer to create and maintain.

Next Steps
~~~~~~~~~~

All calls to rootwrap, or project-specific interfaces to rootwrap, should be
migrated to interfaces in a project specific privileged task module. This will
still call rootwrap but will allow for better sanitization, identification of
what can be consolidated into shared code, and will allow easier migration to a
future solution.

The current codebase should be audited to determine if there are any specific
places that can be re-architected to avoid running tasks as root. A Bandit
plugin that looked for the use of rootwrap would allow easy identification of
the code that needs to be audited.

Better documentation around how to write safe filters for rootwrap would allow
for developers to become better educated, but would also give reviewers a
citable document to link against in Gerrit.

The neutron privilege separation daemon should be supported to build experience
and understand best practices around such an implementation.

When a final solution is determined the implementation should be
audited regularly to ensure it is being used correctly and the results are as
expected.

References
~~~~~~~~~~

-  `Original rootwrap discussion from the OpenStack developer
   mailinglist <http://lists.openstack.org/pipermail/openstack-dev/2015-February/055971.html>`__
-  `Neutron privileged daemon
   proposal <https://review.openstack.org/#/c/155631>`__
-  `Bandit <https://wiki.openstack.org/wiki/Security/Projects#Bandit_Source_Code_Analyzer>`__
-  (insert AppArmor profile development resources here)
-  (insert SELinux context reference here)
