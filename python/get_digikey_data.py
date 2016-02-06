import urllib2
import sys
from bs4 import BeautifulSoup

output_scr = open("/tmp/get_digikey_data.scr", "w+")

if len(sys.argv) != 2:
    print "error: invalid number of inputs"
    print "usage: python get_digikey_data.py [url]"
    sys.exit(1)

url = sys.argv[1]
headers = { 'User-Agent' : 'Mozilla/5.0' }
postdata = None
#if not url.endswith(".html"):
#    url += ".html"
try:
    req = urllib2.Request(url, postdata, headers)
    data = urllib2.urlopen(req).read()
    soup = BeautifulSoup(data, 'html.parser')
except:
    print "error: invalid url or unable to connect"
    sys.exit(1)

table = soup.find("table",{"id":"product-details"})
# hacky af
DIST_NAME = "Digi-Key"
DIST_PN = table.find(None,{"id":"reportPartNumber"}).contents[2].strip()
MFG_NAME = table.find(None,{"itemprop":"name"}).contents[0].strip()
MFG_PN = table.find(None,{"itemprop":"model"}).contents[0].strip()
DESC = table.find(None,{"itemprop":"description"}).contents[0].strip()

print "DIST_NAME: " + DIST_NAME
print "DIST_PN: " + DIST_PN
print "MFG_NAME: " + MFG_NAME
print "MFG_PN: " + MFG_PN
print "DESC: " + DESC

output_scr.write("attribute DIST_NAME '" + DIST_NAME + "'\n")
output_scr.write("attribute DIST_PN '" + DIST_PN + "'\n")
output_scr.write("attribute MFG_NAME '" + MFG_NAME + "'\n")
output_scr.write("attribute MFG_PN '" + MFG_PN + "'\n")
output_scr.write("description '" + DESC + "<br><a href=\"" + url + "\">Digi-key Page</a>';\n")

output_scr.close()
