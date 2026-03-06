import requests
import pandas as pd


class CityDataCollector:

    def __init__(self, google_key, aqi_key):
        self.google_key = google_key
        self.aqi_key = aqi_key

    def get_aqi(self, lat=28.6139, lon=77.2090):
        """Fetch AQI from OpenWeather API"""

        try:
            url = (
                f"http://api.openweathermap.org/data/2.5/air_pollution"
                f"?lat={lat}&lon={lon}&appid={self.aqi_key}"
            )

            response = requests.get(url, timeout=5)

            if response.status_code != 200:
                print("AQI API FAILED:", response.text)
                return 3  # fallback AQI

            data = response.json()

            print("AQI API RESPONSE:", data)

            if "list" not in data or len(data["list"]) == 0:
                print("AQI data missing, using fallback")
                return 3

            return data["list"][0]["main"]["aqi"]

        except Exception as e:
            print("AQI ERROR:", e)
            return 3  # fallback AQI

    def collect_snapshot(self):
        """Collect simulated city traffic snapshot"""

        try:

            aqi = self.get_aqi()

            # Simulated traffic data (can be replaced with real APIs later)
            data = [
                {
                    "location": "Junction A",
                    "traffic_density": 45,
                    "aqi": aqi
                },
                {
                    "location": "Junction B",
                    "traffic_density": 60,
                    "aqi": aqi
                },
                {
                    "location": "Junction C",
                    "traffic_density": 30,
                    "aqi": aqi
                },
                {
                    "location": "Junction D",
                    "traffic_density": 75,
                    "aqi": aqi
                }
            ]

            df = pd.DataFrame(data)

            return df

        except Exception as e:
            print("COLLECT SNAPSHOT ERROR:", e)

            return pd.DataFrame([])