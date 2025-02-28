import xml.etree.ElementTree as ET
from datetime import date, datetime
import requests
from pathlib import Path
import json


def validate_date(date_str: str) -> bool:
    """
    Checks if the string matches the YYYY-MM-DD format and is a valid date.

    Args:
        date_str (str): Date string to validate.

    Returns:
        bool: True if the date is valid and not in the future, otherwise False.
    """    
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if date_obj.date() > date.today():
            return False
        return True
    except ValueError:
        return False

CURRENCY_CODES_FILE = Path(__file__).parent / "currency_codes.json"

with open(CURRENCY_CODES_FILE, "r", encoding="utf-8") as file:
    ISO_CURRENCY_CODES = set(json.load(file))

def validate_currency(curr: str) -> bool:
    """
    Checks if the currency code is valid according to ISO 4217.

    Args:
        curr (str): Currency code to validate.

    Returns:
        bool: True if the currency code is valid, otherwise False.
    """
    return curr in ISO_CURRENCY_CODES

def exchange_rate(data: str, curr: str):
    """
    Fetches currency data from the Central Bank of the Russian Federation for the specified date

    Args:
        data (str): date in YYYY-MM-DD format
        curr (str): currency corresponding ISO 4217 standard"

    Returns:
        dict: A dictionary containing the exchange rate for the specified currency and date.
              If an error occurs, returns a dictionary with an "error" key containing the error message.
    """    
    if data is None:
        data = date.today()
        formatted_date = data.strftime("%d/%m/%Y")
    else:
        if not validate_date(data):
            return {"error": "Invalid date format or future date. Expected format: YYYY-MM-DD"}
        date_obj = datetime.strptime(data, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")
    
    if curr is not None and not validate_currency(curr):
        return {"error": f"Invalid currency code. Expected one of: {ISO_CURRENCY_CODES}"}
    
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={formatted_date}'
    response = requests.get(url=url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        if not root.findall('Valute'):
            return {"error": "No data available from the Central Bank of Russia for the specified date."}
        
        currency = {}
        exchange_rate = {
            "service": "currency", "data": currency
        }

        if curr is None:
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
    else:
        return {"error": f"Failed to fetch data. HTTP status code: {response.status_code}"}