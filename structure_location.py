import pandas as pd
import us
import re
from geopy.geocoders import Nominatim
import time

def is_valid_location(location):
    # Check if the location contains only valid characters (letters, commas, spaces)
    return bool(re.match(r'^[a-zA-Z .,-]+$', location))

def get_city_state_from_geopy(name):
    geolocator = Nominatim(user_agent="geoapi")
    try:
        location = geolocator.geocode(name + ", USA", timeout=10)
        if location and "USA" in location.address:
            address_parts = location.raw.get("display_name", "").split(",")
            if len(address_parts) > 1:
                state = address_parts[-2].strip()
                return name, us.states.lookup(state).abbr if us.states.lookup(state) else ""
    except:
        return name, ""
    return name, ""

def parse_location(location):
    location = str(location).strip()
    
    # If the location contains invalid characters or symbols, return null values
    if not is_valid_location(location) or location in ["United States", "USA"]:
        return "", ""
    
    city, state = "", ""
    
    # Handling cases with '|'
    if '|' in location:
        location = location.split('|')[0].strip()
    
    # Split by commas and remove 'USA' if present
    parts = [p.strip() for p in location.split(',') if p.strip() != "USA"]
    
    if len(parts) == 1:
        if us.states.lookup(parts[0]):
            state = us.states.lookup(parts[0]).abbr
        else:
            city, state = get_city_state_from_geopy(parts[0])
    elif len(parts) == 2:
        if us.states.lookup(parts[1]):
            city, state = parts[0], us.states.lookup(parts[1]).abbr
        elif us.states.lookup(parts[0]):
            city, state = parts[1], us.states.lookup(parts[0]).abbr
        else:
            city, state = get_city_state_from_geopy(parts[0])
    elif len(parts) == 3:
        city, state = parts[0], us.states.lookup(parts[1]).abbr if us.states.lookup(parts[1]) else ""
    
    return city, state

def process_excel(file_path, output_path):
    df = pd.read_excel(file_path)
    
    city_list, state_list = [], []
    
    for loc in df['location']:
        city, state = parse_location(loc)
        city_list.append(city)
        state_list.append(state)
    
    df['city'] = city_list
    df['state'] = state_list
    
    df.to_excel(output_path, index=False)
    print("Updated file saved at:", output_path)

# Usage
input_file = "locations.xlsx"  # Change this to your actual file path
output_file = "updated_locations.xlsx"
process_excel(input_file, output_file)