from comp62521 import app
from database import database
from flask import (render_template, request, redirect, url_for)
from operator import itemgetter

#status = idle (no sorting)
status_2 = 0

def format_data(data):
    fmt = "%.2f"
    result = []
    for item in data:
        if type(item) is list:
            result.append(", ".join([ (fmt % i).rstrip('0').rstrip('.') for i in item ]))
        else:
            result.append((fmt % item).rstrip('0').rstrip('.'))
    return result

def sort_by_surname(data):
	for i in range(0,len(data[1])):
		temp_name = (data[1][i][0]).split()
		if(temp_name[-1].isdigit() == True):
			temp_name[-1] = temp_name[-2] + temp_name[-1]
		if(temp_name[-1].startswith('(') == True):
			temp_name[-1] = temp_name[-2]
			if(temp_name[-1].isdigit() == True):
				temp_name[-1] = temp_name[-3] + temp_name[-2]
		(data[1][i]).append(temp_name[-1])
	sorted_tuple = sorting(data, -1, 1)
	for i in sorted_tuple[1]:
		i.pop()
	return (sorted_tuple[0], sorted_tuple[1])

def sorting(data, no_col, stat):
	global status_2
	data_sorted =[]
	data_sorted.append(data[0])

	#ascending
	if (status_2 == 0):
		status_2 = 1
		data_sorted.append(sorted(data[1], key=itemgetter(no_col) , reverse=True))
	#descending
	elif (status_2 == 1):
		status_2 = 0
		data_sorted.append(sorted(data[1], key=itemgetter(no_col) , reverse=False))

	if (stat == 1):
		return data_sorted[0], data_sorted[1]
	
	else:
		return (data_sorted[0], data_sorted[1])

@app.route("/searchPartName")
def showSearchPartName():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"stats"}
    args["title"] = "Search for Author by part name"
    author = str(request.args.get("author"))
    app.debug=True
    first = str(request.args.get('first'))
    args["first"] = first
    if (first=="None"):
        args["part_name"]=db.calculate_searchPartName(author)
        if (len(args["part_name"])==1):
            args["authors"]=args["part_name"][0]
	    args["onlyOne"] = "1"
	    args["flag_none"] = "0"
	elif(len(args["part_name"])==0):
	    args["flag_none"] = "1"
	else:
	   args["flag_none"] = "0" 
    else:
	args["flag_none"] = "0"
    return render_template("searchPartName.html",args=args)
    
@app.route("/stats")
def showFirstLast():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"stats"}
    args["title"] = "Stats"
    args["data"] = db.calculate_first_last_sole()
    return render_template("stats.html", args=args)

@app.route("/searchAuthor")
def showSearchAuthor():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"stats"}
    args["title"] = "Search for Author"
    author = str(request.args.get("author"))
    publications,conference,journals,chapters,books,coauthors,first,last=db.calculate_searchAuthors(author)
    args["publications"]=publications
    args["conference"]=conference
    args["journals"]=journals
    args["chapters"]=chapters
    args["books"]=books
    args["coauthors"]=coauthors
    args["first"]=first
    args["last"]=last
    return render_template("searchAuthor.html",args=args)

@app.route("/StatsForAuthor")
def showStatsForAuthor():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"stats"}
    #args["title"] = "Stats"
    author = str(request.args.get("author"))
    '''if author=="None":
	print("if")
	author = args["author"]'''
    #else:
	#print("else")
    '''if args["author"]!="None":
	print("if")
	author = args["author"]
    else:
	print("else")'''
        
    args["title"] = "Stats for "+author
    publications, conference_papers, journals, book_chapters, books, coauthors, first, Fconference_papers, Fjournals, Fbook_chapters,Fbooks, last, Lconference_papers, Ljournals, Lbook_chapters, Lbooks, sole, Sconference_papers, Sjournals, Sbook_chapters, Sbooks=db.StatsForAuthor(author)
    args["publications"]=publications
    args["conference_papers"]=conference_papers
    args["journals"]=journals
    args["book_chapters"]=book_chapters
    args["books"]=books
    args["coauthors"]=coauthors
    args["first"]=first
    args["Fconference_papers"]=Fconference_papers
    args["Fjournals"]=Fjournals
    args["Fbook_chapters"]=Fbook_chapters
    args["Fbooks"]=Fbooks
    args["last"]=last
    args["Lconference_papers"]=Lconference_papers
    args["Ljournals"]=Ljournals
    args["Lbook_chapters"]=Lbook_chapters
    args["Lbooks"]=Lbooks
    args["sole"]=sole
    args["Sconference_papers"]=Sconference_papers
    args["Sjournals"]=Sjournals
    args["Sbook_chapters"]=Sbook_chapters
    args["Sbooks"]=Sbooks
    return render_template("StatsForAuthor.html",args=args)

@app.route("/degrees")
def showDegrees():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"stats"}
    authors= db.get_all_authors_names()


    args["title"] = "Degrees of Separation"
    author1 = str(request.args.get("author#1"))
    author2 = str(request.args.get("author#2"))
    degree = db.degrees_of_separation(author1,author2)
    args["author1"]= author1
    args["author2"] = author2
    args["degree"] = degree
    args["authors"] = authors
    return render_template("degreesOfSeparation.html",args=args)

