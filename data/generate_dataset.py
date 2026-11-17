"""
ESTATEIQ - Indian Real Estate Dataset Generator
Generates realistic, statistically consistent Indian property transaction records
across major metropolitan and emerging tier-1/tier-2 hubs in India.
"""

import os
import random
import numpy as np
import pandas as pd

# Set fixed seed for reproducibility
np.random.seed(42)
random.seed(42)

# Locality definitions with real geographic coordinates, base price per sqft (INR), and administrative details
LOCALITY_DATA = [
    # Mumbai, Maharashtra
    {"city": "Mumbai", "district": "Mumbai Suburban", "state": "Maharashtra", "area_name": "Bandra West", "pincode": 400050, "lat": 19.0596, "lon": 72.8295, "base_rate": 42000, "tier": "Super-Luxury"},
    {"city": "Mumbai", "district": "Mumbai Suburban", "state": "Maharashtra", "area_name": "Andheri East", "pincode": 400069, "lat": 19.1136, "lon": 72.8697, "base_rate": 21000, "tier": "Mid-Premium"},
    {"city": "Mumbai", "district": "Mumbai Suburban", "state": "Maharashtra", "area_name": "Powai", "pincode": 400076, "lat": 19.1176, "lon": 72.9060, "base_rate": 23500, "tier": "Premium"},
    {"city": "Mumbai", "district": "Mumbai City", "state": "Maharashtra", "area_name": "Worli", "pincode": 400018, "lat": 19.0178, "lon": 72.8178, "base_rate": 48000, "tier": "Super-Luxury"},
    {"city": "Mumbai", "district": "Mumbai Suburban", "state": "Maharashtra", "area_name": "Borivali West", "pincode": 400092, "lat": 19.2307, "lon": 72.8567, "base_rate": 18500, "tier": "Mid"},
    {"city": "Mumbai", "district": "Thane", "state": "Maharashtra", "area_name": "Thane West", "pincode": 400601, "lat": 19.2183, "lon": 72.9781, "base_rate": 12500, "tier": "Affordable-Mid"},
    {"city": "Mumbai", "district": "Thane", "state": "Maharashtra", "area_name": "Vashi (Navi Mumbai)", "pincode": 400703, "lat": 19.0771, "lon": 72.9986, "base_rate": 14000, "tier": "Mid"},

    # Delhi NCR, Delhi
    {"city": "Delhi", "district": "South West Delhi", "state": "Delhi", "area_name": "Vasant Kunj", "pincode": 110070, "lat": 28.5244, "lon": 77.1558, "base_rate": 22000, "tier": "Premium"},
    {"city": "Delhi", "district": "South West Delhi", "state": "Delhi", "area_name": "Dwarka Sector 10", "pincode": 110075, "lat": 28.5823, "lon": 77.0500, "base_rate": 11500, "tier": "Mid"},
    {"city": "Delhi", "district": "North West Delhi", "state": "Delhi", "area_name": "Rohini Sector 13", "pincode": 110085, "lat": 28.7166, "lon": 77.1245, "base_rate": 10500, "tier": "Mid"},
    {"city": "Delhi", "district": "South Delhi", "state": "Delhi", "area_name": "Greater Kailash I", "pincode": 110048, "lat": 28.5482, "lon": 77.2372, "base_rate": 28000, "tier": "Super-Luxury"},
    {"city": "Delhi", "district": "East Delhi", "state": "Delhi", "area_name": "Mayur Vihar Phase 1", "pincode": 110091, "lat": 28.6083, "lon": 77.2974, "base_rate": 12000, "tier": "Mid"},

    # Bengaluru, Karnataka
    {"city": "Bengaluru", "district": "Bengaluru Urban", "state": "Karnataka", "area_name": "Whitefield", "pincode": 560066, "lat": 12.9698, "lon": 77.7499, "base_rate": 9200, "tier": "IT-Hub"},
    {"city": "Bengaluru", "district": "Bengaluru Urban", "state": "Karnataka", "area_name": "Koramangala", "pincode": 560034, "lat": 12.9352, "lon": 77.6245, "base_rate": 16500, "tier": "Premium"},
    {"city": "Bengaluru", "district": "Bengaluru Urban", "state": "Karnataka", "area_name": "Indiranagar", "pincode": 560038, "lat": 12.9784, "lon": 77.6408, "base_rate": 17800, "tier": "Super-Luxury"},
    {"city": "Bengaluru", "district": "Bengaluru Urban", "state": "Karnataka", "area_name": "HSR Layout", "pincode": 560102, "lat": 12.9121, "lon": 77.6446, "base_rate": 11800, "tier": "Mid-Premium"},
    {"city": "Bengaluru", "district": "Bengaluru Urban", "state": "Karnataka", "area_name": "Electronic City Phase 1", "pincode": 560100, "lat": 12.8452, "lon": 77.6602, "base_rate": 6500, "tier": "Affordable-Mid"},
    {"city": "Bengaluru", "district": "Bengaluru Urban", "state": "Karnataka", "area_name": "Hebbal", "pincode": 560024, "lat": 13.0358, "lon": 77.5970, "base_rate": 11000, "tier": "Mid-Premium"},
    {"city": "Bengaluru", "district": "Bengaluru Urban", "state": "Karnataka", "area_name": "Bellandur", "pincode": 560103, "lat": 12.9260, "lon": 77.6762, "base_rate": 9800, "tier": "IT-Hub"},

    # Hyderabad, Telangana
    {"city": "Hyderabad", "district": "Rangareddy", "state": "Telangana", "area_name": "Gachibowli", "pincode": 500032, "lat": 17.4401, "lon": 78.3489, "base_rate": 9500, "tier": "IT-Hub"},
    {"city": "Hyderabad", "district": "Rangareddy", "state": "Telangana", "area_name": "HITEC City", "pincode": 500081, "lat": 17.4435, "lon": 78.3772, "base_rate": 10500, "tier": "IT-Hub"},
    {"city": "Hyderabad", "district": "Hyderabad", "state": "Telangana", "area_name": "Jubilee Hills", "pincode": 500033, "lat": 17.4319, "lon": 78.4073, "base_rate": 17500, "tier": "Super-Luxury"},
    {"city": "Hyderabad", "district": "Hyderabad", "state": "Telangana", "area_name": "Banjara Hills", "pincode": 500034, "lat": 17.4156, "lon": 78.4350, "base_rate": 16800, "tier": "Super-Luxury"},
    {"city": "Hyderabad", "district": "Rangareddy", "state": "Telangana", "area_name": "Kondapur", "pincode": 500084, "lat": 17.4699, "lon": 78.3578, "base_rate": 8600, "tier": "Mid-Premium"},
    {"city": "Hyderabad", "district": "Medchal", "state": "Telangana", "area_name": "Kukatpally", "pincode": 500072, "lat": 17.4948, "lon": 78.3996, "base_rate": 7200, "tier": "Mid"},

    # Chennai, Tamil Nadu
    {"city": "Chennai", "district": "Chennai", "state": "Tamil Nadu", "area_name": "OMR - Thoraipakkam", "pincode": 600097, "lat": 12.9348, "lon": 80.2312, "base_rate": 7800, "tier": "IT-Hub"},
    {"city": "Chennai", "district": "Chennai", "state": "Tamil Nadu", "area_name": "Velachery", "pincode": 600042, "lat": 12.9815, "lon": 80.2180, "base_rate": 8900, "tier": "Mid-Premium"},
    {"city": "Chennai", "district": "Chennai", "state": "Tamil Nadu", "area_name": "Anna Nagar West", "pincode": 600040, "lat": 13.0850, "lon": 80.2101, "base_rate": 13800, "tier": "Premium"},
    {"city": "Chennai", "district": "Chennai", "state": "Tamil Nadu", "area_name": "Adyar", "pincode": 600020, "lat": 13.0012, "lon": 80.2565, "base_rate": 16200, "tier": "Super-Luxury"},
    {"city": "Chennai", "district": "Chennai", "state": "Tamil Nadu", "area_name": "Sholinganallur", "pincode": 600119, "lat": 12.9010, "lon": 80.2279, "base_rate": 6800, "tier": "Affordable-Mid"},
    {"city": "Chennai", "district": "Chennai", "state": "Tamil Nadu", "area_name": "Porur", "pincode": 600116, "lat": 13.0382, "lon": 80.1565, "base_rate": 6500, "tier": "Affordable-Mid"},

    # Pune, Maharashtra
    {"city": "Pune", "district": "Pune", "state": "Maharashtra", "area_name": "Hinjewadi Phase 1", "pincode": 411057, "lat": 18.5913, "lon": 73.7389, "base_rate": 7400, "tier": "IT-Hub"},
    {"city": "Pune", "district": "Pune", "state": "Maharashtra", "area_name": "Wakad", "pincode": 411057, "lat": 18.5987, "lon": 73.7663, "base_rate": 8100, "tier": "Mid"},
    {"city": "Pune", "district": "Pune", "state": "Maharashtra", "area_name": "Baner", "pincode": 411045, "lat": 18.5590, "lon": 73.7868, "base_rate": 9600, "tier": "Mid-Premium"},
    {"city": "Pune", "district": "Pune", "state": "Maharashtra", "area_name": "Kothrud", "pincode": 411038, "lat": 18.5074, "lon": 73.8077, "base_rate": 11800, "tier": "Premium"},
    {"city": "Pune", "district": "Pune", "state": "Maharashtra", "area_name": "Kharadi", "pincode": 411014, "lat": 18.5516, "lon": 73.9349, "base_rate": 8800, "tier": "IT-Hub"},
    {"city": "Pune", "district": "Pune", "state": "Maharashtra", "area_name": "Viman Nagar", "pincode": 411014, "lat": 18.5679, "lon": 73.9143, "base_rate": 10500, "tier": "Mid-Premium"},

    # Kolkata, West Bengal
    {"city": "Kolkata", "district": "North 24 Parganas", "state": "West Bengal", "area_name": "New Town Action Area 1", "pincode": 700156, "lat": 22.5850, "lon": 88.4633, "base_rate": 6200, "tier": "IT-Hub"},
    {"city": "Kolkata", "district": "North 24 Parganas", "state": "West Bengal", "area_name": "Salt Lake Sector 5", "pincode": 700091, "lat": 22.5804, "lon": 88.4378, "base_rate": 7800, "tier": "Mid-Premium"},
    {"city": "Kolkata", "district": "Kolkata", "state": "West Bengal", "area_name": "Ballygunge", "pincode": 700019, "lat": 22.5280, "lon": 88.3653, "base_rate": 13500, "tier": "Super-Luxury"},
    {"city": "Kolkata", "district": "Kolkata", "state": "West Bengal", "area_name": "Alipore", "pincode": 700027, "lat": 22.5310, "lon": 88.3289, "base_rate": 15500, "tier": "Super-Luxury"},
    {"city": "Kolkata", "district": "South 24 Parganas", "state": "West Bengal", "area_name": "Garia", "pincode": 700084, "lat": 22.4645, "lon": 88.3832, "base_rate": 4800, "tier": "Affordable-Mid"},

    # Ahmedabad, Gujarat
    {"city": "Ahmedabad", "district": "Ahmedabad", "state": "Gujarat", "area_name": "SG Highway", "pincode": 380054, "lat": 23.0489, "lon": 72.5050, "base_rate": 6500, "tier": "Mid-Premium"},
    {"city": "Ahmedabad", "district": "Ahmedabad", "state": "Gujarat", "area_name": "Bopal", "pincode": 380058, "lat": 23.0337, "lon": 72.4634, "base_rate": 5200, "tier": "Affordable-Mid"},
    {"city": "Ahmedabad", "district": "Ahmedabad", "state": "Gujarat", "area_name": "Bodakdev", "pincode": 380054, "lat": 23.0373, "lon": 72.5119, "base_rate": 8400, "tier": "Premium"},
    {"city": "Ahmedabad", "district": "Ahmedabad", "state": "Gujarat", "area_name": "Prahlad Nagar", "pincode": 380015, "lat": 23.0118, "lon": 72.5110, "base_rate": 7800, "tier": "Mid-Premium"},

    # Gurgaon, Haryana
    {"city": "Gurgaon", "district": "Gurugram", "state": "Haryana", "area_name": "Golf Course Road", "pincode": 122002, "lat": 28.4601, "lon": 77.0999, "base_rate": 24500, "tier": "Super-Luxury"},
    {"city": "Gurgaon", "district": "Gurugram", "state": "Haryana", "area_name": "DLF Phase 5", "pincode": 122009, "lat": 28.4554, "lon": 77.0945, "base_rate": 21000, "tier": "Premium"},
    {"city": "Gurgaon", "district": "Gurugram", "state": "Haryana", "area_name": "Sohna Road Sector 48", "pincode": 122018, "lat": 28.4239, "lon": 77.0428, "base_rate": 10200, "tier": "Mid"},
    {"city": "Gurgaon", "district": "Gurugram", "state": "Haryana", "area_name": "Sector 57", "pincode": 122003, "lat": 28.4290, "lon": 77.0780, "base_rate": 11500, "tier": "Mid-Premium"},

    # Noida, Uttar Pradesh
    {"city": "Noida", "district": "Gautam Buddha Nagar", "state": "Uttar Pradesh", "area_name": "Sector 62", "pincode": 201309, "lat": 28.6280, "lon": 77.3649, "base_rate": 8200, "tier": "IT-Hub"},
    {"city": "Noida", "district": "Gautam Buddha Nagar", "state": "Uttar Pradesh", "area_name": "Sector 137 (Expressway)", "pincode": 201305, "lat": 28.5133, "lon": 77.4042, "base_rate": 8900, "tier": "Mid-Premium"},
    {"city": "Noida", "district": "Gautam Buddha Nagar", "state": "Uttar Pradesh", "area_name": "Sector 150", "pincode": 201310, "lat": 28.4485, "lon": 77.4789, "base_rate": 9800, "tier": "Mid-Premium"},
    {"city": "Noida", "district": "Gautam Buddha Nagar", "state": "Uttar Pradesh", "area_name": "Noida Extension (Greater Noida W)", "pincode": 201306, "lat": 28.6012, "lon": 77.4475, "base_rate": 5600, "tier": "Affordable-Mid"},

    # Jaipur, Rajasthan
    {"city": "Jaipur", "district": "Jaipur", "state": "Rajasthan", "area_name": "Vaishali Nagar", "pincode": 302021, "lat": 26.9075, "lon": 75.7423, "base_rate": 6200, "tier": "Mid-Premium"},
    {"city": "Jaipur", "district": "Jaipur", "state": "Rajasthan", "area_name": "Malviya Nagar", "pincode": 302017, "lat": 26.8532, "lon": 75.8197, "base_rate": 6800, "tier": "Mid-Premium"},
    {"city": "Jaipur", "district": "Jaipur", "state": "Rajasthan", "area_name": "Mansarovar", "pincode": 302020, "lat": 26.8624, "lon": 75.7634, "base_rate": 5100, "tier": "Affordable-Mid"},
    {"city": "Jaipur", "district": "Jaipur", "state": "Rajasthan", "area_name": "C-Scheme", "pincode": 302001, "lat": 26.9110, "lon": 75.8015, "base_rate": 10500, "tier": "Super-Luxury"},

    # Kochi, Kerala
    {"city": "Kochi", "district": "Ernakulam", "state": "Kerala", "area_name": "Kakkanad (Infopark)", "pincode": 682030, "lat": 10.0159, "lon": 76.3419, "base_rate": 5800, "tier": "IT-Hub"},
    {"city": "Kochi", "district": "Ernakulam", "state": "Kerala", "area_name": "Marine Drive", "pincode": 682031, "lat": 9.9839, "lon": 76.2753, "base_rate": 11200, "tier": "Super-Luxury"},
    {"city": "Kochi", "district": "Ernakulam", "state": "Kerala", "area_name": "Edappally", "pincode": 682024, "lat": 10.0247, "lon": 76.3082, "base_rate": 6400, "tier": "Mid-Premium"}
]

