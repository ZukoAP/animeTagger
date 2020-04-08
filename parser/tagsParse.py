import requests
def gettags(i):
    r = requests.get("https://www.zerochan.net/tags?p="+str(i)).text.split("\n")
    for line in r:
        for tline in line.split("\t"):
            if "<li ><a href=\"/" in tline and (not "ul" in tline):
                print(tline.split("<")[2].split(">")[1])


gettags(1)