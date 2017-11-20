from comp62521 import app
from database import database
from flask import (render_template, request)
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
		(data[1][i]).append(temp_name[-1])
	return data[1][0]

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

    if (no_col!=None):
		args["data"] = sorting(get_from_db, int(no_col), 0)
    elif (no_col==None):
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
	
    if (no_col!=None):
		args["data"] = sorting(get_from_db, int(no_col), 0)
    elif (no_col==None):
		args["data"] = get_from_db
    return render_template('statistics_details.html', args=args)
