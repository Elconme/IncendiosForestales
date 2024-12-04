import requests

def get_user_location():
  try:
    response = requests.get('http://ipinfo.io/json')
    response.raise_for_status()
    data = response.json()
    city = data['city']
    loc = data['loc']
    return city, loc
  except requests.exceptions.RequestException as e:
    print(f"Error fetching location: {e}")
    return None, None

def get_weather_data(api_key):
  city, loc = get_user_location()
  url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=es"
  response = requests.get(url)
  data = response.json()

  if response.status_code == 200:
    current = data['current']
    temperature = current['temp_c']
    humidity = current['humidity']
    wind_veloc = current['wind_kph']
    return temperature, humidity, wind_veloc, loc, city
  else:
    return None, None, None, None, None
  
if __name__ == "__main__":
  get_user_location()