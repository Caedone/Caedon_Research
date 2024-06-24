import pandas as pd

csv_file_list = ["file1.csv", "file2.csv", "file3.csv"]  # Input CSV File names
output_file = "output.csv"  # Result output name
X = True


# Function to read CSV file with space as delimiter
def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().replace(' ', ',')
    with open(file_path, 'w') as file:
        file.write(content)
    return pd.read_csv(file_path, header=None)


# Read each CSV file and store in globals
for i in range(len(csv_file_list)):
    globals()[f"df_{i}"] = read_csv_file(csv_file_list[i])

first_file = True
for i in range(len(csv_file_list)):
    if first_file:
        df_name = globals()[f"df_{i}"]  # Retrieve the DataFrame object using globals()

        final_row = df_name.iloc[-1].astype(int)  # Stores the final row of the first file
        division = final_row / df_name.iloc[-2].astype(int)  # Divides the last two rows

        # Copies file to the output file
        df_name.to_csv(output_file, index=False, header=True)
        first_file = False

    else:
        df = globals()[f"df_{i}"]  # Retrieve the DataFrame object using globals()
        row_count = len(df)  # Gets the amount of rows in file
        if X == True:  # If initial iteration
            temp2 = final_row  # Copies the final row to temp variable

        # Initialize a list to accumulate row strings
        rows_to_write = []

        w = 0
        while w < row_count:
            sum_row = (temp2 + division).astype(int)  # Add final row + the divided rows
            sum_row_str = sum_row.to_frame().T.to_csv(header=False, index=False).strip()  # Convert to CSV row string and strip newlines
            rows_to_write.append(sum_row_str)  # Add to list of rows to write
            temp2 = sum_row
            w += 1

        # Write all accumulated rows to the output file at once
        with open(output_file, 'a') as fd:
            fd.write("\n".join(rows_to_write) + "\n")  # Join rows with newline and write to file

        X = False

    # Read the final output to verify
print(pd.read_csv(output_file))
