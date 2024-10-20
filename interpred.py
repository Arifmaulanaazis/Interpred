import telebot
import json
import logging
from datetime import datetime
from database_interaksi import database_interaksi
from database_synonim import database_synonim

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('bot_interactions.log')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def normalize_drug_name(drug_name_input, synonym_database):
    pengulangan = 0
    normalized_name = drug_name_input.lower()
    for drug_name in synonym_database:
        if drug_name.lower() == normalized_name:
            return drug_name
        elif normalized_name in [i.lower() for i in synonym_database[drug_name]['synonim']]:
            return drug_name
        elif normalized_name in [i.lower() for i in synonym_database[drug_name]['product']]:
            return drug_name
        else:
            pengulangan += 1
            if pengulangan == len(synonym_database):
                return drug_name_input

def prediksi(list_obat, data, synonym_database):
    normalized_list_obat = [normalize_drug_name(obat, synonym_database) for obat in list_obat]
    
    list_interaksi = []
    for obat in normalized_list_obat:
        try:
            for interaksi in data[obat]:
                if interaksi in normalized_list_obat:
                    index_obat = normalized_list_obat.index(obat)
                    index_interaksi = normalized_list_obat.index(interaksi)

                    if normalized_list_obat[index_obat] != list_obat[index_obat] and normalized_list_obat[index_interaksi] == list_obat[index_interaksi]:
                        list_interaksi.append([f"{list_obat[index_obat]}/" + obat, interaksi, data[obat][interaksi]])

                    elif normalized_list_obat[index_obat] == list_obat[index_obat] and normalized_list_obat[index_interaksi] != list_obat[index_interaksi]:
                        list_interaksi.append([obat, f"{list_obat[index_interaksi]}/" + interaksi, data[obat][interaksi]])

                    elif normalized_list_obat[index_obat] != list_obat[index_obat] and normalized_list_obat[index_interaksi] != list_obat[index_interaksi]:
                        list_interaksi.append([f"{list_obat[index_obat]}/" + obat, f"{list_obat[index_interaksi]}/" + interaksi, data[obat][interaksi]])

                    else:
                        list_interaksi.append([obat, interaksi, data[obat][interaksi]])
        except KeyError:
            pass

    sorted_interaksi = [sorted(sublist) for sublist in list_interaksi]
    unique_sorted_interaksi = list(set(tuple(sublist) for sublist in sorted_interaksi))
    sublist_counts = {tuple(sublist): sorted_interaksi.count(sublist) for sublist in unique_sorted_interaksi}
    hasil_shorting = []
    for sublist, count in sublist_counts.items():
        string_terpanjang = max(sublist, key=len)
        daftar_interaksi = list(sublist)
        daftar_interaksi.remove(string_terpanjang)
        daftar_interaksi.append(string_terpanjang)
        hasil_shorting.append(daftar_interaksi)
    return hasil_shorting

def predict_interactions(list_obat, data, synonym_database):
    hasil_prediksi = prediksi(list_obat, data, synonym_database)
    if len(hasil_prediksi) > 0:
        result_message = 'Interactions:\n'
        for index, data_interaksi in enumerate(hasil_prediksi):
            result_message += f'{index+1}. {data_interaksi[0]} & {data_interaksi[1]}: {data_interaksi[2]}\n'
        return result_message
    else:
        return 'No interactions were found between the included drugs.'

try:
    with open('token.json') as token_file:
        token_data = json.load(token_file)
        TOKEN = token_data['token']
except FileNotFoundError:
    print("The file 'token.json' was not found.")
    exit(1)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        logging.info(f"Message from user: {message.from_user.username} (ID: {message.from_user.id}), Text: {message.text}")

        if message.text.startswith('prediction:'):
            list_obat = message.text.split(':')[1].strip().split(',')
            if len(list_obat) >= 2:
                hasil_prediksi = predict_interactions(list_obat, database_interaksi, database_synonim)
                logging.info(f"Prediction result for {message.from_user.username}: {hasil_prediksi}")
                bot.reply_to(message, hasil_prediksi)
            else:
                example_format = "Example format:\nprediction: drug1, drug2, drug3 (minimum 2 drugs and separated by commas ',' without spaces)"
                logging.warning(f"Incorrect format from user: {message.from_user.username}. {example_format}")
                bot.reply_to(message, f"The format entered is incorrect.\n{example_format}")

        elif message.text == '/start' or message.text == '/help':
            help_message = "The correct format for predicting drug interactions is as follows:\n\nprediction: drug1, drug2, drug3\n\nMinimum 2 drugs and separated by commas ',' without spaces."
            bot.send_message(message.chat.id, help_message)

        else:
            example_format = "Example format:\nprediction: drug1, drug2, drug3 (minimum 2 drugs and separated by commas ',' without spaces)"
            logging.warning(f"Incorrect message format from user: {message.from_user.username}. {example_format}")
            bot.send_message(message.chat.id, f"The format entered is incorrect.\n{example_format}")

    except Exception as e:
        logging.error(f"Error encountered: {e}")
        bot.reply_to(message, f"There is an error: {e}")

print("Interpred bot | Created by: @arif maulana azis")
print('Bot is running...')

while True:
    try:
        bot.polling()
    except Exception as e:
        logging.error(f"Polling error: {e}")
        pass
