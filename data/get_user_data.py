import requests
import openpyxl
import json
import psycopg2


def getJson(username):
    url = "https://codeforces.com/api/"
    method = "user.status"
    args = {"handle": username}

    response = requests.get(url+method, params=args)

    if (response.status_code is not 200):
        print("API REQUEST FAILED, SEE RETURN FOR MORE DETAILS")
        return json.loads(response.text)
    
    decoded = json.loads(response.text)
    decoded = decoded["result"]
    for question in decoded:
        del question['creationTimeSeconds']
        del question['relativeTimeSeconds']
        del question['author']
        del question['programmingLanguage']
        del question['testset']
        del question['passedTestCount']
        del question['timeConsumedMillis']
        del question['memoryConsumedBytes']
        if 'contestId' in question:
            del question['contestId']
    result = json.dumps(decoded)
    result = result.replace("'", "")
    return result




if __name__ == '__main__':
    wb = openpyxl.load_workbook("data/userNames.xlsx")
    sheet = wb.active

    conn = psycopg2.connect(database="userdata", user="postgres", password="a", port='5432')
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    
    with conn.cursor() as cursor:
        for i in range(401, 501):
            userName = sheet['A' + str(i)].value
            result = getJson(userName)
            try:
                cursor.execute("""INSERT INTO data values('{0}', '{1}')""".format(userName, result))
                print(cursor.statusmessage)
            except Exception:
                print("Writing to database failed, continuing")
    