import requests
import json
import collections

def find_airport(code):
    url = 'https://api.ajala.ng/v1/api/flight/airports?city=' + code
    headers = {"accept": "application/json, text/plain, */*", "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.9", "origin": "https://ajala.ng", "referer": "https://ajala.ng/", "sec-fetch-mode": "cors", "sec-fetch-site": "same-site", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3929.0 Safari/537.36"}
    info = eval(requests.get(url, headers=headers).content)
    return info[0]



def create_payload(flight_type, adults, children, infants, departure_airport, arrival_airport, departure_date, arrival_date, ticket_class):
    payload = collections.OrderedDict()
    segments = []
    origin = collections.OrderedDict()
    origin["airCode"] = departure_airport["airCode"]
    origin["airportName"] = departure_airport["airportName"]
    origin["countryName"] = departure_airport["countryName"]
    origin["countryCode"] = departure_airport["countryCode"]
    origin["cityCode"] = departure_airport["cityCode"]
    origin["city"] = departure_airport["city"]
    origin["state"] = departure_airport["state"]
    origin["typeCode"] = departure_airport["typeCode"]
    arriving = collections.OrderedDict()
    arriving["airCode"] = arrival_airport["airCode"]
    arriving["airportName"] = arrival_airport["airportName"]
    arriving["countryName"] = arrival_airport["countryName"]
    arriving["countryCode"] = arrival_airport["countryCode"]
    arriving["cityCode"] = arrival_airport["cityCode"]
    arriving["city"] = arrival_airport["city"]
    arriving["state"] = arrival_airport["state"]
    arriving["typeCode"] = arrival_airport["typeCode"]
    date = departure_date[6:10] + "-" + departure_date[0:2] + "-" + departure_date[3:5] + "T00:01:00"
    temp = collections.OrderedDict()
    temp["origin"] = origin
    temp["arriving"] = arriving
    temp["departureDate"] = date
    segments.append(temp)
    if flight_type == "Return":
        date = arrival_date[6:10] + "-" + arrival_date[0:2] + "-" + arrival_date[3:5] + "T00:01:00"
        print(date)
        temp = collections.OrderedDict()
        temp["origin"] = arriving
        temp["arriving"] = origin
        temp["departureDate"] = date
        segments.append(temp)
    payload["segments"] = segments
    payload["ticketPolicy"] = "SOTO"
    payload["ticketLocale"] = "International"
    payload["salesCategory"] = "B2C"
    payload["directFlight"] = False
    payload["preferredCabin"] = ticket_class
    payload["tabSessionId"] = "cYkHpJULxcFRrVN"
    passengers = []
    temp = collections.OrderedDict()
    temp["quantity"] = adults
    temp["code"] = "ADULT"
    passengers.append(temp)
    if children != 0:
        temp = collections.OrderedDict()
        temp["quantity"] = children
        temp["code"] = "CHILD"
        passengers.append(temp)
    if infants != 0:
        temp = collections.OrderedDict()
        temp["quantity"] = infants
        temp["code"] = "INFANT"
        passengers.append(temp)
    payload["passengers"] = passengers
    #return payload
    return json.dumps(payload)
    
FlightType = "Oneway"
Adults = 1
Children = 0
Infants = 0
Departure_airport = "LOS"
Arrival_airport = "IST"
Departure_date = "04/01/2021"
Arrival_date = "12/02/2021"
Cabin_class = "Business"

payload = create_payload(FlightType, Adults, Children, Infants, find_airport(Departure_airport), find_airport(Arrival_airport), Departure_date, Arrival_date, Cabin_class)

headers = {"accept": "application/json, text/plain, */*", "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.9", "content-length": "631", "content-type": "application/json;charset=UTF-8", "origin": "https://ajala.ng", "referer": "https://ajala.ng/", "sec-fetch-mode": "cors", "sec-fetch-site": "same-site", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3929.0 Safari/537.36"}
post_url = "https://api.ajala.ng/v1/api/flight/search-minimal"
with requests.Session() as session:
    test = session.post(url=post_url, headers=headers, data=payload)
    temp = test.text
    temp = temp.replace('true', 'True').replace('false', 'False').replace('null', 'None')
    temp = eval(temp)
    sessionId = temp["result"][0]["ref"][-16:-1]
    flights_url = "https://api.ajala.ng/v1/api/flight/components-only"
    flights_headers = {"accept": "application/json, text/plain, */*", "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.9", "origin": "https://ajala.ng", "referer": "https://ajala.ng/flight/search/result", "sec-fetch-mode": "cors", "sec-fetch-site": "same-site", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3929.0 Safari/537.36"}
    output = session.get(url=flights_url, headers=flights_headers, params={"sessionId":sessionId})

with open('ajala_data.json', 'w') as outfile:
    outfile.write(json.dumps(eval(output.text.replace('false', 'False').replace('true', 'True').replace('null', 'None'))))