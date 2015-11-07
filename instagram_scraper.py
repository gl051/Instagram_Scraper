#!/usr/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import threading

verbose_mode = False;


def get_urls(config_file):
    if not os.path.isfile(config_file):
        print "Can't find file {}".format(config_file)
        print "Be sure to create a config file as the one provided as a sample"
        return None
    ret_list = []
    with open(config_file,'r') as fin:
        for line in fin:
            ret_list.append(line.strip('\n'))
    return ret_list


def download_url(url):
    global verbode_mode
    # Create directory for downloads if not exists already
    download_folder = os.path.join(os.getcwd(), 'instagram_downloads')
    if not os.path.exists(download_folder):
        os.mkdir(download_folder)

    res = requests.get(url)
    # Raise expection if we couldn't read the webpage
    res.raise_for_status()
    # Folder name
    instagram_handle = url[url.find('instagram.com')+len('instagram.com')+1:-1]
    folder_path = os.path.join(download_folder, instagram_handle)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    print 'Started download {}'.format(instagram_handle)
    soup = BeautifulSoup(res.text,"html.parser")
    # All the pictures URLs to download are in the script tag
    scripts = soup.select('script')
    # Precisely yhe script tag #5
    picscript = scripts[5]
    # From the text of the script tag element we use display_src
    # to detect the start of each picture URL. The first element
    # of the slipt is not a picture.
    nrange = max(0,len(picscript.text.split('"display_src":'))-1)
    counter = 0
    for i in xrange(1, nrange):
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
                counter += 1
            if verbose_mode:
                print 'Downloaded picture ', path
    print 'Completed download {} with {} new pictures'.format(instagram_handle, counter)


# Gather our code in a main() function
def main():
    global verbose_mode

    # Check if verbose mode is on
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == '-verbose':
            verbose_mode = True

    # List of download threads, to speed up the process.
    downloadThreads = []

    # Get the instagram URLs from the config file
    urls = get_urls("config.txt")

    # Per each url start a downaload thread
    for url in urls:
        downloader = threading.Thread(target=download_url, args=(url,))
        downloadThreads.append(downloader)
        downloader.start()

    #Wait for all downloaders to complete
    for downloader in downloadThreads:
        downloader.join()
    print 'All done.'
    
# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
  main()
