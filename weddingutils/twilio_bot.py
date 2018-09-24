#!/usr/bin/python3

## Install required packets:
## $ pip install twilio


from twilio.rest import Client
import configparser
import wedding_gsheet_downloader as wgd


class Twilio:
    def __init__(self, account_sid, auth_token, your_twilio_num):
        self.your_twilio_num = your_twilio_num
        self.client = Client(account_sid, auth_token)

    def send_sms_msg(self, receiver_number, msg):
        message = self.client.messages.create(
                        body=msg,
                        from_= self.your_twilio_num,
                        to=receiver_number
                    )
        print(message.sid)

### helpers
def send_sms_to_people_without_confirmation(guests_dict, twilio_client):
    if guests_dict is None:
        raise Exception('guests_dict is empty!')    
    # extract people without confirmation before the deadline date: 20.09.2018
    msg_0 = 'Cześć, tutaj robot weselny Justyny i Łukasza. Wygląda na to że mija termin potwierdzenia udziału w ich weselu. \
             Potwierdź proszę telefonicznie swoją obecność.\n Justyna: 515323976 , Łukasz: 506305438. Pozdrawiam, Miłego dnia!'
    msg_1 = 'Cześć, tutaj Justyna i Łukasz. Wygląda na to że powoli mija termin potwierdzenia/odmówienia udziału w naszym weselu-27.10.2018\
             Proszę, jeśli już wiesz, potwierdź/odmów telefonicznie swoją obecność.\n Justyna: 515323976, Łukasz: 506305438. Pozdrawiamy, Miłego wieczoru!'
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
            twilio_client.send_sms_msg(guest['phone'], msg_1)
    ## test
    twilio_client.send_sms_msg('515 323 976', msg_1)
    twilio_client.send_sms_msg('506 305 438', msg_1)

# main
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('wedding_utils_config.ini')
    twilio = Twilio(config['TWILIO']['ACCOUNT_SID'], config['TWILIO']['AUTH_TOKEN'], config['TWILIO']['BOT_TWILIO_NUM'])
    send_sms_to_people_without_confirmation(wgd.generate_names_dict(wgd.extract_guests_from_wedding_sheet()), twilio)
