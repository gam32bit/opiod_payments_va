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

def get_data_frame(data):
    county_names = [row[1] for row in data[0][13:] if row[1] != None and row[1] != "TOTALS"]
    columns = ["County", "Coordinates", "Distributors_2021", "Distributors_2022", "Distributors_2023", "Janssen_2022", "Janssen_2023", "Total_Payment"]
    county_dict = {county : [] for county in county_names}
    for table in data:
        for row in table:
            if row[1] == "Subdivision":
                break
            if row[1] in county_names:
                county_dict[row[1]].append(row[-1])
    county_df = pd.DataFrame(county_dict, columns=columns)
    county_df.set_index("County", inplace=True)
    return county_df
    
print(get_data_frame(all_data))

