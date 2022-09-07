import xlwings as xw

with xw.App(visible=False) as app:
    book = xw.Book("weather.xls")
    sheet = book.sheets['data']
    print(sheet.range('A1').value)
    # xw.Range((k, i)).value = rec
    book.close()

