
import pandas as pd
from fuzzywuzzy import process
import swifter

# Load Excel file
input_file = "output3.xlsx"  # Hardcoded input file
df = pd.read_excel(input_file, engine='openpyxl')

# Ensure required columns exist
if "name" in df.columns and "Full Name_x" in df.columns:

    # Convert "Full Name_x" to a list (fix for ambiguous truth value error)
    full_name_choices = df["Full Name_x"].dropna().tolist()

    # Function to perform fuzzy matching
    def fuzzy_match(name, choices):
        if pd.isna(name) or name.strip() == "":  # Handle empty names
            return pd.Series(["", 0])  # No match, 0% similarity
        result = process.extractOne(name, choices)
        if result:
            match, score = result[0], result[1]  # Extract best match and score
            with open("progress.log", "a", encoding="utf-8") as f:  # Fix Unicode error
                f.write(f"{name} -> {match} ({score}%)\n")
            return pd.Series([match, score])
        return pd.Series(["", 0])  # No match found

    # Apply fuzzy matching in parallel using swifter
    df[['Best Match', 'Fuzzy Matching Percentage']] = df['name'].swifter.apply(
        lambda x: fuzzy_match(x, full_name_choices)
    )

    # Save the modified DataFrame to a new Excel file
    output_file = "output_final.xlsx"
    df.to_excel(output_file, index=False, engine='openpyxl')

    print(f"Processed file saved as '{output_file}'")

else:
    print("Error: Required columns 'name' and 'Full Name_x' are missing in the Excel file.")