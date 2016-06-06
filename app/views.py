# views.py 

from django.shortcuts import render, HttpResponse
import requests, ctypes, urllib, urllib2, zipfile,easygui


#Testview = ctypes.windll.user32.MessageBoxA(0, url, 'test', 1)

baseurl = "https://api.github.com/repos/"
basetype = "/zipball/master"
outerPath = "C:\Project\Zip\\"
# Create your views here.

def index(request):
    return HttpResponse('Hello World!')

def test(request):
    return HttpResponse('My second view!')

def downloadRepo(repoName):
    url = baseurl + repoName + basetype
    easygui.msgbox(url)
    local_filename = repoName.split('/')[1]
    local_filename = local_filename.split('\n')[0]
    local_filename = local_filename +".zip"
    easygui.msgbox(local_filename)
    path = outerPath + local_filename
    urllib.urlretrieve(url, path)

    return local_filename


def unzip(zipName):
    path = outerPath + zipName
    easygui.msgbox(path)
    with zipfile.ZipFile(path,'r') as z:
        z.extractall("C:\Project\Unzip")



def repos(request):
    parsedData = []
    if request.method == 'POST':
        filename = request.POST.get('file_input')
        data = []
        with open(filename, 'r') as file:
            data = file.readlines()
        for repo in data:
            try:
                repo = repo.split('\n')[0]
                easygui.msgbox(repo)
                zipName = downloadRepo(repo)
                # ctypes.windll.user32.MessageBoxA(0, zipName, 'test', 1)
                easygui.msgbox(zipName)
                unzip(zipName)
            except:
                easygui.exceptionbox()


    return render(request, 'app/profile.html')


def profile(request):
    parsedData = []
    if request.method == 'POST':
        username = request.POST.get('file_input')

        req = requests.get('https://api.github.com/users/' + username)
        jsonList = []
        jsonList.append(req.json())
        userData = {}
        for data in jsonList:
            userData['name'] = data['name']
            userData['blog'] = data['blog']
            userData['email'] = data['email']
            userData['public_gists'] = data['public_gists']
            userData['public_repos'] = data['public_repos']
            userData['avatar_url'] = data['avatar_url']
            userData['followers'] = data['followers']
            userData['following'] = data['following']
        parsedData.append(userData)
    return render(request, 'app/profile.html', {'data': parsedData})