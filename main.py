# Caedon Ewing
# Date: 6/25/2024
# This code aims to combine the timestamp files by continuing the first file based on
# the numbers of rows in the other given files, incrementing by a number calculated by the difference between the
# last two rows of the first file


import pandas as pd

# Input the path to all files you want to combine:
csv_file_list = [r"C:\Users\gangliagurdian\Desktop\Unsupervised Learning\Test_Data\Test\VTSA.csv",
                 r"C:\Users\gangliagurdian\Desktop\Unsupervised Learning\Test_Data\Test\VTSB.csv",
                 r"C:\Users\gangliagurdian\Desktop\Unsupervised Learning\Test_Data\Test\VTSC.csv"]

# Input the path to where you want to store the result
output_file = r"C:\Users\gangliagurdian\Desktop\Unsupervised Learning\Test_Data\Resultant.csv"

X = True  # Sets temp value to final_row value


# Function to read CSV file with space as delimiter
def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().replace(' ', ',')
    with open(file_path, 'w') as file:
        file.write(content)
    return pd.read_csv(file_path, usecols=[0, 1], header=None)


# Function to replace the commas added with spaces
def fix_Csv(file_path):
    with open(file_path, 'r') as file:
        content = file.read().replace(',', ' ')
    with open(file_path, 'w') as file:
        file.write(content)


# Read each CSV file and store in globals
for i in range(len(csv_file_list)):
    globals()[f"df_{i}"] = read_csv_file(csv_file_list[i])

first_file = True  # Keeps track if the first file is being read in
for i in range(len(csv_file_list)):
    if first_file:
        df_name = globals()[f"df_{i}"]  # Retrieve the DataFrame object using globals()
        final_row = df_name.iloc[-1].astype(int)  # Stores the final row of the first file
        subtraction = final_row - df_name.iloc[-2].astype(int)  # Divides the last two rows

        # Copies file to the output file
        df_name.to_csv(output_file, index=False, header=None)
        first_file = False

        fix_Csv(csv_file_list[i])

    else:
        df = globals()[f"df_{i}"]  # Retrieve the DataFrame object using globals()

        row_count = len(df)  # Gets the amount of rows in file
        if X:  # If initial iteration
            temp2 = final_row  # Copies the final row to temp variable

        # Initialize a list to accumulate row strings
        rows_to_write = []

        w = 0
        while w < row_count:
            sum_row = (temp2 + subtraction).astype(int)  # Add final row + the subtacted rows
            sum_row_str = sum_row.to_frame().T.to_csv(header=False, index=False).strip()  # Convert to CSV row string and strip newlines
            rows_to_write.append(sum_row_str)  # Add to list of rows to write
            temp2 = sum_row
            w += 1

        # Write all accumulated rows to the output file at once
        with open(output_file, 'a') as fd:
            fd.write("\n".join(rows_to_write) + "\n")  # Join rows with newline and write to file
        X = False

    fix_Csv(output_file)  # Restores resultant CSV to original format
    fix_Csv(csv_file_list[i])  # Restores CSV's given to original format

    # Read the final output to verify
print(pd.read_csv(output_file))
