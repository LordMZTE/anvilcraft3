import json
from urllib import request, parse
import ntpath
import os

#Constants:
manifestlocation="src/twitch/manifest.json"
if os.path.exists("mods"):
    if os.listdir("mods"):
        print("mods directory is not empty, delete or empty")
        quit()
else:
    os.mkdir("mods")


try:
    with open(manifestlocation, "r") as manifestfile:
        manifestdata = manifestfile.read()
except:
    print("manifest not found")
    quit()
manifestobj = json.loads(manifestdata)

downloadLinks = []
filecount = len(manifestobj["files"])

i = 0
for file in manifestobj["files"]:
    i += 1
    with request.urlopen("https://addons-ecs.forgesvc.net/api/v2/addon/" + str(file["projectID"]) + "/file/" + str(file["fileID"]) + "/download-url", timeout=1000) as response:
        responseLink = response.read().decode("utf-8")
        downloadLinks.append(responseLink)
        print("(" + str(i) + "/" + str(filecount) + ") Got Download Link For " + ntpath.basename(responseLink))

i = 0
filecount = len(downloadLinks)
for link in downloadLinks:
    i += 1
    filename = ntpath.basename(link)
    request.urlretrieve(link, "mods/" + filename)
    print("(" + str(i) + "/" + str(filecount) + ") Downloaded " + filename)