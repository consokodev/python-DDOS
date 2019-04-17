#!python3
import sqlite3
import os
from time import sleep
from datetime import datetime
import config

def main():
    conn = sqlite3.connect(config.dbfile)
    c = conn.cursor()
    c.execute('PRAGMA synchronous = OFF')
    c.execute('PRAGMA journal_mode = MEMORY')
    c.execute('PRAGMA busy_timeout = 300000')
    c.execute('CREATE TABLE IF NOT EXISTS accesslog (remote_ip varchar(255), request_time NUMERIC)')
    c.execute('CREATE INDEX IF NOT EXISTS accesslog_index ON accesslog(remote_ip,request_time)')

    fileSize = os.stat(config.logfile).st_size
    print(fileSize)
    while True:
        currentFileSize = os.stat(config.logfile).st_size
        print(currentFileSize)
        if (fileSize == currentFileSize):
            sleep(30)
            print("wait wait wait wait wait wait")
            continue
        file = open(config.logfile, 'r')
        file.seek(fileSize)
        line = file.readline()
        print("=====================" + line)
        while line:
            line.strip()
            listLine = line.split()
            remote_ip = listLine[0]
            print(remote_ip)
            ##convert datetime from nginx log with format 13/Mar/2017:18:51:24 to 2017-03-13 18:51:24
            request_time = datetime.strptime(listLine[3][:13].replace("[","").replace("/","-").replace(":",""), '%d-%b-%Y').strftime('%Y-%m-%d') + " " + listLine[3][13:]
            print(request_time)
            c.execute("INSERT INTO accesslog (remote_ip, request_time) VALUES (?, ?)", (remote_ip, request_time))
            line = file.readline()
        file.close()
        fileSize = currentFileSize
        conn.commit()
    conn.close()

main()
    
    