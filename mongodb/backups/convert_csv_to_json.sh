#!/bin/bash

# Input and output files
INPUT_CSV="candidates_skills.csv"
OUTPUT_JSON="candidates_skills.json"

# Fixed values
COMPANY_ID="6792df37ae32f695bcd13420"
COMPANY_NAME="Samana Group LLC"
REVIEWED_BY="Candidate"

# Start JSON array
echo "[" > "$OUTPUT_JSON"

# Process CSV
{
  # Read headers (categories) and skill names
  IFS=',' read -r -a categories
  IFS=',' read -r -a skill_names

  # Process each data row
  first_row=true
  while IFS=',' read -r email rest; do
    # Split the rest of the row into an array
    IFS=',' read -r -a ratings <<< "$rest"

    # Loop through ratings
    for ((i=0; i<${#ratings[@]}; i++)); do
      rating="${ratings[$i]}"
      if [ -n "$rating" ]; then  # Skip empty ratings
        # Add comma between objects (except for first one)
        if [ "$first_row" = false ]; then
          echo "," >> "$OUTPUT_JSON"
        else
          first_row=false
        fi

        # Create JSON object using jq, explicitly without _id
        jq -c -n \
          --arg companyId "$COMPANY_ID" \
          --arg companyName "$COMPANY_NAME" \
          --arg email "$email" \
          --arg category "${categories[$((i+1))]}" \
          --arg skillName "${skill_names[$((i+1))]}" \
          --argjson rating "$rating" \
          --arg reviewedBy "$REVIEWED_BY" \
          --arg reviewerEmail "$email" \
          '{
            "companyId": $companyId,
            "companyName": $companyName,
            "email": $email,
            "skillsetCategory": $category,
            "skillsetName": $skillName,
            "skillsetRating": $rating,
            "reviewedBy": $reviewedBy,
            "reviewerEmail": $reviewerEmail
          }' >> "$OUTPUT_JSON"
      fi
    done
  done
} < "$INPUT_CSV"

# Close JSON array
echo "]" >> "$OUTPUT_JSON"

# Optional: Pretty-print the JSON (remove this line if you want compact output)
jq '.' "$OUTPUT_JSON" > tmp.json && mv tmp.json "$OUTPUT_JSON"

echo "Converted CSV to JSON in $OUTPUT_JSON"
