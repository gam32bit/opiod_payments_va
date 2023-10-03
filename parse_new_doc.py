import pdfplumber
import pandas as pd
from geopy.geocoders import Nominatim

pd.set_option('display.float_format', '{:.2f}'.format)

#Extract Data from PDFs

pdf = pdfplumber.open("files/Summary-of-Opioid-Funds-to-Virginia-Localities-as-of-Jan-2023.pdf")

def extract_table_data(pdf):
    data = []
    for page in pdf.pages:

        data.append(page.extract_tables())
    return data

def get_county_list(pdf):
    
    #extract text entries from dictionary, turn into a list
    text_entries = [entry['text'] for entry in pdf.pages[2].extract_words()]
    #to skip table of contents at the beginning, set variables to first entry
    counties_unsorted = ["ACCOMACK"]
    prev_number_idx = 4
    for idx, text in enumerate(text_entries):
        if idx > 4:
            if text.isdigit():
                county = ' '.join(text_entries[prev_number_idx + 1 : idx])
                #concatenate words since last number and add to new list
                counties_unsorted.append(county.upper())
                prev_number_idx = idx
    sorted_counties = sorted(counties_unsorted)
    return sorted_counties
    

fips_df = pd.read_csv("files/fips-codes-virginia.csv", dtype={"County FIPS Code": str})
fips_df["GU Name"] = fips_df["GU Name"].str.upper()

data_stuff = extract_table_data(pdf)

def get_data_frame(data):
    columns = ["County", "FIPS", "Distributors_2021", "Distributors_2022", "Distributors_2023", "Janssen_2022", "Janssen_2023", "Total_Payment"]
    df = pd.DataFrame(columns=columns)
    df.set_index("County", inplace=True)
    counter = 0
    final = []
    for table in data:
        final.append(table)
    return final
"""         full_table = table[0] + table[1]
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
    final_df = df[final_columns] """
    
print(get_county_list(pdf))
""" print(get_data_frame(data_stuff)) """
test = '1'
print(test.isdigit())