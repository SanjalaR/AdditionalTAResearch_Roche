import pandas as pd

# Hardcoded file path (modify as needed)
file_path = "work.xlsx"

# Read the Excel file
df = pd.read_excel(file_path)

# Create the new column 'Fullname_with_middlename'
df["Fullname_with_middlename"] = df["Provider First Name"] + " " + df["Provider Middle Name"].str[0].fillna('') + " " + df["Provider Last Name (Legal Name)"]

# Trim any extra spaces in case middle name is missing
df["Fullname_with_middlename"] = df["Fullname_with_middlename"].str.strip()

# Save the modified file
df.to_excel("work_done.xlsx", index=False)

print("New column 'Fullname_with_middlename' added and saved in 'output.xlsx'.")

