import pdfplumber
import pandas as pd
from geopy.geocoders import Nominatim

pd.set_option('display.float_format', '{:.2f}'.format)

#Extract Data from PDFs

pdf = pdfplumber.open("files/Summary-of-Opioid-Funds-to-Virginia-Localities-as-of-Jan-2023.pdf")

#first and last tables weren't extracting properly so I'm just typing them out

first_table = [[
    [None, 'Direct Distribution from Settlement Administrator', None, None, None, None],
    ['Fiscal Year', 'Distributors', 'Janssen', 'Mallinckrodt', 'From OAA', '25%\nIncentive'],
    ['FY 2022', '14,151', '0', '0', '0', '0'],
    ['FY 2023', '24,546', '61,395', '3,642', '32,416', '8,104'],
    ['FY 2024', '14,872', '0', 'Still', '5,453', '1,363'],
    ['FY 2025', '18,614', '0', 'being', '6,825', '1,706'],
    ['FY 2026', '18,614', '0', 'determined', '6,826', '1,706'],
    ['FY 2027', '18,614', '2,857', '', '7,873', '1,968'],
    ['FY 2028', '18,614', '2,857', '', '7,873', '1,968'],
    ['FY 2029', '21,893', '2,857', '', '9,075', '2,269'],
    ['FY 2030', '21,893', '3,638', '', '9,361', '2,340'],
    ['FY 2031', '21,893', '3,638', '', '9,361', '2,340'],
    ['FY 2032', '18,403', '3,638', '', '8,082', '2,020'],
    ['FY 2033', '18,403', '0', '', '6,748', '1,687'],
    ['FY 2034', '18,403', '0', '', '6,748', '1,687'],
    ['FY 2035', '18,403', '0', '', '6,748', '1,687'],
    ['FY 2036', '18,403', '0', '', '6,748', '1,687'],
    ['FY 2037', '18,403', '0', '', '6,748', '1,687'],
    ['FY 2038', '18,403', '0', '', '6,748', '1,687'],
    ['FY 2039', '18,403', '0', '', '6,748', '1,687'],
    [None, '$ 340,928', '$ 80,881', 'TBD', '$ 150,379', '$ 37,595']
]]
#typing out last table because it wasn't extracting right for some reason
last_page_table = [[
    [None, 'Direct Distribution from Settlement Administrator', None, None, None, None],
    ['Fiscal Year', 'Distributors', 'Janssen', 'Mallinckrodt', 'From OAA', '25%\nIncentive'],
    ['FY 2022', '22,812', '0', '0', '0', '0'],
    ['FY 2023', '39,570', '98,972', '5,871', '52,256', '13,064'],
    ['FY 2024', '23,975', '0', 'Still', '8,791', '2,198'],
    ['FY 2025', '30,008', '0', 'being', '11,003', '2,751'],
    ['FY 2026', '30,008', '0', 'determined', '11,003', '2,751'],
    ['FY 2027', '30,008', '4,606', '', '12,692', '3,173'],
    ['FY 2028', '30,008', '4,606', '', '12,692', '3,173'],
    ['FY 2029', '35,292', '4,606', '', '14,630', '3,657'],
    ['FY 2030', '35,292', '5,865', '', '15,091', '3,773'],
    ['FY 2031', '35,292', '5,865', '', '15,091', '3,773'],
    ['FY 2032', '29,667', '5,865', '', '13,028', '3,257'],
    ['FY 2033', '29,667', '0', '', '10,878', '2,719'],
    ['FY 2034', '29,667', '0', '', '10,878', '2,719'],
    ['FY 2035', '29,667', '0', '', '10,878', '2,719'],
    ['FY 2036', '29,667', '0', '', '10,878', '2,719'],
    ['FY 2037', '29,667', '0', '', '10,878', '2,719'],
    ['FY 2038', '29,667', '0', '', '10,878', '2,719'],
    ['FY 2039', '29,667', '0', '', '10,878', '2,719'],
    [None, '$ 549,599', '$ 130,386', 'TBD', '$ 242,421', '$ 60,605']
]]

def extract_table_data(pdf, first_page, last_page):
    data = []
    
    for idx, page in enumerate(pdf.pages):
        if idx > 2:
            data.append(page.extract_tables())  
    data.pop()
    data.append(last_page)
    return data

def get_county_list(pdf):
    
    #extract text entries from dictionary, turn into a list
    text_entries = [entry['text'] for entry in pdf.pages[2].extract_words()]
    #to skip table of contents at the beginning, set variables to first entry
    counties_unsorted = ["ACCOMACK COUNTY"]
    prev_number_idx = 4
    for idx, text in enumerate(text_entries):
        if idx > 4:
            if text.isdigit():
                county = ' '.join(text_entries[prev_number_idx + 1 : idx])
                #concatenate words since last number and add to new list
                county = county.upper()
                #add county ending to properly match FIPS
                if "CITY" not in county:
                    county = county + " COUNTY"
                elif county == "JAMES CITY" or county == "CHARLES CITY":
                    county = county + " COUNTY"
                counties_unsorted.append(county)
                prev_number_idx = idx
    sorted_counties = sorted(counties_unsorted)
    return sorted_counties

fips_df = pd.read_csv("files/fips-codes-virginia.csv", dtype={"County FIPS Code": str})
fips_df["GU Name"] = fips_df["GU Name"].str.upper()
fips_df["Entity Description"] = fips_df["Entity Description"].str.upper()

data_stuff = extract_table_data(pdf, first_table, last_page_table)

counties = get_county_list(pdf)
years = list(range(2022, 2040))

#Create variables for multi-index empty dataframe

# Create tuples for the multi-level index
county_tuples = [(county, year) for year in years for county in counties]
print("Unique elements in county_tuples:", len(set(county_tuples)))


def get_data_frame_settlement_by_year(data, index_tuples):
    columns = ["Distributors", "Janssen", "Mallinckrodt", "From OAA", "25% Incentive"]
    index = pd.MultiIndex.from_tuples(index_tuples, names=["County", "Fiscal Year"])
    print("DF index is ", len(index))
    clean_data = []

    for table in data:
    # Skip the first two rows and the last row, and remove the first column (Fiscal Year)
        exact_table = table[0]
        clean_table = exact_table[2:-1]
        for row in clean_table:
            clean_row = row[1:]
            new_row = []
            for cell in clean_row:
                
                clean_cell = cell.replace("$", "").replace(",", "")
                if clean_cell.replace('.', '', 1).isdigit():
                    new_row.append(float(clean_cell))
                else:
                    new_row.append(None)
            clean_data.append(new_row)
       
    final_df = pd.DataFrame(clean_data, index=index, columns=columns)
    return final_df

print(data_stuff)