# -*- coding: utf-8 -*-
import flickrapi
import time
import os
import requests
from PIL import Image
from StringIO import StringIO
from requests.exceptions import ConnectionError
import uuid # Import UUID to generate a unique ID for a file
import normalizer # Import NORMALIZER to create a valid directory name

# Requirements: set environment variables
api_key    = unicode( os.getenv('API_KEY') )
api_secret = unicode( os.getenv('API_SECRET') )

flickr = flickrapi.FlickrAPI(api_key, api_secret)

def worker(search_keywords, num_results):
    """
    Download images from Flickr. 
    
    References: Original code version from gpascualg/flickr-downloader
    (https://github.com/gpascualg/flickr-downloader/blob/master/flickrDownloader.py)
    """
    t0 = time.time()   # Start the timer
    
    # Determine destination
    this_file = os.path.realpath( __file__ )
    this_dir  = os.path.dirname( this_file )
    directory = normalizer.dirname(search_keywords) # Create a valid directory name out of the search keywords
    directory = os.path.join( this_dir, directory )
    
    # If necessary, create a new directory
    if not os.path.exists( directory ):
        os.makedirs( directory )

    per_page = num_results % 501
    page = 1
    i=0
    errorCount=0
    while num_results > 0:
        photos = flickr.photos.search(text=search_keywords, format='parsed-json', per_page=per_page, page=page)
        photos = photos['photos']
        
        print( "Starting download..." )
        
        for photo in photos['photo']:
            # Construct the URL as described: https://www.flickr.com/services/api/misc.urls.html
            size = 'z' # s=75, q=150, t=100, m=240, n=320, -=500, z=640, c=800, b=1024, h=1600, k=2048
            url = 'http://farm' + str(photo['farm']) + '.staticflickr.com/' + str(photo['server']) + '/' + str(photo['id']) + '_' + str(photo['secret']) + '_' + size + '.jpg'
            
            try:
                image = requests.get(url)
            except ConnectionError:
                errorCount+=1
                print( "ConnectionError: Could not download image " + str(i+1) )
            
            filename    = uuid.uuid4() # Create a random unique ID
            destination = os.path.join( directory, '{}.jpg'.format(filename) )
            
            # Save the image
            try:
                with open( destination, 'wb+' ) as file:
                    file.write(image.content)
                print( "completed ====> " + str(i+1) )
            except IOError:
                errorCount+=1
                print( "IOError: Could not save image " + str(i+1) )

            i += 1
        
        # Next page
        num_results -= 500
        page += 1
        
    print( "Everything downloaded!" )
    print( "Errors: " + str(errorCount) )
    t1 = time.time() # Stop the timer
    total_time = t1 - t0 # Calculating the total time required to crawl, find and download all images
    print( "Total time: "+ str(total_time) + " seconds" )
    print("")

try:
    print "Press CTRL-C to exit"
    while(True):
        worker( raw_input('Search term: '), int(raw_input('Number of results: ')) )
except:
    pass