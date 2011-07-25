#!/usr/bin/env python
from xml.dom.minidom import parse
import re
import optparse
def main():
    opts = optparse.OptionParser()
    opts.add_option('--filename', '-f')
    options, arguments = opts.parse_args()
    patt = re.compile(r'<.*?>')
    if options.filename is not None: 
        parseFile(options.filename, patt)

def parseFile(xmlFile, patt):
    """Converts an XML sitemap to a list of URLs"""
    if xmlFile is not None:
        dom = parse(xmlFile)
        for node in dom.getElementsByTagName("loc"):
            print patt.sub('', node.toxml())

if __name__ == '__main__':
    main()
