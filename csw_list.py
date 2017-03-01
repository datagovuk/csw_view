#!/usr/bin/env python
import sys
from owslib.csw import CatalogueServiceWeb

PAGE_BY = 50

def display_records(csw):
    for rec in csw.records:
        record = csw.records[rec]
        print record.title, record.identifier

        # ['abstract', 'accessrights', 'alternative', 'bbox', 'bbox_wgs84', 'contributor', 'coverage', 'created', 'creator', 'date', 'format', 'identifier', 'identifiers', 'ispartof', 'issued', 'language', 'license', 'modified', 'publisher', 'rdf', 'references', 'relation', 'rights', 'rightsholder', 'source', 'spatial', 'subjects', 'temporal', 'title', 'type', 'uris', 'xml']

def info(url):
    csw = CatalogueServiceWeb(url)
    csw.getrecords2(maxrecords=PAGE_BY)

    start = PAGE_BY
    while csw.records:
        display_records(csw)
        records = csw.getrecords2(startposition=start, maxrecords=PAGE_BY)
        start += PAGE_BY


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Please specify the URL"
        sys.exit(1)

    url = sys.argv[-1]
    info(url)

