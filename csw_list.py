#!/usr/bin/env python
import sys
import cmd
from owslib.csw import CatalogueServiceWeb
from owslib.fes import PropertyIsEqualTo, PropertyIsLike

PAGE_BY = 50

class CSWCommand(cmd.Cmd):

    def setup(self, args):
        self.url = ''
        self.csw = None
        self.prompt = ' > '

        if len(args) == 2:
            self.url = args[-1]
            self.do_connect(self.url)


    def do_connect(self, line):
        """
            Connect to a remote CSW server.

            e.g.  connect http://server/csw
        """
        self.url = line
        self.csw = CatalogueServiceWeb(self.url)
        self.prompt = self.url + " > "

    def do_show(self, line):
        """
        Shows the data about a specific record when found by ID

        e.g. show 7be6f471-d348-4e3b-959a-6a1ab44b8dd2
        """
        if not self.csw:
            print "Not connected, use connect command first"
            return

        self.csw.getrecordbyid(id=line)
        record = self.csw.records[line]
        for k, v in record.__dict__.iteritems():
            if k[0] == '_':
                continue
            print "  {}\t{}".format(k ,v)

    def do_search(self, line):
        """
        Search records where a specific term/phrase appears in the title

        e.g. search quota
        """
        constraint = PropertyIsLike('dc:title', '%{}%'.format(line))
        self._list(line, constraint=constraint)

    def do_list(self, line, constraint=None):
        """
        Lists the name and identifier of each record at the CSW server
        by paging through the results. The title and identifier will be
        printed to stdout.
        """
        self._list(line)

    def _list(self, line, constraint=None):
        if not self.csw:
            print "Not connected, use connect command first"
            return

        if constraint:
            self.csw.getrecords2(maxrecords=PAGE_BY, constraints=[constraint])
        else:
            self.csw.getrecords2(maxrecords=PAGE_BY)

        count = 0
        start = PAGE_BY
        while self.csw.records:
            # count += len(self.csw.records)
            self.display_records()
            if constraint:
                self.csw.getrecords2(startposition=start, maxrecords=PAGE_BY, constraints=[constraint])
            else:
                self.csw.getrecords2(startposition=start, maxrecords=PAGE_BY)

            start += PAGE_BY


    def display_records(self):
        for rec in self.csw.records:
            record = self.csw.records[rec]
            print record.title, record.identifier

    def do_quit(self, line):
        """ Exits """
        sys.exit(0)



        # ['abstract', 'accessrights', 'alternative', 'bbox', 'bbox_wgs84', 'contributor', 'coverage', 'created', 'creator', 'date', 'format', 'identifier', 'identifiers', 'ispartof', 'issued', 'language', 'license', 'modified', 'publisher', 'rdf', 'references', 'relation', 'rights', 'rightsholder', 'source', 'spatial', 'subjects', 'temporal', 'title', 'type', 'uris', 'xml']

def info(url):


    print "Total: {}".format(count)

if __name__ == '__main__':
    c = CSWCommand()
    c.setup(sys.argv)
    c.cmdloop()


