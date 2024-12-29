import pdfplumber
import re
import sqlite3

# Regular expressions for extracting form data
per_street_pattern = r"3\.1 Street Address:\s*(.*?)(?:_+)?$"
per_city_pattern = r"3\.2 City:\s*([A-Za-z\s]+)"
per_state_pattern = r"3\.3 State:\s*([A-Za-z\s]+)"
per_zip_pattern =  r"3\.4 Zip Code:\s*([0-9]+)"
per_country_pattern = r"3\.5 Country:\s*([A-Za-z\s]+)"
per_dob_pattern = r"4\. Date of Birth:\s*(\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{1,4})"
per_age_pattern = r"5\. Age:\s*(\d+)"
per_gender_pattern = r"6\. Gender:\s*([A-Za-z\s]+)"
per_passport_pattern = r"7\. Passport:\s*([A-Za-z0-9]+)"
per_mobile_pattern = r"8\. Mobile:\s*([0-9\-]+)"
per_pan_pattern = r"9\. PAN No.:\s*([A-Za-z0-9]+)"
per_visa_pattern = r"10\. Visa:\s*([A-Za-z0-9]+)"
per_email_pattern = r"11\. Email ID:\s*([\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,})"
per_emergency_pattern = r"12\. Name of Emergency Contact:\s*([A-Za-z\s]+)"
per_emergency_contact_pattern =  r"13\. Emergency Contact's Number:\s*([0-9\-]+)"
per_relocation_pattern = r"14\. Available for Relocation:\s*(X|x|__*)"

# Patterns for Current Address
current_street_pattern = r"3\.1 Street Address:\s*(.*?)(?:_+)?$"
current_city_pattern = r"3\.2 City:\s*([A-Za-z\s]+)"
current_state_pattern = r"3\.3 State:\s*([A-Za-z\s]+)"
current_zip_pattern = r"3\.4 Zip Code:\s*([0-9]+)"
current_country_pattern = r"3\.5 Country:\s*([A-Za-z\s]+)"

# Class to store form data
class FormData:
    def __init__(self):
        # Initialize dictionaries with default empty values
        self.permanent_address = {
            "street": None,
            "city": None,
            "state": None,
            "zip_code": None,
            "country": None
        }
        self.current_address = {
            "street": None,
            "city": None,
            "state": None,
            "zip_code": None,
            "country": None
        }
        self.general_details = {}

    def set_permanent_address(self, street, city, state, zip_code, country):
        self.permanent_address = {
            "street": street,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "country": country
        }

    def set_current_address(self, street, city, state, zip_code, country):
        self.current_address = {
            "street": street,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "country": country
        }

    def set_general_details(self, dob, age, gender, passport, mobile, pan, visa, email, emergency_contact_name, emergency_contact_number, relocation):
        self.general_details = {
            "dob": dob,
            "age": age,
            "gender": gender,
            "passport": passport,
            "mobile": mobile,
            "pan": pan,
            "visa": visa,
            "email": email,
            "emergency_contact_name": emergency_contact_name,
            "emergency_contact_number": emergency_contact_number,
            "relocation": relocation
        }

