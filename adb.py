from twisted.enterprise import adbapi
from twisted.internet import reactor
from subprocess import Popen, PIPE
import re,string
import time
import optparse
#sensitivity = 0.25 
jphide = re.compile(r"(.*)jphide\([\*]{1,3}\)(.*)")
outguess = re.compile(r"(.*)outguess(.*)\([\*]{1,3}\)")
typeofsteg = "jo" #jphide and outguess

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
            print row[0], data[2]
    else:
        print err
def processdata(row, data,sensitivity):
    return dbpool.runInteraction(__processdata, row, data,sensitivity)
def __processdata(txn, row, data,sensitivity):
    res = convertnum(data)
    txn.execute(\
            "INSERT INTO analysis(FK_data,sensitivity,positive,jsteg,outguess,jphide,invsecrets,f5,appended,created) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(row,sensitivity,res[0], res[1], res[2], res[3], res[4], res[5],res[6],time.time()) 
            )
    print "Added to db!"

def convertnum(data):
    results = [0,0,0,0,0,0,0]
    print data
    if jphide.match(data):
        results[3] = 1
        results[0] = 1
    if outguess.match(data):
        results[2] = 1
        results[0] = 1
    return results
if __name__ == '__main__':
    opt = optparse.OptionParser()
    opt.add_option('--sensitivity', '-s')
    opt.add_option('--spidername', '-p')
    options, arguments = opt.parse_args()
    dbpool = adbapi.ConnectionPool("MySQLdb", host='storo', user='ritesh', passwd='6510',db='ritesh' )
    getstuff(options.spidername, options.sensitivity).addErrback(errhandler)
    reactor.run()

