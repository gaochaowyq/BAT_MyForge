from zipfile import ZipFile
import json


def unzipfile(file):
    if file:
        with ZipFile(file) as myzip:
            with myzip.open('manifest.json','r') as myfile:
                return json.loads(myfile.read().decode('utf-8'))

    else:
        return ('unzipfile has error')