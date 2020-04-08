import os
import requests
import sys
import shutil
import re
import threading
from bs4 import BeautifulSoup as soup

THREAD_COUNTER = 0
THREAD_MAX = 10


def get_source(link):
    r = requests.get(link)
    if r.status_code == 200:
        return soup(r.text)
    else:
        sys.exit("[~] Invalid Response Received.")


def filter(html):
    fullImgs = []
    imgs = html.findAll("img")
    for img in imgs:
        if "download" in str(img):
            fullImgs.append(img.find_parent())
    if fullImgs:
        return fullImgs
    else:
        sys.exit("[~] No images detected on the page.")


def requesthandle(link, name, tag):
    global THREAD_COUNTER
    THREAD_COUNTER += 1
    try:
        r = requests.get(link, stream=True)
        if r.status_code == 200 and name != "download.png":
            r.raw.decode_content = True
            f = open(os.path.join(os.getcwd(), '../../tags/'+tag+'/') + name, "wb")
            shutil.copyfileobj(r.raw, f)
            f.close()
            print("[*] Downloaded Image: %s" % name)

    except Exception as error:
        print("[~] Error Occurred with {} : {}".format(name, error))
    THREAD_COUNTER -= 1


def main():
    page = "?p=1"
    pics = 0
    f = open("tags", 'r')
    tagLook = f.readline().replace("\n","")
    if not os.path.exists("..././tags/" + tagLook):
        os.mkdir("../../tags/" + tagLook)
    while True:
        print("Current page is : ", page)
        print("Current tag is : ", tagLook)
        html = get_source(link = "https://www.zerochan.net/" + tagLook + str(page))
        tags = filter(html)
        for tag in tags:
            src = tag.get("href")
            if src:
                src = re.match(r"((?:https?:\/\/.*)?\/(.*\.(?:png|jpg)))", src)
                if src:
                    (link, name) = src.groups()
                    if not link.startswith("http"):
                        link = "https://www.zerochan.net/" + tagLook + str(page) + link
                    _t = threading.Thread(target=requesthandle, args=(link, name.split("/")[-1], tagLook))
                    _t.daemon = True
                    _t.start()
                    pics += 1

                    while THREAD_COUNTER >= THREAD_MAX:
                        pass
        while THREAD_COUNTER > 0:
            pass
        page = html.find(attrs={"rel":"next"}).get("href")
        if (pics > 3000):
            tagLook = f.readline().replace("\n",'')
            page = "?p=1"
            if not os.path.exists("../../tags/"+tagLook):
                os.mkdir("../../tags/"+tagLook)

if __name__ == "__main__":
    main()