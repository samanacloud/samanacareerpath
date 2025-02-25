import csv
import json
from bson import ObjectId  # You'll need to install pymongo: pip install pymongo

# Input and output file names
input_csv = 'candidates_skills.csv'  # Replace with your actual CSV file name
output_json = 'candidates_skills.json'

# Fixed values for all records
fixed_values = {
    "companyId": "6792df37ae32f695bcd13420",
    "companyName": "Samana Group LLC",
    "reviewedBy": "Candidate"
}

# List to store all JSON documents
documents = []

# Read CSV and process data
with open(input_csv, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Get headers
    headers = next(csv_reader)  # First row (categories)
    skill_names = next(csv_reader)  # Second row (skillset names)
    
    # Process each candidate row
    for row in csv_reader:
        email = row[0]  # First column is email
        
        # Create a document for each skill rating
        for i in range(1, len(row)):  # Start from 1 to skip email column
            if row[i]:  # Only process if there's a rating
                document = {
                    "_id": {"$oid": str(ObjectId())},  # Generate unique ObjectId
                    "companyId": fixed_values["companyId"],
                    "companyName": fixed_values["companyName"],
                    "email": email,
                    "skillsetCategory": headers[i],
                    "skillsetName": skill_names[i],
                    "skillsetRating": int(row[i]),  # Convert rating to integer
                    "reviewedBy": fixed_values["reviewedBy"],
                    "reviewerEmail": email  # Same as candidate email
                }
                documents.append(document)

# Write to JSON file
with open(output_json, 'w', encoding='utf-8') as json_file:
    # Write as a JSON array
    json.dump(documents, json_file, indent=2)

print(f"Converted {len(documents)} records to JSON format in {output_json}")
