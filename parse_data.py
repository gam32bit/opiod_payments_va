import pdfplumber
import pandas as pd
from geopy.geocoders import Nominatim

pd.set_option('display.float_format', '{:.2f}'.format)
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

fips_df = pd.read_csv("files/fips-codes-virginia.csv", dtype={"County FIPS Code": str})
fips_df["GU Name"] = fips_df["GU Name"].str.upper()


def get_data_frame(data):
    columns = ["County", "FIPS", "Distributors_2021", "Distributors_2022", "Distributors_2023", "Janssen_2022", "Janssen_2023", "Total_Payment"]
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
                    if clean_county_name.split(' ', 1)[0] in fips_df["GU Name"].values:
                        df.loc[clean_county_name, "FIPS"] = fips_df.loc[fips_df["GU Name"] == clean_county_name.split(' ', 1)[0], "County FIPS Code"].iloc[0]
                df.loc[clean_county_name, columns[counter + 2]] = round(float(row[-1].replace('$', '').replace(',', '')), 2)


        counter += 1
    columns_to_sum = ["Distributors_2021", "Distributors_2022", "Distributors_2023", "Janssen_2022", "Janssen_2023"]
    df["Total_Payment"] = df[columns_to_sum].sum(axis=1)
    total_total_payment = df["Total_Payment"].sum()
    df["Percent_of_Total"] = df["Total_Payment"] / total_total_payment
    final_columns = ["FIPS", "Percent_of_Total"]
    final_df = df[final_columns]
    return final_df
    
my_df = get_data_frame(all_data)
my_df.to_csv("files/va_data.csv")
