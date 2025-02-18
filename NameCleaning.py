import pandas as pd
import re

def clean_name(name):
    if pd.isna(name):
        return name  # Keep NaN values unchanged
    
    # If the name is in format like "NameMD" (without a space), remove MD
    name = re.sub(r"MD$", "", name, flags=re.IGNORECASE).strip()

    # Define patterns to remove
    patterns = [
        r",.*", r"\bMD\b", r"\b MD\b", r"\bmd\b", r"\bms\b", r"\b MS\b",
        r"\(Tag\)", r"Jr", r"\bMPH\b", r"\bM\.D\.\b", r"\bMA\b", r"\bMSCR\b",
        r"\bFACG\b", r"\bIFMCP\b", r"\bPediatrician\b"
    ]
    
    # Apply regex substitution for patterns
    for pattern in patterns:
        name = re.sub(pattern, "", name, flags=re.IGNORECASE).strip()
    
    # Ensure "Name M.D." → "Name"
    name = re.sub(r"\bM\.D\.\b$", "", name, flags=re.IGNORECASE).strip()

    return name

# Load Excel file
input_file = "input.xlsx"
df = pd.read_excel(input_file, engine='openpyxl')

# Apply the cleaning function
if "name" in df.columns:
    df["name"] = df["name"].astype(str).apply(clean_name)

# Save modified data to a new Excel file
output_file = "output.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Processed file saved as '{output_file}'")

