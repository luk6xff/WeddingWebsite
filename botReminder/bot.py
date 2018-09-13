#!/usr/bin/python3

## Install required packets:
## $ pip install twilio
## GD API setup instructions: https://developers.google.com/drive/api/v3/quickstart/python, gsheets handles it
## $ pip install gsheets
from twilio.rest import Client
import csv
from gsheets import Sheets
import configparser


class Twilio:
    def __init__(self, account_sid, auth_token, your_twilio_num):
        self.your_twilio_num = your_twilio_num
        self.client = Client(account_sid, auth_token)

    def send_sms_msg(self, receiver_number, msg):
        message = self.client.messages.create(
                        body=msg,
                        from_=self.your_twilio_num,
                        to=receiver_number
                    )
        print(message.sid)


def download_sheet_from_gdrive(file_id):
    sheets = Sheets.from_files('credentials.json', 'token.json')
    s = sheets.get(file_id)
    return s


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


### helpers
def send_sms_to_people_without_confirmation(guests_dict, twilio_client):
    if guests_dict is None:
        raise Exception('guests_dict is empty!')    
    # extract people without confirmation before the deadline date: 20.09.2018
    msg_0 = 'Cześć, tutaj robot weselny Justyny i Łukasza. Wygląda na to że zbliża się termin potwierdzenia udziału w ich weselu. \
             Proszę daj telefonicznie znać młodym jaki jest twój status. Jeśli potrzebujesz więcej czasu na zastanowienie, \
             też ich o tym poinformuj, napewno się zgodzą :)  Justyna: 515323976 , Łukasz: 506305438. Pozdrawiam, Miłego dnia!'
    not_confirmed_list = []
    for i, _ in enumerate(guests_dict['name']):
        if guests_dict['invited'][i] == 'T' and guests_dict['confirmed'][i] == '-':
            not_confirmed_list.append({'name':guests_dict['name'][i],
                                       'surname':guests_dict['surname'][i],
                                       'phone':guests_dict['phone'][i]})    
    for guest in not_confirmed_list:
        #print("{} {} - {}".format(guest['name'], guest['surname'], guest['phone']))
        if guest['phone'] is not '-':
            print("sending sms to: {} {} - {}...".format(guest['name'], guest['surname'], guest['phone']))
            twilio_client.send_sms_msg(guest['phone'], msg_0)
    ## test
    #twilio_client.send_sms_msg('515 323 976', msg_0)  

# main
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('bot_config.ini')
    twilio = Twilio(config['TWILIO']['ACCOUNT_SID'], config['TWILIO']['AUTH_TOKEN'], config['TWILIO']['BOT_TWILIO_NUM'])
    sheet = download_sheet_from_gdrive(config['GUESTS_FILE']['WEDDING_GOOGLE_SHEET_FILE_ID'])
    guests = sheet.find(config['GUESTS_FILE']['GUESTS_SHEET_NAME'])
    
    # save as csv
    csv_name = 'guests.csv'
    guests.to_csv(csv_name, encoding='utf-8', dialect='excel')
    send_sms_to_people_without_confirmation(generate_names_dict(guests), twilio)
