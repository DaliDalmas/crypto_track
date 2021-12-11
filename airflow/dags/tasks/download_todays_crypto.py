from bs4 import BeautifulSoup
import requests as rq
import pandas as pd
from datetime import datetime

def get_data():
    page=1
    all_coins = {}
    while True:
        web_page = rq.get(f'https://coinmarketcap.com/?page={page}').content
        soup = BeautifulSoup(web_page)
        the_row = soup.find_all("tr")[1:]
        if len(the_row)==0:
            break
        for a_row in the_row:
            try:
                coin_name_tags = a_row.find_all('p',class_='iworPT')
                if len(coin_name_tags)>0:
                    coin_name = coin_name_tags[0].getText()
                else:
                    coin_name = a_row.find_all('span')[3].getText()
            except Exception as e:
                print(e)

            try:
                coin_value_tags = a_row.find_all('a',class_='cmc-link')
                if len(coin_value_tags)==4:
                    coin_value = a_row.find_all('a',class_='cmc-link')[1].find('span').getText()
                elif len(the_row)==1:
                    coin_value = a_row.find_all('span')[-2].getText()
            except Exception as e:
                print(e)
            all_coins[coin_name] = [coin_value.replace('$','')]
        page += 1
        todays_data = pd.DataFrame(all_coins).T.reset_index()
        todays_data.columns = ['coin_name','coin_value']
        todays_data['currency'] = 'usd'
        todays_data['read_time'] = datetime.now()
        todays_data.to_csv('temp_csvs/todays_coin.csv',index=False)
    return None
if __name__=='__miin__':
    get_data()