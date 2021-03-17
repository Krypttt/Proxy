import requests
import threading
import time
import os

url = "https://www.proxyscan.io/api/proxy?format=txt&limit=20&type=https"

def get_list(ret_list):
    # one batch
    ret_list += requests.get(url).text.split('\n')[:-1]

def get_proxy_list():
    ret_list = []
    my_threads = []
    for i in range(1, 20):
        t = threading.Thread(name=i, target=get_list, args=(ret_list,))
        my_threads.append(t)
        print("Start Thread No.{}".format(i))
        t.start()
    for t in my_threads:
        if t.is_alive:
            t.join()
    return list(set(ret_list))

def write_to_file():
    llist = get_proxy_list()
    with open("/etc/proxychains.conf", "w") as fd:
        fd.write("[ProxyList]\n")
        for elem in llist:
            elem = elem.split(":")
            fd.write("https {} {}\n\n".format(elem[0], elem[1]))

write_to_file()
