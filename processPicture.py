import urllib.request as urllib
import requests
from getFaces import get_faces

def downloadFile(url, filename):
    testfile = urllib.URLopener()
    testfile.retrieve(url, filename)

def uploadFile(filename, url):
    fin = open(filename, "rb")
    headers = { 'x-ms-blob-type': 'BlockBlob', 'content-type': 'image/jpeg' }
    r = requests.put(url, data = fin, headers = headers)
    print(r.text)
    fin.close()

def process_picture(url_in, url_out):
    downloadFile(url_in, "input.jpg")
    get_faces("input.jpg", "output.jpg")
    uploadFile("output.jpg", url_out)
