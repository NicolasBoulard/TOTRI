import requests
from urllib3.exceptions import NewConnectionError

from settings import Config


class TotalAPI:
    FUEL_NAME = {
        'excellium98': 'SP98 Excellium',
        'excelliumdiesel': 'Excellium Diesel',
        'gasoil': 'Diesel',
        'SP95E10': 'SP95 E10'

                 }
    def __init__(self, station_code):

        url = f"{Config.TOTAL_API_URL}?Lang=fr_FR&AdditionalData=Items&AdditionalDataFields=Items_Code,Items_Price," \
             f"Items_Availability,Items_UpdateDate&Code={station_code}"
        #url = "http://127.0.0.1:5000/test"

        headers = {"Content-Type": "application/json; charset=utf-8", "Origin": "https://services.totalenergies.fr",
                   "Referer": "https://services.totalenergies.fr"}


        response = requests.get(url, headers=headers)
        self.station = response.json()
        self.items = []
        for item in self.station['Pois'][0]['Items']:
            if item['Code'] == 'excellium98' or item['Code'] == 'excelliumdiesel' or item['Code'] == 'gasoil' or \
                    item['Code'] == 'SP95E10':
                if item['Availability']:
                    self.items.append(f"{item['Code']}:true")
                if item['Availability'] == False:
                    self.items.append(f"{item['Code']}:false")

    def get_available_fuel(self):
        return self.items

    def get_location(self):
        lat = self.station['Pois'][0]['Latitude']
        lon = self.station['Pois'][0]['Longitude']
        return [lon, lat]

    def compare_before(self, obj):
        current_fuel = self.get_available_fuel()
        old_fuel = obj.get_available_fuel()
        compare = set(old_fuel) - set(current_fuel)
        msg = ""
        if len(compare):
            name = self.station['Pois'][0]['Name']
            address = f"{self.station['Pois'][0]['AddressPart1']} {self.station['Pois'][0]['City']}"

            msg += f"*{name}* \n" \
                   f"_{address}_\n"
            for item in compare:
                fuel_status = item.split(':')

                if fuel_status[1] == "true":
                    fuelname = self.FUEL_NAME[fuel_status[0]]
                    msg += f"❌ {fuelname}\n"

                if fuel_status[1] == "false":
                    fuelname = self.FUEL_NAME[fuel_status[0]]
                    msg += f"✅ {fuelname}\n"
        return msg
