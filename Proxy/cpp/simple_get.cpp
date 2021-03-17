#include <iostream>
#include <string>
#include <curl/curl.h>
#include <fstream>
#include <jsoncpp/json/json.h>
#include <sstream>
#include <vector>
#include <cstring>

using namespace std;

const char *proxyAPIUrl = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=2000&country=all&ssl=yes&anonymity=all";
const string ip2GeoAPIUrl = "http://ip-api.com/json/";

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    ((string*)userp) -> append((char*)contents, size* nmemb);
    return size * nmemb;
}

string webGet(const char *Url) {
    CURL *curl;
    CURLcode res;
    string readBuffer;
    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, Url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
    return readBuffer;
}

vector<string> intoVector(string inData) {
    istringstream _(inData);
    vector<string> tmpVector;
    for (string line; getline(_, line);) {
        tmpVector.push_back(line);
    }
    return tmpVector;
}

Json::Value ip2Geo_data(string ipaddr) {
    Json::Reader reader;
    Json::Value data;
    string combined_ip = ip2GeoAPIUrl + ipaddr.substr(0, ipaddr.find(":"));
    char char_combined_url[combined_ip.size()+1];
    strcpy(char_combined_url, combined_ip.c_str());
    string tmp = webGet(char_combined_url);
    if (!reader.parse(tmp.c_str(), data)) {
        cout << "Failed to parse" << reader.getFormattedErrorMessages();
    }
    return data;
}

void ip2Geo(string ipaddr) {
    Json::Value data = ip2Geo_data(ipaddr);
    cout << "IP Address: " << data["query"].asString();
    cout << ",Country: " << data["country"].asString();
    cout << ", City: " << data["city"].asString();
    cout << endl;
}

int main() {
    string rawList;
    rawList = webGet(proxyAPIUrl);
    vector<string> ipaddrList = intoVector(rawList);
    for (vector<string>::iterator it = ipaddrList.begin(); it != ipaddrList.end(); it++) {
        //cout << *it << endl;
        string test_ip = *it;
        ip2Geo(test_ip);
    }
    return 0;
}
