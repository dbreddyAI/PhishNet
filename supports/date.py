from datetime import datetime

def convert_string_to_date(string):
    return datetime.strptime(
        string,
        '%b %d, %Y')

def sep_store_location(string):
    s = string.split(',')
    x = s[0].split(' ')
    store_name = x[0][0:(len(x[-1]) + 1)]
    location = "%s,%s" % (x[-1], s[-1],)
    # store_name = s[0]
    # location = "%s,%s" % (s[1],s[2],)
    return store_name, location
