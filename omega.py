import csv
import json
import re
from datetime import datetime


def formatToCsv(filename):
    rep_row = []
    # utf8 encoding since I'm on windows and emojies don't need to be processed

    with open(filename, errors='ignore', encoding='utf8') as f1:
        csv_reader = csv.reader(f1 , delimiter='|')
        for row in csv_reader:
            author_message = re.split(":", row[1])
            time_break = re.split(":", row[0])
            if time_break[0] == "-0":
                hour = 18
                minut = 59
                sec = 59 - int(time_break[1])
            else:
                if len(time_break) > 2:
                    hour = 19 + int(time_break[0])
                    minut = int(time_break[1])
                    sec = int(time_break[2])
                else:
                    hour = 19
                    minut = int(time_break[0])
                    sec = int(time_break[1])
                
            date_add = datetime(2021, 3, 10, hour,minut,sec)
            rep_row.append(date_add.strftime("%Y-%m-%d %H:%M:%S") + ',' + author_message[0] + ',' + author_message[1].replace("," , " "))
            # rep_row.append(row[1])
            # if row:
                # if len(row) > 3:
                #     ret_row = row[3]
                #     ret_row = ret_row.replace(',', '')
                #     rep_row.append(row[0] + ':' + row[1] + ':' + row[2] + ',' + ret_row)
                # else:
                #     ret_row = row[2]
                #     ret_row = ret_row.replace(',', ' ')
                #     rep_row.append(row[0] + ':' + row[1] + ',' + ret_row)
    
    with open("day1_timefix.csv", 'w', errors='ignore') as f1:
        f1.write('\n\n'.join(rep_row))
            

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



def jsonToCsv(filename):
    dict_list = []
    field_names= ['datetime', 'author', 'message']
    ret_list = []

    with open(filename, errors='ignore') as f1:
        csv_reader = csv.reader(f1, delimiter=',')
        # data cleanup *todo: is there a faster way to format the data*
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
        # json.loads returns a dict of the string representaion of a json object
        # if not a json string representation and just a normal dict string representation
        # eval shoul work too but not tested
        data = json.loads(js_obj)

        # pop whatever key you don't want from the dict that json.loads return
        data.pop('type', None)
        data.pop('id', None)
        data.pop('timestamp', None)
        data.pop('elapsedTime', None)
        data.pop('messageEx', None)
        data.pop('amountValue', None)
        data.pop('amountString', None)
        data.pop('currency', None)
        data.pop('bgColor', None)

        # nested dicts in json response
        data["author"] = data["author"]["name"]

        dict_list.append(data)

    with open('day2-7.csv', 'a+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(dict_list)

        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(dict_list)

