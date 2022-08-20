import json

class FileOperations():

  def read_file(self):
    '''
    open the data file, read it and convert it to JSON Object form JSON string
    '''
    with open("/Users/payassingh/Desktop/net-worth-calculator/backend/data.txt", "r+") as f:
      data = json.load(f)
      f.seek(0)
    return data