#!/usr/bin/env python2.7

"""
jackson raffety
jwr2131
hw1.3
"""

import os
import datetime as dt
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from random import randint

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://jwr2131:cde34rfvCDE#$RFV@35.196.158.126/proj1part2"

engine = create_engine(DATABASEURI)

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

@app.route('/')
def index():
 
  cursor = g.conn.execute("SELECT DISTINCT bottle_count,frequency, price FROM signed_up")
  names = []
  for row in cursor:
    names.append(row) 
  cursor.close()
  context = dict(data = names)
  return render_template("index.html", **context)

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
  fullname = fname + ' ' + lname
  g.conn.execute('INSERT INTO customer(cid,tel_num,full_name,state,city,zip,address) VALUES (%s,%s,%s,%s,%s,%s,%s)', \
                (cid,telno,fullname,state,city,zip_code,address))
  bottlecount = request.form['Bottle_Count']
  frequency = request.form['Frequency']
  date_now = dt.datetime.today().strftime('%Y-%m-%d')
  price = 0
  if frequency == 'Annual':
    price = 150 if bottlecount == 6 else 300
  if frequency == 'Bi-Annual':
    price = 300 if bottlecount == 6 else 450
  g.conn.execute('INSERT INTO signed_up(bottle_count,frequency,since,price,cid) VALUES (%s,%s,%s,%s,%s)', \
                 (bottlecount,frequency.lower(),date_now,price,cid))
  
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
