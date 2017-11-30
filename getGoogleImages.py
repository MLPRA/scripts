# -*- coding: utf-8 -*-
"""
    Download images from Google.
    
    Edited by Stefan Fuchs.
    
    References: Original code version from hardikvasa/google-images-download
    (https://github.com/hardikvasa/google-images-download/blob/master/google-images-download.py)
"""

import sys
import urllib2
from   urllib2 import Request, urlopen
from   urllib2 import URLError, HTTPError
# Downloading a web document (page content)
def download_page(url):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:   #If the Current Version of Python is 3.0 or above
        import urllib.request    #urllib library for Extracting web pages
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:                        #If the Current Version of Python is 2.x
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"


# Finding 'Next Image'
def get_next_image(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link      = "no_links"
        return link, end_quote
    else:
        start_line    = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content   = s.find(',"ow"',start_content+1)
        content_raw   = str(s[start_content+6:end_content-1])
        return content_raw, end_content


# Getting all links with the help of 'get_next_image'
def get_all_images(page):
    items = []
    while True:
        item, end_content = get_next_image(page)
        if item == "no_links":
            break
        else:
            items.append(item) # Append all the links in the list named 'Links'
            page = page[end_content:]
    return items


import time # Import the time library to check the time of code execution
import os
import uuid # Import UUID to generate a unique ID for a file
import normalizer # Import NORMALIZER to create a valid directory name
from requests.exceptions import ConnectionError
############## Main Program ############
def worker(search_keywords, num_results):
    t0 = time.time()   # Start the timer
    
    # Search for images
    images = []
    print( "Searching..." )
    
    # Determine destination
    this_file = os.path.realpath( __file__ )
    this_dir  = os.path.dirname( this_file )
    directory = normalizer.dirname(search_keywords) # Create a valid directory name out of the search keywords
    directory = os.path.join( this_dir, directory )
    
    # If necessary, create a new directory
    if not os.path.exists( directory ):
        os.makedirs( directory )
    
    url    = 'https://www.google.com/search?q=' + search_keywords.replace(' ','%20') + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    page   = download_page(url)
    time.sleep(0.1)
    images = images + get_all_images(page)
    
    # Download images
    print( "Starting download..." )
    i=0
    errorCount=0
    while(i < num_results):
        
        try:
            request     = Request( images[i], headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"} )
            response    = urlopen( request, None, 15 )
            image       = response.read()
            response.close();
        except ConnectionError:
            errorCount+=1
            print( "ConnectionError: Could not download image " + str(i+1) )
                          
        filename    = uuid.uuid4() # Create a random unique ID
        destination = os.path.join( directory, '{}.jpg'.format(filename) )
        
        # Save the image
        try:
            with open( destination, 'wb+' ) as file:
                file.write(image)
            print( "completed ====> " + str(i+1) )
        # If there is any IOError
        except IOError:
            errorCount+=1
            print( "IOError: Could not save image " + str(i+1) )
        
        i=i+1;
        
    print( "Everything downloaded!" )
    print( "Errors: " + str(errorCount) )
    t1 = time.time() # Stop the timer
    total_time = t1 - t0 # Calculating the total time required to crawl, find and download all images
    print( "Total time: "+ str(total_time) + " seconds" )
    print("")
############## End of main program ############

try:
    while(True):
        print( "Press CTRL-C to exit" )
        worker( raw_input('Search term: '), int(raw_input('Number of results: ')) )
except:
    pass