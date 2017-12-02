from comp62521.statistics import average
import itertools
import numpy as np
from xml.sax import handler, make_parser, SAXException
from operator import itemgetter
import collections
from heapq import *
PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]

class Publication:
    CONFERENCE_PAPER = 0
    JOURNAL = 1
    BOOK = 2
    BOOK_CHAPTER = 3

    def __init__(self, pub_type, title, year, authors):
        self.pub_type = pub_type
        self.title = title
        if year:
            self.year = int(year)
        else:
            self.year = -1
        self.authors = authors

class Author:
    def __init__(self, name):
        self.name = name

class Stat:
    STR = ["Mean", "Median", "Mode"]
    FUNC = [average.mean, average.median, average.mode]
    MEAN = 0
    MEDIAN = 1
    MODE = 2

class Database:
    def read(self, filename):
        self.publications = []
        self.authors = []
        self.author_idx = {}
        self.min_year = None
        self.max_year = None

        handler = DocumentHandler(self)
        parser = make_parser()
        parser.setContentHandler(handler)
        infile = open(filename, "r")
        valid = True
        try:
            parser.parse(infile)
        except SAXException as e:
            valid = False
            print "Error reading file (" + e.getMessage() + ")"
        infile.close()

        for p in self.publications:
            if self.min_year == None or p.year < self.min_year:
                self.min_year = p.year
            if self.max_year == None or p.year > self.max_year:
                self.max_year = p.year

        return valid

    def get_all_authors(self):
        return self.author_idx.keys()

    def calculate_first_last_sole(self):
        header = ("Author", "First Author",
                  "Last Author", "Sole Author")

        astats = [[0, 0, 0] for _ in range(len(self.authors))]
        for p in self.publications:
                if len(p.authors)!= 1:
                   for a in p.authors:
                       if p.authors[0] == a:
                           astats [a][0] += 1
                       if p.authors[len(p.authors)-1] == a:
                            astats [a][1] += 1
                if len(p.authors) == 1:
                    for a in p.authors:
                        if p.authors[0] == a:
                            astats [a][2] += 1
        data = [[self.authors[i].name] + astats[i]
            for i in range(len(astats))]
        return (header, data)
        #pass the third test

    def StatsForAuthor(self,author):
        publications = 0
        conference_papers = 0
        journals = 0
        books = 0
        book_chapters = 0
        coauthors = 0
        flag = True
        lista = []
        first = 0
        Fconference_papers = 0
        Fjournals = 0
        Fbooks = 0
        Fbook_chapters = 0
        last = 0
        Lconference_papers = 0
        Ljournals = 0
        Lbooks = 0
        Lbook_chapters = 0
        sole = 0
        Sconference_papers = 0
        Sjournals = 0
        Sbooks = 0
        Sbook_chapters = 0

        for p in self.publications:
            for a in p.authors:
                if str(self.authors[a].name)==author:
                    publications += 1
                    if p.pub_type==0:
                        conference_papers += 1
                    if p.pub_type==1:
                        journals += 1
                    if p.pub_type==2:
                        books += 1
                    if p.pub_type==3:
                        book_chapters += 1
                    for i in p.authors:
                        if str(self.authors[i].name) != author and str(self.authors[i].name) not in lista:
                            lista.append(str(self.authors[i].name))
                            coauthors += 1
            if len(p.authors) != 1 and self.authors[p.authors[0]].name == author:
                first += 1
                if p.pub_type==0:
                    Fconference_papers += 1
                if p.pub_type==1:
                    Fjournals += 1
                if p.pub_type==2:
                    Fbooks += 1
                if p.pub_type==3:
                    Fbook_chapters += 1

            if len(p.authors) != 1 and self.authors[p.authors[-1]].name == author:
                last += 1
                if p.pub_type == 0:
                    Lconference_papers += 1
                if p.pub_type == 1:
                    Ljournals += 1
                if p.pub_type == 2:
                    Lbooks += 1
                if p.pub_type == 3:
                    Lbook_chapters += 1

            if len(p.authors) == 1 and self.authors[p.authors[0]].name == author:
                sole += 1
                if p.pub_type == 0:
                    Sconference_papers += 1
                if p.pub_type == 1:
                    Sjournals += 1
                if p.pub_type == 2:
                    Sbooks += 1
                if p.pub_type == 3:
                    Sbook_chapters += 1
        return (publications,conference_papers,journals,book_chapters,books,coauthors,first,Fconference_papers,Fjournals,Fbook_chapters,
                Fbooks,last,Lconference_papers,Ljournals,Lbook_chapters,Lbooks,sole,Sconference_papers,Sjournals,Sbook_chapters,Sbooks)
