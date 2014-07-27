import json
import jsonschema
import sys

# Based on https://wiki.openstack.org/wiki/Security_supported_projects
VMT_SECURITY_SUPPORTED = [
    "nova",
    "python-novaclient",
    "swift",
    "python-swiftclient",
    "glance",
    "python-glanceclient",
    "keystone",
    "python-keystoneclient",
    "horizon",
    "horizon_lib",
    "django_openstack_auth",
    "neutron",
    "python-neutronclient",
    "cinder",
    "python-cinderclient",
    "ceilometer",
    "python-ceilometerclient",
    "heat",
    "python-heatclient",
    "heat-cfntools",
    "trove",
    "python-troveclient",
    "sahara",
    "python-saharaclient",
    "oslo.config",
    "oslo.version"
]

# Based on https://access.redhat.com/security/updates/classification
VMT_IMPACT_DESCRIPTIONS = [ "critical", "important", "moderate", "low" ]

# (allow temporarily for CVE data missing this information)
VMT_IMPACT_DESCRIPTIONS.append("UNKNOWN")

# This is a jsonschema in attempt to ensure content added to the
# repository is in a sane & consistent format..
OSSA_SCHEMA_V1 = {
    "title" : "OpenStack Advisory",
    "type" : "object",
    "properties": {
        "schema_version"  : {
            "type" : "integer"
        },

        "vulnerabilities" : {

            "type" : "array",
            "items" : {
                "type" : "object",
                "properties" : {
                    "cve" : {
                        "type" : "string",
                        "pattern" : "^CVE-[0-9]+-[0-9]+$"
                    },

                    "cwe" : {
                        "type" : "string"
                    },

                    "cvss" : {
                        "type": "object",
                        "properties": {
                            "base_score" : {
                                "type" : "string"
                            },
                            "scoring_vector" : {
                                "type" : "string"
                            }
                        },
                        "required": ["base_score", "scoring_vector" ]
                    },

                    "impact" : {
                        "enum" : VMT_IMPACT_DESCRIPTIONS
                    },
                },
                "required" : [ "cve", "cwe", "cvss", "impact" ]
            },
            "minItems" : 1,
            "uniqueItems" : True
        },

        "advisory" : {
            "type" : "object",
            "properties" : {

                "id" : {
                    "type" : "string",
                    "pattern" : "^[0-9]+-[0-9]+$"
                },
                "date" :{
                    "type": "string",
                    "pattern" : "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]"
                },
                "url" : {
                    "type" : "string"
                },
                "title" : {
                    "type" : "string"
                },
                "description" : {
                    "type" : "string"
                }
            },
            "required" : ["id", "date", "url", "title", "description" ]
        },

        "reporters" : {
            "type" : "array",
            "items" : {
                "type" : "object",
                "properties" : {
                    "name" : {
                        "type" : "string",
                    },
                    "company" : {
                        "type" : "string"
                    }
                },
                "required" : ["name", "company"],
            },
            "minItems" : 1,
            "uniqueItems" : True
        },

        "affects" : {
            "type" : "array",
            "items" : {
                "type" : "object",
                "properties" : {
                    "product" : {
                        "enum" : VMT_SECURITY_SUPPORTED
                    },
                    "version"  : {
                        "type" : "string"  # TODO define format for this
                    }
                },
                "required" : ["product", "version" ]
            },
            "minItems" : 1,
            "uniqueItems" : True

        },

        "bugs" : {
            "type" : "array",
            "items" : {
                "type" : "string",
                "pattern" : "^[0-9]+$"
            },
            "minItems" : 1,
            "uniqueItems" : True
        },

        "reviews" : {
            "type" : "array",
            "items" : {
                "type" : "string",
                "pattern" : "^[0-9]+$"
            },
            "minItems": 1,
            "uniqueItems": True
        },

        "notes"  : {
            "type" : "string"
        }
    },

    "required" : [
        "schema_version",
        "vulnerabilities",
        "advisory",
        "reporters",
        "affects",
        "bugs",
        "reviews"
    ]
}

def get_schema(version):
    if version == 1:
        return OSSA_SCHEMA_V1
    else:
        raise ValueError("Schema version: '{}' is not supported.".format(version))


def validate(files):
    for filename in files:
        with open(filename) as data:
            ossa = json.loads(data.read())
            if 'schema_version' not in ossa:
                print("error: <{}>: schema_version missing".format(filename))
                continue

            try:
                jsonschema.validate(ossa, get_schema(int(ossa["schema_version"])))
                print("{} - ok".format(filename))

            except jsonschema.ValidationError as e:
                print("{} - fail".format(filename))
                print(e.message)


if __name__ == "__main__":
    validate(sys.argv[1:])

