import os
# import datetime # Can use datetime to schedule IP updates for a set time period
import time
import pprint
from bs4 import BeautifulSoup as bsoup
import urllib3
import json


def run():
    # with open("C:\Program Files\WireGuard\Configurations\maki_2.conf", "w") as file:

    #     print(file.write("Able to Write to file"))

    # Google search for Public IP
    googleIpUrl = "https://www.google.com/search?sxsrf=ALeKk00gmMWGmd4e8nw6cy-BQ5-kOML_cw%3A1605983379008&source=hp&ei=kly5X43DOs6z5NoPgJK8-AQ&q=what+is+my+ip&oq=&gs_lcp=CgZwc3ktYWIQAxgAMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnUABYAGCoHGgBcAB4AIABAIgBAJIBAJgBAKoBB2d3cy13aXqwAQo&sclient=psy-ab"
    # other website for finding Public IP
    whatsMyIP = "https://api.myip.com"
    httpBin = "http://httpbin.org/ip" # Add, when IP is in IPV6 format
    # General Header
    hdr = {'User-Agent': 'Mozilla/5.0'}

    Headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "pragma": "no-cache",
        # "referer": "https://www.google.com/",
        "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; ANID=AHWqTUnsC0TIwTVpzxMK8_uTZBsammXK-XHVo0MT0N2PObvJYkEl8qNy6m5UQWBb; SEARCH_SAMESITE=CgQI8I8B; OTZ=5689058_72_76_104100_72_446760; NID=204=CDOhhC4ckOdMxfHx4mpXCGNyfK8wGzA8WSYP0XAPCdc89Z_Cv1GSFgGqAJFPQmLPpDMWi797O4s7n_P9tNv2s-6XJcaVxhdreYLVGqriOdOLIqrw3Gb6mdQKw87HsSzEQwV-N_7z8yEvIJbHg7zMEHhkKWYH4Mrd_ubTGmRu4gaNvfcoFCsvqBFwSqoKPw3C2LQymj9py-vl_KdMJXujguoPQ-hKpGEU2mCUUJvcYmVKnr6IFwbHDuJItZfB_GgID4cWnAsWvzj2dSA9td7zSlv_099EmBcu3qeG8tqG; 1P_JAR=2020-11-22-02; DV=8_fM620wrogscJwiBMaOV26JcL3bXtdcOI1FeSUqggAAAAA",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    }

    try:
        http = urllib3.PoolManager()
        res = http.request("GET", googleIpUrl, headers=Headers, timeout=(10))
        # print(res.status)
        if res.status != 200:  # Attempt to scrape backup Site
            try:
                res = http.request(
                    "GET", whatsMyIP, headers=Headers, timeout=(10))
                # print("Second Site Status: ", res.status)
                parsedHtmlSite = bsoup(res.data, 'lxml')
                dataIP = parsedHtmlSite.find("p")
                JsonDataIP = json.loads(dataIP.text)
                print(JsonDataIP['ip'])
            except urllib3.exceptions.HTTPError as e:
                print(e)
              
        parsedHtml = bsoup(res.data, 'html.parser')
        dataIP = parsedHtml.find_all("span", style='font-size:20px')
        print(dataIP[0].text)

    except urllib3.exceptions.HTTPError as e:
         print(e)

def main():
    run()


if __name__ == "__main__":
    main()
