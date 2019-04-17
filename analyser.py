#!python3
import subprocess
import sqlite3
import datetime
from time import sleep
import logging
import config
from imp import reload

def main():
    block_list_ip = []

    print("Add IP's attacker into Iptables")
    subprocess.call('iptables -N BLOCKEDIP', shell=True)
    subprocess.call('iptables -A BLOCKEDIP -j LOG --log-level 4 --log-prefix \'blockedip\'', shell=True)
    subprocess.call('iptables -A BLOCKEDIP -p tcp --dport 80 -j DROP', shell=True)

    while True:
        conn = sqlite3.connect(config.dbfile)
        c = conn.cursor()
        c.execute('PRAGMA synchronous = OFF')
        c.execute('PRAGMA journal_mode = MEMORY')
        c.execute('PRAGMA busy_timeout = 300000')
        count_request = c.execute('SELECT remote_ip, count(remote_ip) AS request_num FROM accesslog WHERE request_time BETWEEN ? AND ? GROUP BY remote_ip ORDER BY request_num DESC', (datetime.datetime.now() - datetime.timedelta(seconds=config.timewindow), datetime.datetime.now()))
        line = count_request.fetchone()
        print(line)
        while line:
            reload(config)
            if (line[1] >= config.threshold and line[0] not in block_list_ip and line[0] not in config.exclude_list_ip):
                subprocess.call(['iptables', '-A', 'INPUT', '-s', line[0], '-j', 'BLOCKEDIP'])
                block_list_ip.append(line[0])
                with open('list_ip_block.log', 'a') as f:
                    f.write(line[0])
                with open('manualblockip.sh', 'a') as f_script:
                    f_script.write('iptables -A INPUT -s ' + line[0] + ' -j BLOCKEDIP')
            line = count_request.fetchone()
        sleep(60)
main()
            