#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from random import randint

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://jwr2131:cde34rfvCDE#$RFV@35.196.158.126/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  
  # DEBUG: this is debugging code to see what request looks like
  #print request.args


  #
  # example of a database query
  #
  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html")

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/manager')
def manager():
  return render_template("manager.html")

@app.route('/approvedorders')
def approvedorders():
  cursor = g.conn.execute("SELECT * FROM approval")
  names = []
  for row in cursor:
    names.append(row) 
  cursor.close()
  context = dict(data = names)
  return render_template("approvedorders.html", **context)

@app.route('/clubcontent')
def clubcontent():
  cursor = g.conn.execute("SELECT * FROM club_content")
  names = []
  for row in cursor:
    names.append(row) 
  cursor.close()
  context = dict(data = names)
  return render_template("clubcontent.html", **context)

@app.route('/customers')
def customers():
  cursor = g.conn.execute("SELECT * FROM customer")
  names = []
  for row in cursor:
    names.append(row) 
  cursor.close()
  context = dict(data = names)
  return render_template("customers.html", **context)

@app.route('/employees')
def employees():
  cursor = g.conn.execute("SELECT * FROM employees")
  names = []
  for row in cursor:
    names.append(row) 
  cursor.close()
  context = dict(data = names)
  return render_template("employees.html", **context)

@app.route('/orders')
def orders():
  cursor = g.conn.execute("SELECT * FROM orders")
  names = []
  for row in cursor:
    names.append(row) 
  cursor.close()
  context = dict(data = names)  
  return render_template("orders.html", **context)
                        
@app.route('/shippedorders')
def shippedorders():
  cursor = g.conn.execute("SELECT * FROM ship")
  names = []
  for row in cursor:
    names.append(row) 
  cursor.close()
  context = dict(data = names)  
  return render_template("shippedorders.html", **context)
                         
@app.route('/clubsignups')
def clubsignups():
  cursor = g.conn.execute("SELECT * FROM signed_up")
  names = []
  for row in cursor:
    names.append(row) 
  cursor.close()
  context = dict(data = names)
  return render_template("clubsignups.html", **context)       

@app.route('/tastingrooms')
def tastingrooms():
  cursor = g.conn.execute("SELECT * FROM tasting_room")
  names = []
  for row in cursor:
    names.append(row) 
  cursor.close()
  context = dict(data = names)  
  return render_template("tastingrooms.html", **context)                                      
                                              
# Example of adding new data to the database                        
@app.route('/add', methods=['POST'])
def add():
  cid = randint(10000,99999)
  fname = request.form['First_Name']
  lname = request.form['Last_Name']
  telno = request.form['Mobile_Number']
  address = request.form['Address']
  city = request.form['City']
  zip_code = request.form['Zip']
  state = request.form['State']
  country = request.form['Country']
  fullname = fname + " " + lname
  g.conn.execute('INSERT INTO customer VALUES (cid,tel_num,full_name,state,city,zip,address)', \
                cid,telno,fullname,state,city,zip_code,address)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
