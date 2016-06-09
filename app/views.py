
# views.py 

from django.shortcuts import render, HttpResponse
import requests, ctypes, urllib, urllib2, zipfile, easygui, json, sys, os


#Testview = ctypes.windll.user32.MessageBoxA(0, url, 'test', 1)

baseurl = "https://api.github.com/repos/"
basetype = "/zipball/master"
outerPath = "C:\Project\Zip\\"
commits = "/commits"
parsedData = []



# Create your views here.



def downloadRepo(repoName):
    url = baseurl + repoName + basetype
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
        if easygui.ccbox("WARNING: The repositories will be downloaded and unzipped in the background and saved in the folden C:/Project/Zip and C:/Project/Unzip.." + "\n" + "If this is the first time you run this program, these directories will be created automatically.","Warning"):
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
            for repo in parsedData:
                topFileData = getCommitFiles(repo["repo"], repo["sha"])
                timesIncommit = listFiles(topFileData)
                sortedList = sortItems(timesIncommit)

    return render(request, 'app/profile.html', {'data': parsedData})





def projectCommits(repo):
    data = {}
    formattedData = []
    url = baseurl + repo + commits
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
    url = baseurl + repo + commits + "/" + shaKey
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
    amountData = []
    for file in fileData:
        amountDataSingle = {}
        for amount in amountData:

            if file["filename"] not in amount["filename"]:
                amountDataSingle["repo"] = file["repo"]
                amountDataSingle["filename"] = file["filename"]
                amountDataSingle["amount"] = 1
                amountData.append(amountDataSingle)
            else:


                result = filter(lambda lambdafile: lambdafile["filename"] == file["filename"] and lambdafile["repo"] == file["repo"], amountData)
                if result != "":
                    result["amount"] += 1
                else:
                    amountDataSingle["repo"] = file["repo"]
                    amountDataSingle["filename"] = file["filename"]
                    amountDataSingle["amount"] = 1
                    amountData.append(amountDataSingle)

    return amountData


def sortItems(timesArray):
    sortedList = sorted(timesArray, key=lambda k: k["amount"])
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