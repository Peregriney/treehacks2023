import os
import urllib.request


def download(url):
    filename = url.split("/")[-1]
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)

download("https://s3.amazonaws.com/fast-ai-imageclas/CUB_200_2011.tgz")

