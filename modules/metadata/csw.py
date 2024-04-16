# -*- coding: utf-8 -*-
import requests, os, re


def putFileToCswServer(url, user, password, file):
    def getCapabilities():

        params = {
            'SERVICE': 'CSW',
            'REQUEST': 'GetCapabilities',
            'VERSION': '2.0.2'
        }

        return requests.get(url=url, params=params)

    def transaction():
        headers = {"Content-Type": "application/xml"}
        params = {
            'SERVICE': 'CSW',
            'REQUEST': 'Transaction',
            'VERSION': '2.0.2'
        }
        data = open(os.path.join(file), 'rb').read()
        return requests.post(url=url, params=params, headers=headers, data=data, auth=(user, password))

    try:
        c = re.compile("Operation name=\"Transaction\"\>")
        response = getCapabilities()
        if bool(response.ok) and not bool(c.findall(response.text)):     # serwer nie obsługuje Transaction
            return False, "Serwer CSW nie obsługuje zdalnego wgrywania plików metadanych"
    except requests.exceptions.InvalidSchema:
        return False, "Niepoprawny adres serwera: %s" % url

    response = transaction()
    if response.ok: # Sukces zapytania
        return [True]
    elif response.status_code == 401:
        return False, "Błąd autoryzacji dla użytkownika '%s'. Sprawdź dane logowania" % user
    elif response.status_code == 400:
        return False, "Błąd wewnętrzny serwera CSW\nKod błędu:\n%s\nOdpowiedź serwera:\n%s\nWięcej informacji:\n%s" % (response.status_code, response.reason, response.text)
    else:   # pozostałe typy błędów
        print(response.reason, response.status_code, response.text, response.ok)
        return False, "Błąd.\nKod błędu:\n%s\nOdpowiedź serwera:\n%s" % (response.status_code, response.reason)
    return [True]


if __name__ == "__main__":
    res = putFileToCswServer(
        url="http://gis.parseta.pl/geoportal/csw",
        user="test",
        password="test",
        file=""
    )
    print(res)