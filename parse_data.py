import pdfplumber
import pandas as pd
from geopy.geocoders import nominatim

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
    geolocator = nominatim(user_agent="county_coordinates")
    location = geolocator.geocode(county + " County, Virginia, USA")
    if location:
        return location.latitude, location.longitude
    else:
        return "N/A", "N/A"

def get_data_frame(data):
    county_data = []
    county_names = [x[1] for x in data[0][13:]]
    return county_names

columns = ["County", "Coordinates", "Distributors_2021", "Distributors_2022", "Distributors_2023", "Janssen_Year_2022", "Janssen_Year_2023", "Total_Payment"]
    
print(get_data_frame(all_data))

