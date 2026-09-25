import time
import pandas as pd
from geopy.geocoders import Nominatim



def get_geographic_coordinates(coordinates):
    geolocator = Nominatim(user_agent="vanthora_admin_app_v1")

    try:
        time.sleep(1) 
        
        if not coordinates or pd.isna(coordinates):
            return None, None

        location = geolocator.geocode(coordinates)
        
        if location:
            return location.latitude, location.longitude
            
    except Exception as e:
        print(f"Error al geocodificar {coordinates}: {e}")
        pass
        
    return None, None 