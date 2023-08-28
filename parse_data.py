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
        data.append(page.extract_table())
    return data

all_data = [extract_data(pdf_path) for pdf_path in pdf_paths]



def get_data_frame(data):
    columns = ["County", "Coordinates", "Distributors_2021", "Distributors_2022", "Distributors_2023", "Janssen_2022", "Janssen_2023", "Total_Payment"]
    df = pd.DataFrame(columns=columns)
    df.set_index("County", inplace=True)
    counter = 0
    for table in data:
        full_table = table[0] + table[1]
        header_index = next(idx for idx, row in enumerate(full_table) if row[1] == "Subdivision")
        data_rows = full_table[header_index + 1 : ]
        for idx, row in enumerate(data_rows):
            if row[1] == None:
                continue
            
            else:
                county_name = row[1]
                clean_county_name = county_name.upper()
                if clean_county_name not in df.index:
                    df.loc[clean_county_name] = [None] * (len(columns) - 1)
                df.loc[clean_county_name, columns[counter + 2]] = row[-1]
        counter += 1
    return df
    
my_df = get_data_frame(all_data)
my_df.to_csv("files/va_data.csv")
