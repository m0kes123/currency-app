import xml.etree.ElementTree as ET
from datetime import date, datetime
import requests

def exchange_rate(data: str, curr: str):
    """
    Fetches currency data from the Central Bank of the Russian Federation for the specified date

    Args:
        data (str): date in YYYY-MM-DD format
        curr (str): currency corresponding ISO 4217 standard"

    Returns:
        exchange_rate (str): Exchange rate for the specified currency for the specified date.
    """    
    if data == None:
        data = date.today()
        formatted_date = data.strftime("%d/%m/%Y")
    else:
        date_obj = datetime.strptime(data, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={formatted_date}'
    response = requests.get(url=url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        currency = {}
        exchange_rate = {
            "service": "currency", "data": currency
        }

        if curr == None:
            for cur in root.findall('Valute'):
                char_code = cur.find('CharCode').text
                value = cur.find('Value').text

                currency[char_code] = float(value.replace(',','.'))
            return exchange_rate
        else:
            for cur in root.findall('Valute'):
                char_code = cur.find('CharCode').text
                if char_code == curr:
                    value = cur.find('Value').text

                    currency[char_code] = float(value.replace(',','.'))
            return exchange_rate