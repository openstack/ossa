#!/usr/bin/env python
import yaml
from rstcloth import rstcloth
from datetime import datetime
from pprint import pprint
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

TW=3

def format_affected(affected):
    content = "\n   " # wtf?
    seen = False
    for product in affected:
        if seen:
            content += " "*TW
        content +="- {product}: {version}\n".format(**product)
        seen = True
    content += "\n"
    return content

def format_reporters(reporters):
    content = ""
    seen = False
    for reporter in reporters:
        if seen:
            content += " "*TW
        if not 'affiliation' in reporter:
            content += "- {name}\n".format(**reporter)
        else:
            content += "- {name} from {affiliation}\n".format(**reporter)
        seen = True

    content += "\n"
    return content

def format_urls(links):
    content =""
    seen = False
    for link in links:
        if seen:
            content += " "*TW
        content += "- `{url} <{url}>`_\n".format(url=link)
        seen = True
    content += "\n"
    return content

def main(args):
    for arg in args:
        data = yaml.safe_load(open(arg).read())
        doc = rstcloth.RstCloth()
        doc.title("{id}".format(**data))
        doc.newline()
        doc.h2(data['title'])

        doc.field('Date', "{:%B %d, %Y}".format(data['date']))
        doc.newline()

        doc.field('Description', data['description'])
        doc.newline()

        doc.field('Announcement', doc.inline_link(data['reference'],data['reference']), wrap=False)
        doc.newline()

        doc.field("Products affected", format_affected(data['affected-products']), wrap=False)
        doc.newline()

        doc.field("Credits", format_reporters(data['reporters']), wrap=False)
        doc.newline()

        doc.field("Bug reports", format_urls(data['issues']['links']), wrap=False)
        doc.newline()

        doc.field("Reviews", format_urls(data['reviews']['links']), wrap=False)
        doc.newline()

        #doc.directive('download', '`<{id}.yaml>`'.format(**data))
        doc.print_content()

if __name__ == '__main__':
    main(sys.argv[1:])

