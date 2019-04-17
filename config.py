dbfile = 'ddos_ip'
logfile = '/var/log/nginx/access.log'

####interval time that analyser rerun to collect DDOS IP, suggest 60s
timewindow = 31536000
####if a IP create more than threshold number of requests in 60s. It will be block 
threshold = 3
####while list ip
exclude_list_ip = ['192.168.26.1', '192.168.26.0']