@app.route("/GraphForCoauthor")
def GraphForCoauthor():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset": dataset, "id": "stats"}
    
    adata = str(request.args.get("author"))
    author = adata.split("(")
    author_name = author[0]
    
    hdata, cdata = db.get_coauthor_data(0, 3000, 4)
    coauthors=[]
    
    for i in cdata:
        author = i[0].split("(")[0].strip()
        if str(author).strip() == str(author_name).strip():
            coauthors.append(str(i[1]))

    co = str(coauthors).split(", ")
    co_list=[]
    for author in co:
        temp = author.split("['")
        temp1 = author.split("']")
        if len(temp) ==1:
           co_list.append(author.split("(")[0].strip())
        elif len(temp) >1:
           co_list.append(temp[1].split("(")[0].strip())
        elif len(temp1) >1:
           co_list.append(temp1[0].split("(")[0].strip())

    args["author"] = author_name
    args["title"] = "The Coauthors of " + author_name
    args["coauthor"] = co_list

    return render_template('GraphForCoauthor.html',args=args)


@app.route("/authordetails")
def showAuthorDetails():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"stats"}
    args["title"] = "Authors' Publications by Type"
    header,subheader,data1=db.calculate_authors_details()
    data=[]
    for i in range(len(data1)):
    	temp=[]
    	for j in range(0,13):
    		temp.append(data1[i][j])
    		if j % 3 == 0 and j != 0:
    			temp.append(' ')
    	data.append(temp)
    args["header"]=header[1:]
    args["author"]=header[0]
    args["subheader"]=subheader
    args["data"] = data
    return render_template("authordetails.html", args=args)

@app.route("/averages")
def showAverages():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"averages"}
    args['title'] = "Averaged Data"
    tables = []
    headers = ["Average", "Conference Paper", "Journal", "Book", "Book Chapter", "All Publications"]
    averages = [ database.Stat.MEAN, database.Stat.MEDIAN, database.Stat.MODE ]
    no_col = request.args.get('col')
    no_table = request.args.get('table')


    tables.append({
        "id":1,
        "title":"Average Authors per Publication",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_per_publication(i)[1])
                for i in averages ] })
    tables.append({
        "id":2,
        "title":"Average Publications per Author",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_per_author(i)[1])
                for i in averages ] })
    tables.append({
        "id":3,
        "title":"Average Publications in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_in_a_year(i)[1])
                for i in averages ] })
    tables.append({
        "id":4,
        "title":"Average Authors in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_in_a_year(i)[1])
                for i in averages ] })
    
    get_from_db = []
    lista = []
    for i in range(0,4):
    	lista.append(tables[0]["header"])
        lista.append(tables[i]["rows"])
	get_from_db.append(lista)
	lista = []
    if (no_col!=None) and (no_table!=None):
		y = sorting(get_from_db[int(no_table)], int(no_col), 0)
		tables[int(no_table)]["rows"] = y[1]
		
    args['tables'] = tables
    return render_template("averages.html", args=args)

@app.route("/coauthors")
def showCoAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset":dataset, "id":"coauthors"}
    args["title"] = "Co-Authors"
    no_col = request.args.get('col')

    start_year = db.min_year
    if "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    pub_type = 4
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    get_from_db = db.get_coauthor_data(start_year, end_year, pub_type)
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_type"] = pub_type
    args["min_year"] = db.min_year
    args["max_year"] = db.max_year
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_str"] = PUB_TYPES[pub_type]

    if (no_col != None):
		if (int(no_col) == 0):
			args["data"] = sort_by_surname(get_from_db)
		else:
			args["data"] = sorting(get_from_db, int(no_col), 0)
    elif (no_col == None):
		args["data"] = get_from_db

    return render_template("coauthors.html", args=args)

@app.route("/")
def showStatisticsMenu():
    dataset = app.config['DATASET']
    args = {"dataset":dataset}
    return render_template('statistics.html', args=args)

@app.route("/statisticsdetails/<status>")
def showPublicationSummary(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":status}
    no_col = request.args.get('col')
    flag_author = 0
    app.debug = True
    
    if (status == "publication_summary"):
        args["title"] = "Publication Summary"
	get_from_db = db.get_publication_summary()
		
    if (status == "publication_author"):
        args["title"] = "Author Publication"
        get_from_db = db.get_publications_by_author()
	flag_author = 1

    if (status == "publication_year"):
        args["title"] = "Publication by Year"
        get_from_db = db.get_publications_by_year()
	
    if (status == "author_year"):
        args["title"] = "Author by Year"
        get_from_db = db.get_author_totals_by_year()
	
    if (no_col != None):
		if (flag_author == 1 and int(no_col) == 0):
			args["data"] = sort_by_surname(get_from_db)
		else:
			args["data"] = sorting(get_from_db, int(no_col), 0)
    elif (no_col == None):
		args["data"] = get_from_db
    return render_template('statistics_details.html', args=args)

@app.route("/PubYearChart")
def showChart_publicationsbyyear():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"stats"}
    args["title"] = "Stats"
    args["data"] = db.get_publications_by_year()
    return render_template("PubYearChart.html", args=args)

@app.route("/AuthorYearChart")
def showChart_authorsbyyear():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"stats"}
    args["title"] = "Stats"
    args["data"] = db.get_author_totals_by_year()
    return render_template("AuthorYearChart.html", args=args)

@app.route("/PubAuthorChart")
def showChart_publicationsbyauthor():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"stats"}
    args["title"] = "Stats"
    args["data"] = db.get_publications_by_author()
    return render_template("PubAuthorChart.html", args=args)

@app.route("/StatsChart")
def showChart_Statsforauthor():
    dataset=app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"stats"}
    args["title"] = "Stats"
    args["data"] = db.calculate_first_last_sole()
    return render_template("StatsChart.html", args=args)
