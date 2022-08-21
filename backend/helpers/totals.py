
class Totals:

  def calculate_total_assets_or_liabilities(self, data, typeOfData):
    '''
    calculate total assets or liabilities
    '''
    total = 0.0

    typeOfData = data[typeOfData]
    for obj in typeOfData:
      if obj != "totalAssets" and obj!= "totalLiabilities":
        field = typeOfData[obj]
        for key, item in field.items():
          if item != " ":
            total += round(float(item), 2)

    return str(total)

  def calculate_total_networth(self, assets, liabilities):
    '''
    calculate total networth
    '''
    total = round(float(assets) - float(liabilities), 2)

    return str(total)