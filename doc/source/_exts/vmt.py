#!/usr/bin/env python
import glob
import os
import textwrap

from jinja2 import FileSystemLoader
from jinja2.environment import Environment
import yaml

from sphinx.util import logging

LOG = logging.getLogger(__name__)


def to_snake_case(d):
    for k in dict(d):
        v = d[k]
        del d[k]
        d[k.replace('-', '_')] = v
        if type(k) == dict:
            to_snake_case(d)


def ossa_date_formatter(value):
    return "{:%B %d, %Y}".format(value)


def csv_list_formatter(value):
    return ", ".join(value)


def cve_formater(value):
    if 'note' in value:
        return "%s (%s)" % (value['cve-id'], value['note'])
    return value['cve-id']


def cve_list_formatter(value):
    return ',\n      '.join([cve_formater(x) for x in value])


def render_template(template, data, **kwargs):
    template_dir = kwargs.get('template_dir', os.getcwd())
    loader = FileSystemLoader(template_dir)
    env = Environment(trim_blocks=True, loader=loader)
    env.filters["ossa_date"] = ossa_date_formatter
    env.filters["csv_list"] = csv_list_formatter
    env.filters["cve_list"] = cve_list_formatter
    template = env.get_template(template)
    return template.render(**data)


def render(source, template, **kwargs):
    vals = yaml.safe_load(open(source).read())
    to_snake_case(vals)
    return render_template(template, vals, **kwargs)


def build_advisories(app):

    template_name = "rst.jinja"
    template_files = os.path.join(".", "doc", "source", "_exts")
    yaml_files = os.path.join(".", "ossa")
    input_files = glob.glob(os.path.join(yaml_files, "*.yaml"))
    output_files = [x.replace(".yaml", ".rst") for x in input_files]
    for old, new in zip(input_files, output_files):
        with open(new, "w") as out:
            out.write(render(old, template_name, template_dir=template_files))


def reverse_toctree(app, doctree, docname):
    """Reverse the order of entries in the root toctree if 'glob' is used."""
    if docname in ["index", "ossalist"]:
        for node in doctree.traverse():
            if node.tagname == "toctree" and node.get("glob"):
                node["entries"].reverse()
                if docname == "index":
                    node["entries"] = node["entries"][0:5]
                break


def setup(app):
    LOG.info('Loading the vmt extension')
    app.connect('builder-inited', build_advisories)
    app.connect("doctree-resolved", reverse_toctree)
