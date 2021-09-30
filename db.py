url = "postgres://lwzpkrigadvrfh:8a8f7785ea98c6a63b1d0c82606ebdbbbc61ee72049c76a16d55537cdce3100d@ec2-34-233-105-94.compute-1.amazonaws.com:5432/d35v18mrti2v55"
import psycopg2
from datetime import datetime
xconn = psycopg2.connect(url)
cur = xconn.cursor()
cur.execute("create table if not exists packages (id SERIAL, date text NOT NULL, locations jsonb NOT NULL, finaldestination text not null);")
xconn.commit()
del xconn
def add_package(location, finallocation, id=None):
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    if not len(__selectall()) == 0:
        if id is None and select_package(__selectall()[-1][0]) is not None:
            print("first")
            cur.execute("INSERT INTO packages (date, locations, finaldestination) VALUES ('{date}','{location}','{finaldestination}') RETURNING id;".format(date=datetime.now().strftime("%A %B %d %Y %r"), location=location, finaldestination=finallocation))
        elif id != None:
            cur.execute("INSERT INTO packages VALUES ('{id}','{date}','{location}','{finaldestination}') RETURNING id;".format(date=datetime.now().strftime("%A %B %d %Y %r"), location=location, finaldestination=finallocation, id=id))
    else:
        cur.execute("INSERT INTO packages (date, locations, finaldestination) VALUES ('{date}','{location}','{finaldestination}') RETURNING id;".format(date=datetime.now().strftime("%A %B %d %Y %r"), location=location, finaldestination=finallocation))
    conn.commit()
    
    return cur.fetchone()[0]
def select_package(id):
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    cur.execute("SELECT * from packages where id='{}'".format(str(id)))
    return cur.fetchone()
def __selectall():
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    cur.execute("SELECT * from packages where id IS NOT NULL")
    return cur.fetchall()
def update_packages(id, location):
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    package = select_package(id)[2]
    package.append({"date": datetime.now().strftime("%A %B %d %Y %r"), "location": location})
    x = "UPDATE packages set locations = '{packages}' where id='{id}'".format(packages=str(package).replace("'", '"'), id=id)
    print(x)
    cur.execute(x)
    conn.commit()
