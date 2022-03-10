import string
from numpy import true_divide
import requests
import json
import csv

#Script has been wrote to support up to 299 devices on JC, if you add more please put a new request to JC
#Go to Asset tiger, tools, export
#Select table assets, chose asset tag id, description,serial no, location, category, assigned to.
#put the csv in the same folder as the script and run it
#Api key used is user key for JC


dataCSV = []
#CSV
with open('./asset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    line_toEvaluate = 0

    for row in csv_reader:
        if line_count != 0:
            if "Laptops" in row[4] or "Desktop PCs" in row[4]:
                #print(f'\t TAG: {row[0]} Description: {row[1]} Serial: {row[2]}  Location: {row[3]} Category: {row[4]} Assigned to {row[5]}')
                dataCSV.append([row[0],row[1], row[2].upper(),row[3],row[4],row[5]])
                line_toEvaluate += 1
        line_count += 1
    print(f'Processed {line_count} lines from CSV.')
    print(f'{line_toEvaluate} results ready to evaluate.')
    #print(dataCSV)

#JumpCloud
#1st request
url = "https://console.jumpcloud.com/api/systems"
#querystring = {"fields":"","limit":"","search":"SOME_STRING_VALUE","skip":"0","sort":"","filter":"SOME_STRING_VALUE"}
querystring = {"fields":"serialNumber","limit":"100","search":"","skip":"0","sort":"","filter":""}
headers = {"x-api-key": "XXXXXXX YOUR API KEY XXXXXXX"}
response = requests.request("GET", url, headers=headers, params=querystring)
json_pretty1 = json.loads(response.text)

#To print and see it beautifully
#json_pretty = json.dumps(json_pretty,indent=2)
resultNotFound = []

#Evaluate 1st request of jc against CSV
for key,value in json_pretty1.items():
    if 'results' in key:
        #Machines in jc
        for value2 in value:
            #Serial number to detail from JC
            #Compare to AT here
            found = False
            #serial numbers in CSV
            for detail in dataCSV:
                if detail[2] == value2['serialNumber'].upper():
                    found = True
            if found == False and "VMWARE" not in value2['serialNumber'].upper():
                resultNotFound.append(value2['serialNumber'])
                print(f"Serial number not found in AssetTiger: {value2['serialNumber']}")

#2nd request to JC
querystring = {"fields":"serialNumber","limit":"100","search":"","skip":"99","sort":"","filter":""}
response = requests.request("GET", url, headers=headers, params=querystring)
json_pretty2 = json.loads(response.text)
for key,value in json_pretty2.items():
    if 'results' in key:
        #Machines in jc
        for value2 in value:
            #Serial number to detail from JC
            #Compare to AT here
            found = False
            #serial numbers in CSV
            for detail in dataCSV:
                if detail[2] == value2['serialNumber'].upper():
                    found = True
            if found == False and "VMWARE" not in value2['serialNumber'].upper():
                resultNotFound.append(value2['serialNumber'])
                print(f"Serial number not found in AssetTiger: {value2['serialNumber']}")

#3rd request to JC
querystring = {"fields":"serialNumber","limit":"100","search":"","skip":"199","sort":"","filter":""}
response = requests.request("GET", url, headers=headers, params=querystring)
json_pretty2 = json.loads(response.text)
for key,value in json_pretty2.items():
    if 'results' in key:
        #Machines in jc
        for value2 in value:
            #Serial number to detail from JC
            #Compare to AT here
            found = False
            #serial numbers in CSV
            for detail in dataCSV:
                if detail[2] == value2['serialNumber'].upper():
                    found = True
            if found == False and "VMWARE" not in value2['serialNumber'].upper():
                resultNotFound.append(value2['serialNumber'])
                print(f"Serial number not found in AssetTiger: {value2['serialNumber']}")

print("Total ammount of devices missing on Asset Tiger: ", len(resultNotFound))
print("---------------------------------------------------------------------------------")