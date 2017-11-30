import re # Import RE for regular expression operations

def dirname(string):
    """
    Normalizes strings to valid path names.
    
    References: Original code version from the Django Framework 
    (https://www.djangoproject.com/). Function slugify() under 
    template/defaultfilters.py.
    """
    string = string.strip() # Returns a copy of the string with the leading and trailing characters removed.
    string = string.lower() # Returns a copy of the string in which all case-based characters have been lowercased.
    string = re.sub('[^\w\s-]', '', string)
    string = re.sub('[-\s]+', '-', string)
    return string