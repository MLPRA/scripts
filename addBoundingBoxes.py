#!/usr/bin/python

from PIL import Image

# Get image sizes like width, height and color depth
def getImageSizes(file):
    image         = Image.open(file)
    width, height = image.size
    depth         = len( image.getbands() )
    return (width, height, depth)

import os
import lxml.etree
import lxml.builder

def worker(image_folder='no_building'):
    """
    Script for creating bounding boxes around non-building images.
    Restriction: The image folder must be in the same directory as the script.
    """
    
    # XML structure
    E         = lxml.builder.ElementMaker()
    ROOT      = E.annotation
    FOLDER    = E.folder
    PATH      = E.path
    FILENAME  = E.filename
    SOURCE    = E.source
    DATABASE  = E.database
    SIZE      = E.size
    WIDTH     = E.width
    HEIGHT    = E.height
    DEPTH     = E.depth
    SEGMENTED = E.segmented
    OBJECT    = E.object
    NAME      = E.name
    POSE      = E.pose
    TRUNCATED = E.truncated
    DIFFICULT = E.difficult
    BNDBOX    = E.bndbox
    XMIN      = E.xmin
    YMIN      = E.ymin
    XMAX      = E.xmax
    YMAX      = E.ymax
    
    # General settings
    database   = 'Unknown'
    segmented  = int(False) # 0
    name       = 'no_building' # name of the class!!!
    pose       = 'Unspecified'
    truncated  = int(False) # 0
    difficult  = int(False) # 0

    # Directory settings
    working_directory = os.path.dirname(os.path.realpath(__file__))
    source_directory  = os.path.join(working_directory, image_folder)
    target_directory  = os.path.join(source_directory, 'annotations')
    # Checks if the target directory exists and creates it if necessary
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    
    
    
    # Create file list
    included_extensions = ['jpg', 'bmp', 'png', 'gif']
    file_list = [ file_name for file_name in os.listdir( source_directory )
                  if any( 
                      file_name.endswith(extension) for extension in included_extensions
                  )
                ]
    # For each file ...
    for counter, file_name in enumerate(file_list):
        
        # ... get properties
        full_path = os.path.join(source_directory, file_name)
        width, height, depth = getImageSizes(full_path)
        xmin = 0
        ymin = 0
        xmax = width
        ymax = height
        
        # ... create XML document       
        doc = ROOT(
            FOLDER( str(image_folder) ),
            FILENAME( str(file_name) ),
            PATH( str(full_path) ),
            SOURCE(
                DATABASE( str(database) ),
            ),
            SIZE(
                WIDTH( str(width) ),
                HEIGHT( str(height) ),
                DEPTH( str(depth) ),
            ),
            SEGMENTED( str(segmented) ),
            OBJECT(
                NAME( str(name) ),
                POSE( str(pose) ),
                TRUNCATED( str(truncated) ),
                DIFFICULT( str(difficult) ),
                BNDBOX(
                    XMIN( str(xmin) ),
                    YMIN( str(ymin) ),
                    XMAX( str(xmax) ),
                    YMAX( str(ymax) ),
                ),
            ),
        )
        
        # DEBUG:
#        print lxml.etree.tostring(doc, pretty_print=True)
    
        xml_document = lxml.etree.ElementTree(doc)
        
        file_name, _     = os.path.splitext(file_name) # Splits filename into a name and extension part
        target_file      = os.path.join(target_directory, file_name)
        
        xml_document.write(target_file + '.xml', pretty_print=True)
        
    print( "{} files processed.".format(counter+1) )



if __name__ == "__main__":
    try:
        image_folder = raw_input('Image folder (default: no_building): ')
        if not image_folder:
            worker()
        else:
            worker(image_folder)
    except:
        pass