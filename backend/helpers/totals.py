
class Totals:

  def calculate_total_assets_or_liabilities(self, data, typeOfData):
    '''
    calculate total assets
    '''
    total = 0.0

    typeOfData = data[typeOfData]
    for obj in typeOfData:
      if obj != "totalAssets" and obj!= "totalLiabilities":
        field = typeOfData[obj]
        for key, item in field.items():
          if item != " ":
            total += float(item)

    return total

  def calculate_total_networth(self, assets, liabilities):
    '''
    calculate total
    '''
    total = assets - liabilities

    return total