#pass the third test
    def calculate_authors_details(self):
        header=("Author", "First Author",
                  "Last Author", "Sole Author")
        subheader=('Journals', 'Conference Papers','Books', 'Book Chapters')
        data=[]
        for i in self.authors:
            author=[str(i.name),0,0,0,0,0,0,0,0,0,0,0,0]
            for p in self.publications:
                if p.pub_type==1:
                    if len(p.authors)!= 1:
                        if i.name==self.authors[p.authors[0]].name:
                            author[1]+=1
                        if i.name==self.authors[p.authors[len(p.authors)-1]].name:
                            author[2]+=1
                    else:
                        if i.name==self.authors[p.authors[0]].name:
                            author[3]+=1
                if p.pub_type==0:
                    if len(p.authors)!= 1:
                        if i.name==self.authors[p.authors[0]].name:
                            author[4]+=1
                        if i.name==self.authors[p.authors[len(p.authors)-1]].name:
                            author[5]+=1
                    else:
                        if i.name==self.authors[p.authors[0]].name:
                            author[6]+=1
                if p.pub_type==2:
                    if len(p.authors)!= 1:
                        if i.name==self.authors[p.authors[0]].name:
                            author[7]+=1
                        if i.name==self.authors[p.authors[len(p.authors)-1]].name:
                            author[8]+=1
                    else:
                        if i.name==self.authors[p.authors[0]].name:
                            author[9]+=1
                if p.pub_type==3:
                    if len(p.authors)!= 1:
                        if i.name==self.authors[p.authors[0]].name:
                            author[10]+=1
                        if i.name==self.authors[p.authors[len(p.authors)-1]].name:
                            author[11]+=1
                    else:
                        if i.name==self.authors[p.authors[0]].name:
                            author[12]+=1
            data.append(author)
        return (header,subheader,data)



    def get_coauthor_data(self, start_year, end_year, pub_type):
        coauthors = {}
        for p in self.publications:
            if ((start_year == None or p.year >= start_year) and
                (end_year == None or p.year <= end_year) and
                (pub_type == 4 or pub_type == p.pub_type)):
                for a in p.authors:
                    for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = set([a2])
        def display(db, coauthors, author_id):
            return "%s (%d)" % (db.authors[author_id].name, len(coauthors[author_id]))

        header = ("Author", "Co-Authors")
        data = []
        for a in coauthors:
            data.append([ display(self, coauthors, a),
                ", ".join([
                    display(self, coauthors, ca) for ca in coauthors[a] ]) ])

        return (header, data)

    def get_average_authors_per_publication(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ func(auth_per_pub[i]) for i in np.arange(4) ] + [ func(list(itertools.chain(*auth_per_pub))) ]
        return (header, data)

    def get_average_publications_per_author(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))

        for p in self.publications:
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(pub_per_auth[:, i]) for i in np.arange(4) ] + [ func(pub_per_auth.sum(axis=1)) ]
        return (header, data)

    def get_average_publications_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        ystats = np.zeros((int(self.max_year) - int(self.min_year) + 1, 4))

        for p in self.publications:
            ystats[p.year - self.min_year][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(4) ] + [ func(ystats.sum(axis=1)) ]
        return (header, data)

    def get_average_authors_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        yauth = [ [set(), set(), set(), set(), set()] for _ in range(int(self.min_year), int(self.max_year) + 1) ]

        for p in self.publications:
            for a in p.authors:
                yauth[p.year - self.min_year][p.pub_type].add(a)
                yauth[p.year - self.min_year][4].add(a)

        ystats = np.array([ [ len(S) for S in y ] for y in yauth ])

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(5) ]
        return (header, data)

    def get_publication_summary_average(self, av):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))
        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        name = Stat.STR[av]
        func = Stat.FUNC[av]

        data = [
            [name + " authors per publication"]
                + [ func(auth_per_pub[i]) for i in np.arange(4) ]
                + [ func(list(itertools.chain(*auth_per_pub))) ],
            [name + " publications per author"]
                + [ func(pub_per_auth[:, i]) for i in np.arange(4) ]
                + [ func(pub_per_auth.sum(axis=1)) ] ]
        return (header, data)

    def get_publication_summary(self):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "Total")

        plist = [0, 0, 0, 0]
        alist = [set(), set(), set(), set()]

        for p in self.publications:
            plist[p.pub_type] += 1
            for a in p.authors:
                alist[p.pub_type].add(a)
        # create union of all authors
        ua = alist[0] | alist[1] | alist[2] | alist[3]

        data = [
            ["Number of publications"] + plist + [sum(plist)],
            ["Number of authors"] + [ len(a) for a in alist ] + [len(ua)] ]
        return (header, data)

    def get_average_authors_per_publication_by_author(self, av):
        header = ("Author", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "All publications")

        astats = [ [[], [], [], []] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [self.authors[i].name]
            + [ func(L) for L in astats[i] ]
            + [ func(list(itertools.chain(*astats[i]))) ]
            for i in range(len(astats)) ]
        return (header, data)


    def get_publications_by_author(self):
        header = ("Author", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        astats = [ [0, 0, 0, 0] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type] += 1

        data = [ [self.authors[i].name] + astats[i] + [sum(astats[i])]
            for i in range(len(astats)) ]
        return (header, data)

    def get_average_authors_per_publication_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type].append(len(p.authors))
            except KeyError:
                ystats[p.year] = [[], [], [], []]
                ystats[p.year][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(L) for L in ystats[y] ]
            + [ func(list(itertools.chain(*ystats[y]))) ]
            for y in ystats ]
        return (header, data)

    def get_publications_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type] += 1
            except KeyError:
                ystats[p.year] = [0, 0, 0, 0]
                ystats[p.year][p.pub_type] += 1

        data = [ [y] + ystats[y] + [sum(ystats[y])] for y in ystats ]
        return (header, data)

    def get_average_publications_per_author_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year]
            except KeyError:
                s = np.zeros((len(self.authors), 4))
                ystats[p.year] = s
            for a in p.authors:
                s[a][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(ystats[y][:, i]) for i in np.arange(4) ]
            + [ func(ystats[y].sum(axis=1)) ]
            for y in ystats ]
        return (header, data)

    def get_author_totals_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year][p.pub_type]
            except KeyError:
                ystats[p.year] = [set(), set(), set(), set()]
                s = ystats[p.year][p.pub_type]
            for a in p.authors:
                s.add(a)
        data = [ [y] + [len(s) for s in ystats[y]] + [len(ystats[y][0] | ystats[y][1] | ystats[y][2] | ystats[y][3])]
            for y in ystats ]
        return (header, data)

    def calculate_searchAuthors(self,author):
        publications = 0
        conference_papers=0
        journals = 0
        books=0
        coauthors=0
        flag = True
        lista= []
        first=0
        last=0
        book_chapters=0
        for p in self.publications:
            if len(p.authors)!=1:
                if self.authors[p.authors[0]].name == author:
                	first +=1
                if self.authors[p.authors[len(p.authors)-1]].name == author:
                	last +=1
            for a in p.authors:
                if str(self.authors[a].name)==author:
                    publications+=1
                    if p.pub_type==0:
                        conference_papers+=1
                    if p.pub_type==1:
                        journals+=1
                    if p.pub_type==2:
                        books+=1
                    if p.pub_type==3:
                        book_chapters+=1
                    for i in p.authors:
                        if str(self.authors[i].name)!=author and str(self.authors[i].name) not in lista:
                          lista.append(str(self.authors[i].name)) 
                          coauthors+=1
                
        return (publications,conference_papers,journals,book_chapters,books,coauthors,first,last)    

    def add_publication(self, pub_type, title, year, authors):
        if year == None or len(authors) == 0:
            print "Warning: excluding publication due to missing information"
            print "    Publication type:", PublicationType[pub_type]
            print "    Title:", title
            print "    Year:", year
            print "    Authors:", ",".join(authors)
            return
        if title == None:
            print "Warning: adding publication with missing title [ %s %s (%s) ]" % (PublicationType[pub_type], year, ",".join(authors))
        idlist = []
        for a in authors:
            try:
                idlist.append(self.author_idx[a])
            except KeyError:
                a_id = len(self.authors)
                self.author_idx[a] = a_id
                idlist.append(a_id)
                self.authors.append(Author(a))
        self.publications.append(
            Publication(pub_type, title, year, idlist))
        if (len(self.publications) % 100000) == 0:
            print "Adding publication number %d (number of authors is %d)" % (len(self.publications), len(self.authors))

        if self.min_year == None or year < self.min_year:
            self.min_year = year
        if self.max_year == None or year > self.max_year:
            self.max_year = year

    
    def degrees_of_separation(self,author1,author2):
        #create graph   
        edges=collections.defaultdict(list)
        nodes=set()
        for p in self.publications:
            for a in range(len(p.authors)):
            	nodes.add(str(self.authors[p.authors[a]].name))
                for c in range(a+1,len(p.authors)):
                    edges[str(self.authors[p.authors[a]].name)].append(str(self.authors[p.authors[c]].name))
                    edges[str(self.authors[p.authors[c]].name)].append(str(self.authors[p.authors[a]].name))
        visited = {author1: 0}
        path = {}
        
        while nodes: 
            min_node = None
            for node in nodes:
              if node in visited:
                 if min_node is None:
                    min_node = node
                 elif visited[node] < visited[min_node]:
                    min_node = node
            if min_node is None:
                 break

            nodes.remove(min_node)
            current_weight = visited[min_node]

            for edge in edges[min_node]:
                  weight = current_weight + 1
                  if edge not in visited or weight < visited[edge]:
                       visited[edge] = weight
                       path[edge] = min_node
        
        try:
            return visited[author2]-1
        except KeyError:
        	return 'X'




    def calculate_searchPartName(self,part_name):
        matching_Authors1 = [];
        temp = []
        matching_Authors_sur = []
        matching_Authors_fir = []
        matching_Authors_mid = []
        matching_Authors_subsur = []
        matching_Authors_subfir = []
        matching_Authors_submid = []
        for i in self.authors:
            full_name = str(i.name).split()
            if((full_name[len(full_name)-1].lower()).startswith(part_name.lower()) == True):
                matching_Authors_sur.append(full_name)
            elif((full_name[0].lower()).startswith(part_name.lower()) == True):
                matching_Authors_fir.append(full_name)
            elif ((len(full_name)>2) and ((full_name[1].lower()).startswith(part_name.lower()) == True) == True):
                matching_Authors_mid.append(full_name)
            elif ( part_name.lower() in full_name[-1].lower() ):
                matching_Authors_subsur.append(full_name)
            elif ( part_name.lower() in full_name[0].lower() ):
                matching_Authors_subfir.append(full_name)
            elif ((len(full_name)>2) and part_name.lower() in full_name[1].lower() ):
                matching_Authors_submid.append(full_name)
            elif ( ( part_name.lower() in i.name.lower() ) == True):
                temp.append(full_name)

            else:
                pass
        matching_Authors1.append(sorted(matching_Authors_sur, key=itemgetter(-1,0,1)))
        matching_Authors1.append(sorted(matching_Authors_fir, key=itemgetter(0,-1,1)))
        matching_Authors1.append(sorted(matching_Authors_mid, key=itemgetter(1,-1,1)))
        matching_Authors1.append(sorted(matching_Authors_subsur, key=itemgetter(-1,0,1)))
        matching_Authors1.append(sorted(matching_Authors_subfir, key=itemgetter(0,-1,1)))
        matching_Authors1.append(sorted(matching_Authors_submid, key=itemgetter(1,-1,1)))
        matching_Authors1.append(temp)
        matching_Authors=[]
        
        for i in matching_Authors1:
            for j in i:
                string=''
                for k in j:
                   string+=str(k)+' '
                matching_Authors.append(string.strip())
        return (matching_Authors)
        
    def _get_collaborations(self, author_id, include_self):
        data = {}
        for p in self.publications:
            if author_id in p.authors:
                for a in p.authors:
                    try:
                        data[a] += 1
                    except KeyError:
                        data[a] = 1
        if not include_self:
            del data[author_id]
        return data

    def get_coauthor_details(self, name):
        author_id = self.author_idx[name]
        data = self._get_collaborations(author_id, True)
        return [ (self.authors[key].name, data[key])
            for key in data ]

    def get_network_data(self):
        na = len(self.authors)

        nodes = [ [self.authors[i].name, -1] for i in range(na) ]
        links = set()
        for a in range(na):
            collab = self._get_collaborations(a, False)
            nodes[a][1] = len(collab)
            for a2 in collab:
                if a < a2:
                    links.add((a, a2))
        return (nodes, links)

