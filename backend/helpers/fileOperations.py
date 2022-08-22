import json
from json.decoder import JSONDecodeError
import sys,os

sys.path.insert(0, os.getcwd())


class FileOperations():

  def read_file(self):
    '''
    open the data file, read it and convert it to JSON Object form JSON string
    '''
    with open("data.txt", "r+") as f:
      try:
        data = json.load(f)
        f.seek(0)
      except JSONDecodeError:
        # if file is empty, create an empty list
        f.write(json.dumps([], indent=2))
        data = json.load(f)

    return data

  def write_file(self, dataList):
    '''
    open data file and write new data to it
    '''
    with open('data.txt', 'r+') as f:
      f.seek(0)
      f.write(json.dumps(dataList, indent=2))
      f.truncate()