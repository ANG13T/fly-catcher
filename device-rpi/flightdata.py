from urllib.request import urlopen
import json
from time import sleep

DUMP1090DATAURL = "http://localhost:8080/data/aircraft.json"

class FlightData():
    def __init__(self, data_url = DUMP1090DATAURL, flight_log_number = 0):

        self.data_url = data_url

        self.refresh()

    def refresh(self):
        #open the data url
        print("http://localhost:8080/data/aircraft.json")

        self.req = urlopen("http://localhost:8080/data/aircraft.json")
      
        #read data from the url
        self.raw_data = self.req.read()
        print(self.raw_data)

        #encode the data
        encoding = self.req.headers.get_content_charset()

        #load in the json
        self.json_data = json.loads(self.raw_data.decode('utf-8'))

        self.aircraft = AirCraftData.parse_flightdata_json(self.json_data)

    def _refresh(self):

        data_file = open("data/aircraft.json")
        
        #load in the json
        self.json_data = json.load(data_file)

        self.aircraft = AirCraftData.parse_flightdata_json(self.json_data)

class AirCraftData():
    def __init__(self,
                 dhex,
                 squawk,
                 flight,
                 lat,
                 lon,
                 seen_pos,
                 altitude,
                 vert_rate,
                 track,
                 rssi,
                 speed,
                 messages,
                 seen,
                 mlat):
        
        self.hex = dhex
        self.squawk = squawk
        self.flight = flight
        self.lat = lat
        self.lon = lon
        self.seen_pos = seen_pos
        self.altitude = altitude
        self.vert_rate = vert_rate
        self.track = track
        self.rssi = rssi
        self.speed = speed
        self.messages = messages
        self.seen = seen
        self.mlat = mlat

    @staticmethod
    def parse_flightdata_json(json_data):
        aircraft_list = []
        for aircraft in json_data['aircraft']:
            print("hii ")
            print(json_data['aircraft'])
            aircraftdata = AirCraftData(
                aircraft.get("hex", None),
                aircraft.get("squawk", None),
                aircraft.get("flight", None),
                aircraft.get("lat", None),
                aircraft.get("lon", None),
                aircraft.get("seen_pos", None),
                aircraft.get("altitude", None),
                aircraft.get("vert_rate",None),
                aircraft.get("track", None),
                aircraft.get("rssi", None),
                aircraft.get("speed", None),
                aircraft.get("messages", None),
                aircraft.get("seen", None),
                aircraft.get("mlat", None))
            aircraft_list.append(aircraftdata)
            print(aircraftdata.hex)
            print("data ^")
        return aircraft_list

    def __hash__(self):
        return hash(self.hex)

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return (self.hex == other.hex)
            
#test    
if __name__ == "__main__":
    
    #create FlightData object
    myflights = FlightData()
    while True:
        #loop through each aircraft found
        for aircraft in myflights.aircraft:
            
            #print the aircraft's data
            print(aircraft.hex)
            print(aircraft.squawk)
            print(aircraft.flight)
            print(aircraft.lat)
            print(aircraft.lon)
            print(aircraft.validposition)
            print(aircraft.altitude)
            print(aircraft.vert_rate)
            print(aircraft.track)
            print(aircraft.validtrack)
            print(aircraft.speed)
            print(aircraft.messages)
            print(aircraft.seen)
            print(aircraft.mlat)

        sleep(1)

        #refresh the flight data
        myflights.refresh()

