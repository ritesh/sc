#from twisted.enterprise import adbapi
import reconpool
from twisted.internet import reactor
from subprocess import Popen, PIPE
from twisted.python import log
import re,string
import time
import optparse
jphide = re.compile(r"(.*)jphide\([\*]{3}\)(.*)")
outguess = re.compile(r"(.*)outguess(.*)\([\*]{3}\)")
jsteg = re.compile(r"(.*)jsteg(.*)\([\*]{3}\)")
f5 = re.compile(r"(.*)f5(.*)\([\*]{3}\)")
typeofsteg = "jofp" #jphide, jsteg, outguess and f5

def getstuff(sensitivity, spidername):
    """docstring for getstuff"""
    return dbpool.runInteraction(__getstuff, sensitivity, spidername)

def __getstuff(txn,sensitivity,spidername):
    txn.execute("SELECT * FROM data WHERE spidername=%s", (spidername))
    result = txn.fetchone()
    while result is not None:
        runcmd(result, sensitivity)
        result = txn.fetchone()
    reactor.stop()

def errhandler(l):
    print l

def runcmd(row, sensitivity):
    cmd = "stegdetect -t %s -s %s %s" % (typeofsteg, sensitivity, "~/images/scraper/"+row[2])
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    output = p.stdout.read()
    err = p.stderr.read()
    if output:
        data = output.split()
        if re.match("^[negative|skipped]", data[2].strip()) is None:
            processdata(row[0], data[2], sensitivity)
    else:
        log.err(err)
def processdata(row, data,sensitivity):
    return dbpool.runInteraction(__processdata, row, data,sensitivity)
def __processdata(txn, row, data,sensitivity):
    res = convertnum(data)
    txn.execute(\
            "SELECT * FROM analysis WHERE FK_data=%s AND sensitivity=%s", (row, sensitivity)
            )
    dbresult = txn.fetchone()
    if dbresult:
        print "Already added!"
    else:
        txn.execute(\
                """INSERT INTO
                analysis(FK_data,sensitivity,positive,jsteg,outguess,jphide,invsecrets,f5,appended,created)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (row,sensitivity,res[0], res[1], res[2], res[3], res[4], res[5],res[6],time.time()) 
                )
        print "Added to db!"

def convertnum(data):
    results = [0,0,0,0,0,0,0]
    #results positive, jsteg, outguess, jphide, invsecrets, f5, appended
    print data
    if jphide.match(data):
        results[3] = 3 
        results[0] = 1
    if outguess.match(data):
        results[2] = 3
        results[0] = 1
    if jsteg.match(data):
        results[0] = 1
        results[1] = 3
    if f5.match(data):
        results[0] = 1
        results[5] = 3
    return results
if __name__ == '__main__':
    opt = optparse.OptionParser()
    opt.add_option('--sensitivity', '-s')
    opt.add_option('--spidername', '-p')
    options, arguments = opt.parse_args()
    dbpool = reconpool.ReConnectionPool("MySQLdb", host='storo', user='ritesh', passwd='6510',db='ritesh' )
    getstuff(options.sensitivity, options.spidername).addErrback(errhandler)
    reactor.run()

