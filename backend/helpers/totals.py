import babel.numbers
import sys,os

sys.path.insert(0, os.getcwd() + '/helpers')

from convertCurrency import ConvertCurrency

class Totals:

  def calculate_total_assets_or_liabilities(self, data, typeOfData):
    '''
    calculate total assets or liabilities
    '''
    c = ConvertCurrency()
    total = 0.0

    typeOfData = data[typeOfData]
    for obj in typeOfData:
      if obj != "totalAssets" and obj!= "totalLiabilities":
        field = typeOfData[obj]
        for key, item in field.items():
          if item != " ":
            item = item.translate(str.maketrans('','',','))
            total += round(float(item), 2)

    return str(total)

  def calculate_total_networth(self, assets, liabilities, currency):
    '''
    calculate total networth
    '''
    assets = assets.translate(str.maketrans('','',','))
    liabilities = liabilities.translate(str.maketrans('','',','))
    total = round(float(assets) - float(liabilities), 2)

    return str(total)