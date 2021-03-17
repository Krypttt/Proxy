import requests
import threading
import json
import random
import sys
import logging

#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format="%(message)s")

proxy_scrape = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=2000&country=all&ssl=yes&anonymity=all"
lumtest = "https://lumtest.com/myip.json"

def getList():
    response = requests.get(proxy_scrape)
    proxy_list = response.text.split('\r\n')[:-1]
    return proxy_list

def avail(proxy, ava_list):
    #port = proxy.split(":")[1]
    headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0"}
    proxies = {"http":"http://"+proxy, "https":"https://"+proxy}
    try:
        response = requests.get(lumtest, proxies=proxies, timeout=1)
        info = json.loads(response.text)
        if response.ok:
            #logging.debug("\033[92mAvailable: {} from {}\033[0m".format(proxy, info['country']))
            sys.stderr.write("\033[92mAvailable: {} from {}\033[0m\n".format(proxy, info['country']))
            ava_list.append(proxy)
    except:
        pass
        #print("\033[91mBad proxy\033[0m")

def main():
    #logging.debug("Proxy List:")
    sys.stderr.write("Proxy List:\n")
    proxy_list = getList()
    ava_list = []
    cnt = 0
    my_threads = []
    for proxy in proxy_list:
        t = threading.Thread(name=proxy, target=avail, args=(proxy, ava_list))
        my_threads.append(t)
        if cnt == 4 or proxy == proxy_list[-1]:
            #logging.debug("{:18s}".format(proxy))
            sys.stderr.write("{:18s}\n".format(proxy))
            cnt = 0
        elif cnt < 4:
            #logging.debug("{:18s}".format(proxy), end='\t')
            sys.stderr.write("{:18s}\t".format(proxy))
            cnt += 1
        t.start()
    for t in my_threads:
        if t.is_alive:
            t.join()

    return ava_list

if __name__ == "__main__":
    ava_list = main()
    random_proxy = random.choice(ava_list)
    print(random_proxy)
