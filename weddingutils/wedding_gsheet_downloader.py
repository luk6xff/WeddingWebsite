#!/usr/bin/python3

## Install required packets:
## GD API setup instructions: https://developers.google.com/drive/api/v3/quickstart/python, gsheets handles it
## $ pip install gsheets
import csv
from gsheets import Sheets
import configparser


def download_sheet_from_gdrive(file_id):
    sheets = Sheets.from_files('credentials.json', 'token.json')
    s = sheets.get(file_id)
    return s

def extract_guests_from_wedding_sheet():
    config = configparser.ConfigParser()
    config.read('wedding_utils_config.ini')
    sheet = download_sheet_from_gdrive(config['GUESTS_FILE']['WEDDING_GOOGLE_SHEET_FILE_ID'])
    guests = sheet.find(config['GUESTS_FILE']['GUESTS_SHEET_NAME'])
    return guests   

def generate_names_dict(guests_sheet):
    if guests_sheet is None:
        raise Exception('guests_sheet is invalid!')
    names = {'name': [], 'surname': [], 'phone': [], 'invited': [], 'confirmed': [] , 'hotel': [], 'bus': []}
    first_row_num = 4
    # l side
    name = '-'
    row_num = first_row_num
    while True:
        name = guests_sheet['A{}'.format(row_num)]
        if name == '':
            break
        names['name'].append(name)
        names['surname'].append(guests_sheet['B{}'.format(row_num)])
        names['phone'].append(guests_sheet['D{}'.format(row_num)])
        names['invited'].append(guests_sheet['E{}'.format(row_num)])
        names['confirmed'].append(guests_sheet['F{}'.format(row_num)])
        names['hotel'].append(guests_sheet['G{}'.format(row_num)])
        names['bus'].append(guests_sheet['H{}'.format(row_num)])
        row_num = row_num + 1
    # j side
    name = '-'
    row_num = first_row_num
    while True:
        name = guests_sheet['J{}'.format(row_num)]
        if name == '':
            break
        names['name'].append(name)
        names['surname'].append(guests_sheet['K{}'.format(row_num)])
        names['phone'].append(guests_sheet['M{}'.format(row_num)])
        names['invited'].append(guests_sheet['N{}'.format(row_num)])
        names['confirmed'].append(guests_sheet['O{}'.format(row_num)])
        names['hotel'].append(guests_sheet['P{}'.format(row_num)])
        names['bus'].append(guests_sheet['Q{}'.format(row_num)])
        row_num = row_num + 1
    # print(names)
    return names
 

# main
if __name__ == "__main__":
    guests = extract_guests_from_wedding_sheet()  
    # save as csv
    csv_name = 'guests.csv'
    guests.to_csv(csv_name, encoding='utf-8', dialect='excel')
