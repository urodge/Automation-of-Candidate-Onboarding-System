from img2table.document import Image
from img2table.document import PDF
import pandas as pd
from img2table.ocr import PaddleOCR
import PyPDF2
import re

from database import LocalDatabase
db = LocalDatabase()

paddle_ocr = PaddleOCR(lang="en", kw={"use_dilation": True})

def extract_table_data(pdf_path):
    pdf = PDF(src=pdf_path)

    # Extract tables
    extracted_tables = pdf.extract_tables(ocr=paddle_ocr,
                                        implicit_rows=False,
                                        borderless_tables=False,
                                        min_confidence=50)

    return extracted_tables

"""
print(extracted_tables[0][0].df) --- first table
print(extracted_tables[1][0].df) --- second table
print(extracted_tables[1][1].df) --- third table
print(extracted_tables[1][2].df) --- fourth table
print(extracted_tables[1][3].df) --- fifth table
"""

# save tables in the local.db

def save_tables(extracted_tables):
    try:
        first_table = extracted_tables[0][0].df
        first_table.columns = first_table.iloc[0]
        first_table = first_table.iloc[1:]
        first_table = first_table.reset_index(drop=True)
        for index, row in first_table.iterrows():          
            values = row.to_dict().values()
            db.insert_data("Education",{
                "SrNo":list(values)[0],
                "School_University":list(values)[1],
                "Qualification":list(values)[2],
                "CGPA":list(values)[3],
                "Passout_Year":list(values)[4]
            })
    finally:  
        try:      
            second_table = extracted_tables[1][0].df
            second_table.columns = second_table.iloc[0]
            second_table = second_table.iloc[1:]
            second_table = second_table.reset_index(drop=True)
            for index, row in second_table.iterrows():          
                values = row.to_dict().values()
                db.insert_data("Programs",{
                    "Program":list(values)[0],
                    "Contents":list(values)[1],
                    "Organized_By":list(values)[2],
                    "Duration":list(values)[3]
                })
        finally:
            try:
                third_table = extracted_tables[1][1].df
                third_table.columns = third_table.iloc[0]
                third_table = third_table.iloc[1:]
                third_table = third_table.reset_index(drop=True)
                for index, row in third_table.iterrows():          
                    values = row.to_dict().values()
                    db.insert_data("Certifications",{
                        "SrNo":list(values)[0],
                        "Certification":list(values)[1],
                        "Duration":list(values)[2]
                    })
            finally:
                try:

                    fourth_table = extracted_tables[1][2].df
                    fourth_table.columns = fourth_table.iloc[0]
                    fourth_table = fourth_table.iloc[1:]
                    fourth_table = fourth_table.reset_index(drop=True)
                    for index, row in fourth_table.iterrows():          
                        values = row.to_dict().values()
                        db.insert_data("Relations",{
                            "Relation":list(values)[0],
                            "Occupation_Profession":list(values)[1],
                            "Resident_Location":list(values)[2]
                        })  
                finally:
                    # try:
                    #     fifth_table = extracted_tables[1][3].df
                    #     fifth_table.columns = fifth_table.iloc[0]
                    #     fifth_table = fifth_table.iloc[1:]  
                    #     fifth_table = fifth_table.reset_index(drop=True)
                    #     for index, row in fifth_table.iterrows():          
                    #         values = row.to_dict().values()
                    #         db.insert_data("Contacts",{
                    #             "Name":list(values)[0],
                    #             "Designation":list(values)[1],
                    #             "Contact_No":list(values)[2]
                    #         })
                    # finally:
                        db.insert_data("Education",{
                        "SrNo":None,
                        "School_University":None,
                        "Qualification":None,
                        "CGPA":None,
                        "Passout_Year":None
                        })
                        db.insert_data("Programs",{
                            "Program":None,
                            "Contents":None,
                            "Organized_By":None,
                            "Duration":None
                        })
                        db.insert_data("Certifications",{
                            "SrNo":None,
                            "Certification":None,
                            "Duration":None
                        })
                        db.insert_data("Relations",{
                            "Relation":None,
                            "Occupation_Profession":None,
                            "Resident_Location":None
                        })  
                        db.insert_data("Contacts",{
                            "Name":None,
                            "Designation":None,
                            "Contact_No":None
                        })        
        
if __name__ == "__main__":
    extracted_tables = extract_table_data(pdf_path="filled_form.pdf")
    save_tables(extracted_tables)
    
