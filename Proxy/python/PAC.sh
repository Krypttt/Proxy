#!/usr/bin/bash

proxy_addr=$1

if [ -w /usr/lib/firefox/proxy.pac ]; then
    cat > /usr/lib/firefox/proxy.pac << EOF
function FindProxyForURL(url, host){
    if (dnsDomainIs(host, ".slader.com") || dnsDomainIs(host, "ifconfig.me")){
        return "PROXY $proxy_addr; DIRECT"
    }else{
        return "DIRECT";
    }
}
EOF
    echo "Connected to slader from "$proxy_addr
else
    echo "Permission denied. Run the script as root"
fi

firefox_process_id=$(ps aux | grep "/usr/lib/firefox/firefox" | head -n +1 | tr -s ' ' | cut -d ' ' -f 2)
if [ $? -eq 0 ];then
    kill -9 $firefox_process_id
    sudo -u fred firefox
else
    echo "firefox is not up"
fi
