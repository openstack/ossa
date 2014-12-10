#!/usr/bin/env python
import glob
import os
import sys
import textwrap
import traceback

from docutils import nodes
from docutils.parsers import rst
from docutils.statemachine import ViewList
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.addnodes import toctree
import yaml

reload(sys)
sys.setdefaultencoding("utf-8")


def to_snake_case(d):
    for k in d:
        v = d[k]
        del d[k]
        d[k.replace('-', '_')] = v
        if type(k) == dict:
            to_snake_case(d)


def to_paragraphs(d, *args):
    for k in args:
        if type(d[k]) == str:
            d[k] = '\n'.join(textwrap.wrap(d[k]))


def ossa_date_formatter(value):
    return "{:%B %d, %Y}".format(value)


def csv_list_formatter(value):
    return ", ".join(value)


def cve_list_formatter(value):
    return ', '.join([x['cve-id'] for x in value])


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
    to_paragraphs(vals, 'description')
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


def setup(app):
    app.info('Loading the vmt extension')
    app.connect('builder-inited', build_advisories)
