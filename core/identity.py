import random
from faker import Faker
import sqlite3
import os
import time
import uuid

class Persona:
    def __init__(self, seed=None):
        self.faker = Faker()
        if seed is not None:
            random.seed(seed)
            self.faker.seed_instance(seed)
        self.name = self.faker.name()
        self.address = self.faker.address().replace('\n', ', ')
        self.phone = self.faker.phone_number()
        self.email = self.faker.email()
        self.cc_number = self.faker.credit_card_number(card_type=None)
        self.cc_exp = self.faker.credit_card_expire()
        self.cc_cvv = self.faker.credit_card_security_code()
        self.cc_name = self.name

    def as_dict(self):
        return {
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'cc_number': self.cc_number,
            'cc_exp': self.cc_exp,
            'cc_cvv': self.cc_cvv,
            'cc_name': self.cc_name
        }

class IdentityEngine:
    def inject_address(self, profile_path, persona):
        print(f"[*] INJECTING ADDRESS: {persona.get('address')}")
        
        db_path = os.path.join(profile_path, "Default", "Web Data")
        
        # Ensure parent dir exists (if Burner hasn't run yet)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Standard Chromium Schema for Autofill
        c.execute('''CREATE TABLE IF NOT EXISTS autofill_profiles 
                     (guid VARCHAR PRIMARY KEY, company_name VARCHAR, 
                      street_address VARCHAR, city VARCHAR, state VARCHAR, 
                      zipcode VARCHAR, country_code VARCHAR, date_modified INTEGER, use_count INTEGER)''')

        guid = str(uuid.uuid4())
        c.execute("""
            INSERT OR REPLACE INTO autofill_profiles 
            (guid, company_name, street_address, city, state, zipcode, country_code, date_modified, use_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            guid, "", persona.get('address'), persona.get('city'), 
            persona.get('state'), persona.get('zip'), persona.get('country'), 
            int(time.time()), 25 # High use count = High trust
        ))
        
        conn.commit()
        conn.close()
