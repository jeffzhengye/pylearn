from tqsdk import TqApi, TqAuth
api = TqApi(auth=TqAuth("jeffzhengye", "810716Ye"))
quote = api.get_quote("SHFE.a1609")
print (quote.last_price, quote.volume, type(quote))
print(quote)