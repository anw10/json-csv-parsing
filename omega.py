import csv
import json
import re


def formatToCsv(filename):
    rep_row = []
    # utf8 encoding since I'm on windows and emojies don't need to be processed
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
    
    newFile = filename + '.csv'
    with open(newFile, 'w', errors='ignore') as f1:
        f1.write('\n\n'.join(rep_row))
            
# formatToCsv('filename')

def findMentions(filename):
    dict_list = []
    field_names= ['datetime', 'author', 'message', 'brandMentioned']

    with open(filename, errors='ignore') as f1:
        csv_reader = csv.DictReader(f1, delimiter=',')
        for row in csv_reader:
            if row['message']:
                chat = row['message']
                if any(re.findall("brand1", chat, re.IGNORECASE)):
                    row['brandMentioned'] = "brand1"
                    dict_list.append(row)
                elif any(re.findall("brand2", chat, re.IGNORECASE)):
                    row['brandMentioned'] = "brand2"
                    dict_list.append(row)
                elif any(re.findall("brand3", chat, re.IGNORECASE)):
                    row['brandMentioned'] = "brand3"
                    dict_list.append(row)
                else:
                    pass
    
    with open('mentions.csv', 'a+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(dict_list)

# findMentions(*filename*)


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

    with open('convertedCSV.csv', 'a+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(dict_list)

# jsonToCsv(*filename*)
