import requests
import json
import openpyxl


if __name__ == '__main__':
    wb = openpyxl.load_workbook("data/userNames.xlsx")
    sheet = wb.active
    

    response = requests.get("https://codeforces.com/api/contest.standings?contestId=1598&from=1&showUnofficial=false")
    decoded = json.loads(response.text)
    culled = decoded["result"]["rows"][:6000]
    decoded = None
    response = None

    reduced = culled[0:500]
    reduced.extend(culled[1500:2000])
    reduced.extend(culled[3000:3500])
    reduced.extend(culled[4500:5000])

    culled = None

    for i in range(len(reduced)):
        userName = reduced[i]["party"]["members"][0]["handle"]
        cell = "C" + str(i+1)
        # print(cell)
        sheet[cell].value = userName
    wb.save("data/userNames.xlsx")


