import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import threading

# List here the instagram accounts you want to download
urllist = (
'https://instagram.com/taylorswift/',
'http://instagram.com/usainbolt',
'https://instagram.com/neymarjr/',
'https://instagram.com/burberry',
'https://instagram.com/vevo/'
)

download_folder = os.path.join(os.getcwd(), 'instagram_downloads')

def downloadUrl(url):
    res = requests.get(url)
    # Raise expection if we couldn't read the webpage
    res.raise_for_status()

    # Folder name
    instagram_handle = url[url.find('instagram.com')+len('instagram.com')+1:-1]
    folder_path = os.path.join(download_folder, instagram_handle)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    soup = BeautifulSoup(res.text,"html.parser")
    # All the pictures URLs to download are in the script tag
    scripts = soup.select('script')
    # Precisely yhe script tag #5
    picscript = scripts[5]
    # From the text of the script tag element we use display_src
    # to detect the start of each picture URL. The first element
    # of the slipt is not a picture.
    nrange = max(0,len(picscript.text.split('"display_src":'))-1)
    for i in range(1, nrange):
        urlpic = picscript.text.split('"display_src":')[i].split('},')[0]
        # "https:\\/\\/scontent.cdninstagram.com\\/hphotos-xfa1\\/t51.2885-15\\/e15\\/11809535_437579513099534_959907557_n.jpg"
        urlpic = urlpic.replace("\\","")
        urlpic = urlpic.replace("https","http").strip('"')
        path = os.path.join(folder_path, "pic_" + urlpic[urlpic.rfind('/')+1:])
        # download only new files
        if not os.path.exists(path):
            r = requests.get(urlpic)
            if r.status_code == 200:
    		    with open(path, 'wb') as f:
    			    for chunk in r.iter_content(1024):
    				    f.write(chunk)
            print 'Downloaded picture ', path

print "Start application"
# List of download threads, to speed up the process.
downloadThreads = []
# Create directory for downloads if not exists
if not os.path.exists(download_folder):
    os.mkdir(download_folder)

for myurl in urllist:
    print 'Start download for {}'.format(myurl)
    downloader = threading.Thread(target=downloadUrl, args=(myurl,))
    downloadThreads.append(downloader)
    downloader.start()

# Wait for all downloaders to complete
for downloader in downloadThreads:
    downloader.join()

print 'All downloaded completed'



