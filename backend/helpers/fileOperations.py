import json
from json.decoder import JSONDecodeError


class FileOperations():

  def read_file(self):
    '''
    open the data file, read it and convert it to JSON Object form JSON string
    '''
    with open("/Users/payassingh/Desktop/net-worth-calculator/backend/data.txt", "r+") as f:
      try:
        data = json.load(f)
        f.seek(0)
      except JSONDecodeError:
        # if file is empty, create an empty list
        f.write(json.dumps([], indent=2))
        data = json.load(f)

    return data