PROPERTY_TYPES = [
    ("Apartment", 0.60, 1.0),
    ("Independent House", 0.15, 1.18),
    ("Villa", 0.10, 1.35),
    ("Penthouse", 0.05, 1.45),
    ("Builder Floor", 0.10, 1.08)
]

FURNISHING_STATUS = [
    ("Unfurnished", 0.35, 1.0),
    ("Semi-Furnished", 0.45, 1.07),
    ("Fully Furnished", 0.20, 1.18)
]

FACING_DIRECTIONS = ["East", "North", "North-East", "West", "North-West", "South"]

ALL_AMENITIES_LIST = [
    "Gym", "Swimming Pool", "Clubhouse", "24x7 Security", "Power Backup",
    "Lift", "Children Play Area", "Jogging Track", "Intercom", "CCTV",
    "Rainwater Harvesting", "Landscaped Garden", "Covered Parking", "Fire Safety"
]

def generate_property_records(num_records=3200):
    records = []
    
    for i in range(1, num_records + 1):
        prop_id = f"EQ-{10000 + i}"
        loc = random.choice(LOCALITY_DATA)
        
        # Determine BHK distribution
        bhk_roll = random.random()
        if bhk_roll < 0.22:
            bedrooms = 1
            area_sqft = int(np.random.normal(560, 80))
            area_sqft = max(380, min(800, area_sqft))
            bathrooms = 1
            balcony = random.choice([0, 1])
        elif bhk_roll < 0.62:
            bedrooms = 2
            area_sqft = int(np.random.normal(1050, 140))
            area_sqft = max(750, min(1400, area_sqft))
            bathrooms = random.choice([2, 2, 2, 1])
            balcony = random.choice([1, 1, 2])
        elif bhk_roll < 0.88:
            bedrooms = 3
            area_sqft = int(np.random.normal(1650, 220))
            area_sqft = max(1300, min(2400, area_sqft))
            bathrooms = random.choice([2, 3, 3, 3])
            balcony = random.choice([1, 2, 2, 3])
        elif bhk_roll < 0.97:
            bedrooms = 4
            area_sqft = int(np.random.normal(2550, 350))
            area_sqft = max(2100, min(3600, area_sqft))
            bathrooms = random.choice([3, 4, 4])
            balcony = random.choice([2, 3, 4])
        else:
            bedrooms = 5
            area_sqft = int(np.random.normal(3800, 500))
            area_sqft = max(3200, min(5800, area_sqft))
            bathrooms = random.choice([4, 5, 5])
            balcony = random.choice([3, 4, 5])

        # Property type
        pt_choice = random.choices([p[0] for p in PROPERTY_TYPES], weights=[p[1] for p in PROPERTY_TYPES])[0]
        pt_mult = [p[2] for p in PROPERTY_TYPES if p[0] == pt_choice][0]

        # Villas and Independent houses have larger sqft and fewer floors
        if pt_choice in ["Villa", "Independent House"]:
            area_sqft = int(area_sqft * 1.25)
            total_floors = random.choice([1, 2, 3])
            floor_number = random.choice([0, 1])
        else:
            total_floors = random.choice([4, 7, 12, 14, 18, 22, 28, 35])
            floor_number = random.randint(1, total_floors)

        # Property age (in years)
        age_roll = random.random()
        if age_roll < 0.30:
            property_age = random.randint(0, 1) # Brand New / Under Construction
            age_factor = 1.08
        elif age_roll < 0.65:
            property_age = random.randint(2, 5) # 2-5 yrs
            age_factor = 1.00
        elif age_roll < 0.88:
            property_age = random.randint(6, 12)
            age_factor = 0.91
        else:
            property_age = random.randint(13, 24)
            age_factor = 0.82

        # Furnishing
        furn_choice = random.choices([f[0] for f in FURNISHING_STATUS], weights=[f[1] for f in FURNISHING_STATUS])[0]
        furn_mult = [f[2] for f in FURNISHING_STATUS if f[0] == furn_choice][0]

        # Parking
        if bedrooms >= 3 or pt_choice in ["Villa", "Penthouse"]:
            parking = random.choice([1, 2, 2, 3])
        elif bedrooms == 2:
            parking = random.choice([1, 1, 2])
        else:
            parking = random.choice([0, 1])

        # Facing
        facing = random.choice(FACING_DIRECTIONS)
        facing_mult = 1.03 if facing in ["East", "North-East", "North"] else 0.99

        # Amenities
        num_amenities = random.randint(4, 11)
        amenities_selected = random.sample(ALL_AMENITIES_LIST, num_amenities)
        amenities_str = ";".join(amenities_selected)
        amenities_bonus = 1.0 + (len(amenities_selected) * 0.012)

        # Floor factor (Higher floors in highrises command slight premium in Indian metros)
        if total_floors > 8:
            floor_premium = 1.0 + (floor_number / total_floors) * 0.06
        else:
            floor_premium = 1.0

        # Small micro-variance (+/- 5%) for realistic organic dispersion
        random_noise = np.random.normal(1.0, 0.045)

        # Final calculated Price per sqft & Total Property Price
        calculated_rate = loc["base_rate"] * pt_mult * age_factor * furn_mult * facing_mult * amenities_bonus * floor_premium * random_noise
        price_inr = int(round(calculated_rate * area_sqft, -4)) # Round to nearest 10,000 INR

        # Jitter latitude/longitude slightly (+/- 0.008 deg ~ 800m) to represent realistic addresses inside the locality
        lat_jitter = loc["lat"] + np.random.uniform(-0.007, 0.007)
        lon_jitter = loc["lon"] + np.random.uniform(-0.007, 0.007)

        record = {
            "property_id": prop_id,
            "area_sqft": area_sqft,
            "area_name": loc["area_name"],
            "city": loc["city"],
            "district": loc["district"],
            "state": loc["state"],
            "pincode": loc["pincode"],
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "balcony": balcony,
            "property_type": pt_choice,
            "property_age": property_age,
            "furnishing": furn_choice,
            "parking": parking,
            "floor_number": floor_number,
            "total_floors": total_floors,
            "facing": facing,
            "amenities": amenities_str,
            "latitude": round(lat_jitter, 6),
            "longitude": round(lon_jitter, 6),
            "price": price_inr
        }
        records.append(record)

    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = generate_property_records(3200)
    out_path = os.path.join(os.path.dirname(__file__), "indian_housing_dataset.csv")
    df.to_csv(out_path, index=False)
    print(f"Dataset generated successfully with {len(df)} records at {out_path}")
    print("Sample records preview:")
    print(df.head(3)[["property_id", "area_name", "city", "state", "bedrooms", "area_sqft", "price"]])
    print("\nSummary Statistics:")
    print(df[["area_sqft", "bedrooms", "bathrooms", "price"]].describe())