class DocumentHandler(handler.ContentHandler):
    TITLE_TAGS = [ "sub", "sup", "i", "tt", "ref" ]
    PUB_TYPE = {
        "inproceedings":Publication.CONFERENCE_PAPER,
        "article":Publication.JOURNAL,
        "book":Publication.BOOK,
        "incollection":Publication.BOOK_CHAPTER }

    def __init__(self, db):
        self.tag = None
        self.chrs = ""
        self.clearData()
        self.db = db

    def clearData(self):
        self.pub_type = None
        self.authors = []
        self.year = None
        self.title = None

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        if name in self.TITLE_TAGS:
            return
        if name in DocumentHandler.PUB_TYPE.keys():
            self.pub_type = DocumentHandler.PUB_TYPE[name]
        self.tag = name
        self.chrs = ""

    def endElement(self, name):
        if self.pub_type == None:
            return
        if name in self.TITLE_TAGS:
            return
        d = self.chrs.strip()
        if self.tag == "author":
            self.authors.append(d)
        elif self.tag == "title":
            self.title = d
        elif self.tag == "year":
            self.year = int(d)
        elif name in DocumentHandler.PUB_TYPE.keys():
            self.db.add_publication(
                self.pub_type,
                self.title,
                self.year,
                self.authors)
            self.clearData()
        self.tag = None
        self.chrs = ""

    def characters(self, chrs):
        if self.pub_type != None:
            self.chrs += chrs
