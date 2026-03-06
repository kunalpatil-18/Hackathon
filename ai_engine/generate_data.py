import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_historical_data(days=7):
    data = []
    start_date = datetime.now() - timedelta(days=days)
    
    # 5-minute intervals for 'days' number of days
    intervals = days * 24 * 12 
    
    for i in range(intervals):
        current_time = start_date + timedelta(minutes=i*5)
        hour = current_time.hour
        
        # Simulate Traffic: Peak at 8-9 AM and 5-6 PM
        base_traffic = 0.2
        if 7 <= hour <= 9 or 16 <= hour <= 19:
            base_traffic = 0.7 + np.random.normal(0, 0.1)
        else:
            base_traffic = 0.3 + np.random.normal(0, 0.1)
            
        traffic_density = np.clip(base_traffic, 0, 1)
        
        # Simulate AQI: Higher traffic usually means worse AQI (higher value)
        aqi = np.clip(traffic_density * 5 + np.random.randint(-1, 2), 1, 5)
        
        data.append({
            "timestamp": current_time,
            "traffic_density": traffic_density,
            "aqi": int(aqi)
        })
        
    df = pd.DataFrame(data)
    df.to_csv('historical_traffic.csv', index=False)
    print("Historical dataset generated: historical_traffic.csv")

if __name__ == "__main__":
    generate_historical_data(14) # Generate 2 weeks of data