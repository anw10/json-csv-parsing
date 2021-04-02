import csv
import json
import re


def to_csv(filename):
    rep_row = []

    with open(filename, errors='ignore', encoding='utf8') as f1:
        csv_reader = csv.reader(f1 , delimiter=':')
        for row in csv_reader:
            if len(row) > 3:
                ret_row = row[3]
                ret_row = ret_row.replace(',', '')
                rep_row.append(row[0] + ':' + row[1] + ':' + row[2] + ',' + ret_row)
            else:
                ret_row = row[2]
                ret_row = ret_row.replace(',', ' ')
                rep_row.append(row[0] + ':' + row[1] + ',' + ret_row)
    
    with open("edited"+filename, 'w', errors='ignore') as f1:
        f1.write('\n\n'.join(rep_row))
            
# to_csv("day1.csv")

def findMentions(filename):
    dict_list = []
    field_names= ['datetime', 'author', 'message', 'brandMentioned']

    with open(filename, errors='ignore') as f1:
        csv_reader = csv.DictReader(f1, delimiter=',')
        for row in csv_reader:
            if row['message']:
                chat = row['message']
                if any(re.findall("toyota", chat, re.IGNORECASE)):
                    row['brandMentioned'] = "toyota"
                    dict_list.append(row)
                elif any(re.findall("omega", chat, re.IGNORECASE)):
                    row['brandMentioned'] = "omega"
                    dict_list.append(row)
                elif any(re.findall("emirates", chat, re.IGNORECASE)):
                    row['brandMentioned'] = "emirates"
                    dict_list.append(row)
                else:
                    pass
    
    with open('mentions.csv', 'a+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(dict_list)

findMentions("omega.csv")


def jsonToCsv(filename):
    dict_list = []
    field_names= ['datetime', 'author', 'message']
    ret_list = []

    with open(filename, errors='ignore') as f1:
        csv_reader = csv.reader(f1, delimiter=',')
        count = 0
        for row in csv_reader:
            ret_row = row[1][1:-1]
            res = re.split('},{', ret_row)
            for js in res:
                if js != '':
                    if js != '""':
                        if js[0] != "{":
                            js = "{" + js
                        if js[-1] != "}":
                            js = js + "}"
                        ret_list.append(js)
        
    for js_obj in ret_list:

        data = json.loads(js_obj)
        data.pop('type', None)
        data.pop('id', None)
        data.pop('timestamp', None)
        data.pop('elapsedTime', None)
        data.pop('messageEx', None)
        data.pop('amountValue', None)
        data.pop('amountString', None)
        data.pop('currency', None)
        data.pop('bgColor', None)
    
        data["author"] = data["author"]["name"]

        

    with open('mentions.csv', 'a+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(dict_list)

