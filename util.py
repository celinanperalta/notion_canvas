import re

def cleanhtml(raw_html):
        # cleanr = re.compile('<.*?>')
        if (raw_html == None):
            return ""
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

# Change to whatever you want.
def format_course_name(name):
    return name[6:]