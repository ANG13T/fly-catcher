import math

class GPSUtils():

    MPS_TO_MPH = 2.2369362920544

    @staticmethod
    def lat_lon_to_x_y(lat, lon):
    
        rMajor = 6378137 # Equatorial Radius, WGS84
        shift = math.pi * rMajor
        x = lon * shift / 180
        y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
        y = y * shift / 180
        
        return x,y
