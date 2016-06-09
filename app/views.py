
# views.py 

from django.shortcuts import render, HttpResponse
import requests, ctypes, urllib, urllib2, zipfile, easygui, json, sys, os


#Testview = ctypes.windll.user32.MessageBoxA(0, url, 'test', 1)

baseurl = "https://api.github.com/repos/"
basetype = "/zipball/master"
outerPath = "C:\Project\Zip\\"
commits = "/commits"
parsedData = []
amountData = []
authentication = "?client_id=15c00265fc566965deff&client_secret=b78c4bc8b339953d1f9f2830d4a54b3119414dd8"



# Create your views here.



def downloadRepo(repoName):
    url = baseurl + repoName + basetype + authentication
    local_filename = repoName.split('/')[1]
    local_filename = local_filename.split('\n')[0]
    local_filename = local_filename +".zip"
    path = outerPath + local_filename
    urllib.urlretrieve(url, path)

    return local_filename


def unzip(zipName):
    path = outerPath + zipName
    with zipfile.ZipFile(path,'r') as z:
        z.extractall("C:\Project\Unzip")



def repos(request):
 
    if request.method == 'POST':
        filename = request.POST.get('file_input')
        createDirs()
        data = []
        with open(filename, 'r') as file:
            data = file.readlines()
        for repo in data:
            try:
                repo = repo.split('\n')[0]
                zipName = downloadRepo(repo)
                # ctypes.windll.user32.MessageBoxA(0, zipName, 'test', 1)
                unzip(zipName)
                projectCommits(repo)
                
            except:        
                easygui.exceptionbox()

    return render(request, 'app/profile.html', {'data': parsedData})





def projectCommits(repo):
    data = {}
    formattedData = []
    url = baseurl + repo + commits + authentication
    response = urllib2.urlopen(url)
    data = json.load(response)
    for commit in data:
        presenting = {}

        repository = repo
        presenting["repo"] = repository

        SHAKey = commit['sha']
        presenting["sha"] = SHAKey

        committer = commit["commit"]["committer"]
        presenting["name"] = committer["name"]
        presenting["date"] = committer["date"]
        presenting["email"] = committer["email"]

        message = commit["commit"]["message"]
        presenting["message"] = message


        parsedData.append(presenting)








def getCommitFiles(repo, shaKey):
    data = {}
    url = baseurl + repo + commits + "/" + shaKey + authentication
    response = urllib2.urlopen(url)
    data = json.load(response)
    files = data["files"]
    allFileData = []
    for file in files:
        filedata = {}

        filedata["repo"] = repo
        filedata["filename"] = file["filename"]
        filedata["status"] = file["status"]

        allFileData.append(filedata)
    return allFileData



def listFiles(fileData):

    for file in fileData:
        amountDataSingle = {}      
        if len(amountData) == 0:
            amountDataSingle["repo"] = file["repo"]
            amountDataSingle["filename"] = file["filename"]
            amountDataSingle["amount"] = 1
            amountData.append(amountDataSingle)

        else:

            for index, amount in enumerate(amountData):           
                if file["filename"] != amountData[index]["filename"]:
                    amountDataSingle["repo"] = file["repo"]
                    amountDataSingle["filename"] = file["filename"]
                    amountDataSingle["amount"] = 1
                    amountData.append(amountDataSingle)
                    easygui.msgbox(amountData)
                    easygui.msgbox("i was here aswell")
                    break
                else:


                    result = filter(lambda lambdafile: lambdafile["filename"] == file["filename"] and lambdafile["repo"] == file["repo"], amountData)
                    if result != None:
                        amountData[index]["amount"] +=1
                        easygui.msgbox("i was here")
                        break
                    else:
                        amountDataSingle["repo"] = file["repo"]
                        amountDataSingle["filename"] = file["filename"]
                        amountDataSingle["amount"] = 1
                        amountData.append(amountDataSingle)
                        break

    return amountData


def sortItems(timesArray):
    sortedList = sorted(timesArray, key=lambda k: k["amount"])
    return sortedList


def getTenWithNumber(sortedList):
    sortedList = sortedList[:10]

    for index, data in enumerate(sortedList):
        data["place"] = index + 1
    return sortedList


def createDirs():
    projectDir = "C:\Project"
    zipDir = "C:\Project\Zip"
    unzipDir = "C:\Project\Unzip"

    if not os.path.exists(projectDir):
        os.makedirs(projectDir)

    if not os.path.exists(zipDir):
        os.makedirs(zipDir)

    if not os.path.exists(unzipDir):
        os.makedirs(unzipDir)



def topten(request):
    if len(parsedData) == 0:
        return render(request, 'app/nodata.html')

    for commit in parsedData:
        topFileData = getCommitFiles(commit["repo"], commit["sha"])
        timesIncommit = listFiles(topFileData)
        sortedList = sortItems(timesIncommit)
        topTenList = getTenWithNumber(sortedList)
    #     easygui.codebox("Msg", "Title", timesIncommit)

    return render(request, 'app/commits.html', {'data': topTenList})



# # def profile(request):
#     parsedData = []
#     if request.method == 'POST':
#         username = request.POST.get('file_input')

#         req = requests.get('https://api.github.com/users/' + username)
#         jsonList = []
#         jsonList.append(req.json())
#         userData = {}
#         for data in jsonList:
#             userData['name'] = data['name']
#             userData['blog'] = data['blog']
#             userData['email'] = data['email']
#             userData['public_gists'] = data['public_gists']
#             userData['public_repos'] = data['public_repos']
#             userData['avatar_url'] = data['avatar_url']
#             userData['followers'] = data['followers']
#             userData['following'] = data['following']
#         parsedData.append(userData)
#     return render(request, 'app/profile.html', {'data': parsedData})