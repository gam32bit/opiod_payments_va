import pdfplumber
import pandas as pd
from geopy.geocoders import Nominatim

pdf_paths = [
    "files/va-payment-allocations-distributors-year-1.pdf",
    "files/va-payment-allocations-distributors-year-2.pdf",
    "files/va-payment-allocations-distributors-year-3.pdf",
    "files/va-payment-allocations-janssen-payments-1-and-2-plus-accelerated-3-through-5.pdf",
    "files/va-payment-allocations-janssen-payment-year-2-payment-3.pdf",
]

#Extract Data from PDFs

def extract_data(pdf_path):
    pdf = pdfplumber.open(pdf_path)
    data = []
    for page in pdf.pages:
        table = page.extract_table()
        for row in table:
            data.append(row)
    return data

all_data = [extract_data(pdf_path) for pdf_path in pdf_paths]

def get_coordinates(county):
    geolocator = Nominatim(user_agent="county_coordinates")
    location = geolocator.geocode(county + ", Virginia, USA")
    if location:
        return location.latitude, location.longitude
    else:
        return "N/A", "N/A"
    
def get_payment_by_county(county_name, table):
    df = pd.DataFrame(table)
    payment = df.loc[df[1] == county_name].index[0]][-1]
    return payment

def get_data_frame(data):
    county_names = [x[1] for x in data[0][13:] if x[1] != None and x[1] != "TOTALS"]
    county_data = []
    columns = ["County", "Coordinates", "Distributors_2021", "Distributors_2022", "Distributors_2023", "Janssen_Year_2022", "Janssen_Year_2023", "Total_Payment"]
    for county in county_names:
        county_data.append([county, get_coordinates(county), get_payment_by_county(county, table)] for table in data)
    return pd.DataFrame(county_data, columns=columns)
    
print(get_data_frame(all_data))