# Create the database and tables
def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permanent_address (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            street TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            country TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS current_address (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            street TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            country TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS general_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dob TEXT,
            age INTEGER,
            gender TEXT,
            passport TEXT,
            mobile TEXT,
            pan TEXT,
            visa TEXT,
            email TEXT,
            emergency_contact_name TEXT,
            emergency_contact_number TEXT,
            relocation TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Insert data into the tables
def insert_data(form_data):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()

    # Insert into permanent_address table
    cursor.execute('''
        INSERT INTO permanent_address (street, city, state, zip_code, country)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        form_data.permanent_address['street'],
        form_data.permanent_address['city'],
        form_data.permanent_address['state'],
        form_data.permanent_address['zip_code'],
        form_data.permanent_address['country']
    ))

    # Insert into current_address table
    cursor.execute('''
        INSERT INTO current_address (street, city, state, zip_code, country)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        form_data.current_address['street'],
        form_data.current_address['city'],
        form_data.current_address['state'],
        form_data.current_address['zip_code'],
        form_data.current_address['country']
    ))

    # Insert into general_details table
    cursor.execute('''
        INSERT INTO general_details (dob, age, gender, passport, mobile, pan, visa, email, emergency_contact_name, emergency_contact_number, relocation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        form_data.general_details['dob'],
        form_data.general_details['age'],
        form_data.general_details['gender'],
        form_data.general_details['passport'],
        form_data.general_details['mobile'],
        form_data.general_details['pan'],
        form_data.general_details['visa'],
        form_data.general_details['email'],
        form_data.general_details['emergency_contact_name'],
        form_data.general_details['emergency_contact_number'],
        form_data.general_details['relocation']
    ))

    conn.commit()
    conn.close()

# Extract the form data
def extract_form_data(pdf_path):
    text = ""

    # Open the PDF and extract text
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    lines = text.split('\n')
    form_data = FormData()

    # Extract Permanent Address
    street_address = re.search(per_street_pattern, lines[6])
    form_data.set_permanent_address(
        street_address.group(1).strip() if street_address else None,
        re.search(per_city_pattern, lines[7]).group(1).strip() if re.search(per_city_pattern, lines[7]) else None,
        re.search(per_state_pattern, lines[7]).group(1).strip() if re.search(per_state_pattern, lines[7]) else None,
        re.search(per_zip_pattern, lines[8]).group(1).strip() if re.search(per_zip_pattern, lines[8]) else None,
        re.search(per_country_pattern, lines[8]).group(1).strip() if re.search(per_country_pattern, lines[8]) else None
    )
    current_street_address = re.search(current_street_pattern, lines[10])
    form_data.set_current_address(
        current_street_address.group(1).strip() if current_street_address else None,
        re.search(current_city_pattern, lines[11]).group(1).strip() if re.search(current_city_pattern, lines[11]) else None,
        re.search(current_state_pattern, lines[11]).group(1).strip() if re.search(current_state_pattern, lines[11]) else None,
        re.search(current_zip_pattern, lines[12]).group(1).strip() if re.search(current_zip_pattern, lines[12]) else None,
        re.search(current_country_pattern, lines[12]).group(1).strip() if re.search(current_country_pattern, lines[12]) else None
    )

    # Extract General Details
    form_data.set_general_details(
        re.search(per_dob_pattern, lines[13]).group(1).strip() if re.search(per_dob_pattern, lines[13]) else None,
        re.search(per_age_pattern, lines[13]).group(1).strip() if re.search(per_age_pattern, lines[13]) else None,
        re.search(per_gender_pattern, lines[13]).group(1).strip() if re.search(per_gender_pattern, lines[13]) else None,
        re.search(per_passport_pattern, lines[14]).group(1).strip() if re.search(per_passport_pattern, lines[14]) else None,
        re.search(per_mobile_pattern, lines[14]).group(1).strip() if re.search(per_mobile_pattern, lines[14]) else None,
        re.search(per_pan_pattern, lines[14]).group(1).strip() if re.search(per_pan_pattern, lines[14]) else None,
        re.search(per_visa_pattern, lines[15]).group(1).strip() if re.search(per_visa_pattern, lines[15]) else None,
        re.search(per_email_pattern, lines[15]).group(1).strip() if re.search(per_email_pattern, lines[15]) else None,
        re.search(per_emergency_contact_pattern, lines[16]).group(1).strip() if re.search(per_emergency_contact_pattern, lines[16]) else None,
        re.search(per_emergency_contact_pattern, lines[17]).group(1).strip() if re.search(per_emergency_contact_pattern, lines[17]) else None,
        re.search(per_relocation_pattern, lines[17]).group(1).strip() if re.search(per_relocation_pattern, lines[17]) else None
    )

    return form_data


if __name__ == '__main__':
    pdf_path = 'filled_form.pdf'
    form_data = extract_form_data(pdf_path)
    create_database()  # Create tables if they don't exist
    insert_data(form_data)  # Insert extracted data into the database
    print("Data inserted successfully.")
