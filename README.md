# Instagram Scraper

A simple application for scraping public instagram accounts and download the most recent pictures.

This software has been written as en exercise to get familiar with the following Python modules:

- Request
- Beautiful Soup
- Threading

Anyone using this software will be responsible for the use it makes of the pictures downloaded on its own computer, I suggest to use this application only as a tool to download and backup your own instagram photos.

To run the program:

1. Edit the .py file and specify the instagram urls
2. Call the program with the following command:
   python instagram_scraper.py
3. Multiple threads, one per each instagram account, will be started to download the most recent pictures, duplicated are skipped. Under the folder 'instagram_downloads' you will find the photos organized by instagram handler.
