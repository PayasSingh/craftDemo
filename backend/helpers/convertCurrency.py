from forex_python.converter import CurrencyRates, CurrencyCodes

class ConvertCurrency:

  def convert_currency(self, data, oldCurrency):
    '''
    apply exchange rate to the currency
    '''
    typeOfData = ["assets", "liabilities"]
    newCurrency = data["currency"]["currencyCode"]
    c = CurrencyRates()
    rate = c.get_rate(oldCurrency, newCurrency)

    for i in typeOfData:
      fields = data[i]
      for field in fields:
        print(field)
        if field != "totalAssets" and field != "totalLiabilities":
          subField = fields[field]
          for key, item in subField.items():
            if item != " ":
              fields[field][key] = float(item) * rate
        else:
          fields[field] = fields[field] * rate

    # assets = data["assets"]
    # for asset in assets:
    #   print(asset)
    #   if asset != "totalAssets":
    #     subAsset = assets[asset]
    #     for key, item in subAsset.items():
    #       if item != " ":
    #         assets[asset][key] = float(item) * rate
    #   else:
    #     assets[asset] = assets[asset] * rate

    c = CurrencyCodes()
    data["currency"]["currencySymbol"] = c.get_symbol(newCurrency)
    return data