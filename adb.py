from twisted.enterprise import adbapi
from twisted.internet import reactor
from subprocess import Popen, PIPE
import re,string
import time
sensitivity = 0.5
def getstuff():
    """docstring for getstuff"""
    return dbpool.runInteraction(__getstuff, "craigslist")

def __getstuff(txn,spidername):
    txn.execute("SELECT * FROM data WHERE spidername = %s LIMIT 1, 100", (spidername))
    result = txn.fetchone()
    while result is not None:
        runcmd(result)
        result = txn.fetchone()
    reactor.stop()

def errhandler(l):
    print l

def runcmd(row):
    cmd = "stegdetect -s %s %s" % (sensitivity, "~/images/scraper/"+row[2])
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    output = p.stdout.read()
    err = p.stderr.read()
    if output:
        data = output.split()
        if re.match("^[negative|skipped]", data[2].strip()) is None:
            #processdata(row[0], data[2])
            print row[0], data[2]
    else:
        print err
def processdata(row, data):
    return dbpool.runInteraction(__processdata, row, data)
def __processdata(txn, row, data):
    numdata=convertnum(data)
    txn.execute(\
            "INSERT INTO analysis(FK_data,sensitivity,positive,jsteg,outguess,jphide,invsecrets,f5,appended, created"
            "VALUES(?,?,?,?,?,?,?,?,?,?)",
            (row,sensitivity,1,1,1,1,1,1,1,time.ctime()))

def convertnum(data):
    pass



dbpool = adbapi.ConnectionPool("MySQLdb", host='storo', user='ritesh', passwd='6510',db='ritesh' )
getstuff().addErrback(errhandler)

reactor.run()
