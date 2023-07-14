import xml.etree.ElementTree as ET
import requests
import time
from openpyxl import Workbook 
def xml_to_dict(element):
    result = {}
    for child in element:
        if len(child) == 0:
            result[child.tag] = child.text
        else:
            result[child.tag] = xml_to_dict(child)
    return result
def fillSheet(sheet,data,row):#建立一個function
     for column, value in enumerate(data,1):
        sheet.cell(row = row,column = column,value = value)
def returnStrDayList(startYear,startMonth,endYear,endMonth,day = "01"):
    result = []
    if startYear == endYear:
        for month in range(startMonth,endMonth+1):
            month = str(month)
            if len(month) == 1:
                month = "0" + month
            result.append(str(year)+month+day)
    for year in range(startYear,endYear+1):
        if year == startYear:
            for month in range(startMonth,13):
                month = str(month)
                if len(month) == 1:
                    month = "0" + month
                result.append(str(year)+month+day)
        elif year == endYear:
            for month in range(1,endMonth+1):
                month = str(month)
                if len(month) == 1:
                    month = "0" + month
                result.append(str(year)+month+day)
        else:
            for month in range(1,13):
                month = str(month)
                if len(month) == 1:
                    month = "0" + month
                result.append(str(year)+month+day)
    return result
    
   
# 讀取XML檔案
tree = ET.parse("data.xml")
root = tree.getroot()
# 將XML轉換為字典
data_dict = xml_to_dict(root)
fields = ["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"]
wb = Workbook()#建立excel檔案
sheet = wb.active#讓excel啟動
sheet.title = "fields"
fillSheet(sheet,fields,1)
startYear,startMonth = int(data_dict["startYear"]),int(data_dict["startMonth"])
endYear,endMonth = int(data_dict["endYear"]),int(data_dict["endMonth"])
yearList = returnStrDayList(startYear,startMonth,endYear,endMonth)
print(yearList)
row = 2
for YearMonth in yearList:
    rq = requests.get(data_dict["url"],params={
        "response":"json",
        "date": YearMonth,
        "stockNo": data_dict["stockNo"]
    })
    jsonData = rq.json()
    dailyPriceList = jsonData.get("data",[])
    for dailyPrice in dailyPriceList:
        fillSheet(sheet,dailyPrice,row)
        row += 1
    time.sleep(3)
name = data_dict["excelName"]
wb.save("暫存.xlsx")#存檔