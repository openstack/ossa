#!/bin/env python3
# Copyright 2018 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Import launchpad bugs to a csv file

Install using:
  python3 -m venv --system-site-packages .venv
  . .venv/bin/activate
  pip3 install launchpadlib keyrings.alt

Run:
  ./getbugs.py > bugs.csv

Publish to ethercalc:
  curl --include --request PUT --header "Content-Type: text/csv" \
       --data-binary @./bugs.csv https://ethercalc.openstack.org/_/CALC_ID
"""

from launchpadlib.launchpad import Launchpad
from datetime import datetime, timezone


STATUS = [
    "New",
    "Incomplete",
    "Triaged",
    "Opinion",
    # "Invalid", "Won't Fix", "Fix Released"
    "Confirmed",
    "In Progress",
    "Fix Committed",
]
COLUMNS = [
    ("Number", lambda x: "<https://launchpad.net/bugs/{nr}>".format(
        nr=x.lp_get_parameter('self_link').split('/')[-1])),
    ("Created", lambda x: datetime.strftime(x.lp_get_parameter('date_created'),
                                            "%Y-%m-%dT%H:%M:%S")),
    ("Age", lambda x: (datetime.now(timezone.utc) -
                       x.lp_get_parameter('date_created')).days),
    ("Status", lambda x: x.lp_get_parameter('status')),
    ("Importance", lambda x: x.lp_get_parameter("importance")),
    ("Completed", lambda x: str(x.lp_get_parameter("is_complete"))),
]

print(",".join([col[0] for col in COLUMNS]), end='\r\n')
for bug in Launchpad.login_with('VMT GetBugs', 'production')\
                    .projects["ossa"]\
                    .searchTasks(status=STATUS):
    print(",".join(["\"%s\"" % col[1](bug) for col in COLUMNS]), end='\r\n')
