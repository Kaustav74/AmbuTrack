import gpsd
import tkinter as tk
import requests

def ambulance_app():
    """
    This function creates an emergency ambulance app which tracks and detects ambulances.
    The app uses gpsd-py3, tkinter and requests libraries.
    The app displays a map showing all the ambulances nearby the user's location.
    """
    try:
        # Connect to gpsd
        gpsd.connect()
        
        # Get user's location
        packet = gpsd.get_current()
        user_lat = packet.position()[0]
        user_lon = packet.position()[1]
        
        # Send request to ambulance tracking API
        response = requests.get(f"https://ambulance-tracking-api.com?lat={user_lat}&lon={user_lon}")
        
        # Get ambulance data from response
        ambulance_data = response.json()
        
        # Create tkinter window
        window = tk.Tk()
        window.title("Emergency Ambulance App")
        
        # Create list of ambulance labels
        ambulance_labels = []
        for i, ambulance in enumerate(ambulance_data):
            ambulance_lat = ambulance["latitude"]
            ambulance_lon = ambulance["longitude"]
            distance = distance_between(user_lat, user_lon, ambulance_lat, ambulance_lon)
            label_text = f"Ambulance {i+1}: {distance:.2f} km away"
            label = tk.Label(window, text=label_text)
            label.pack()
            ambulance_labels.append(label)
        
        # Continuously update ambulance distances
        while True:
            # Get updated user location
            packet = gpsd.get_current()
            user_lat = packet.position()[0]
            user_lon = packet.position()[1]
            
            # Update ambulance distances
            for i, ambulance in enumerate(ambulance_data):
                ambulance_lat = ambulance["latitude"]
                ambulance_lon = ambulance["longitude"]
                distance = distance_between(user_lat, user_lon, ambulance_lat, ambulance_lon)
                ambulance_labels[i]["text"] = f"Ambulance {i+1}: {distance:.2f} km away"
            
            # Update window
            window.update()
        
    except Exception as e:
        # Log the error
        print(f"Error: {e}")

def distance_between(lat1, lon1, lat2, lon2):
    """
    This function calculates the distance between two GPS coordinates in kilometers.
    """
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance
