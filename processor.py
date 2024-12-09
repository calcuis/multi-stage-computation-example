import pandas as pd

# Read the input CSV file
input_file = 'input.csv'
# Stage 1 output
output_file1 = 'output1.csv'
# Stage 2 output
output_file2 = 'output2.csv'

df = pd.read_csv(input_file)

# Stage 1
# Calculate the sum of 'Score' for each 'Session'
session_sums = df.groupby('Session')['Score'].sum().reset_index()
session_sums.rename(columns={'Score': 'Sum'}, inplace=True)

# Merge the sums back into the original DataFrame
df = df.merge(session_sums, on='Session', how='left')

# Remove duplicate sums within each Session
df['Sum'] = df.apply(lambda row: row['Sum'] if df[df['Session'] == row['Session']].index[0] == row.name else '', axis=1)

# Save the output to a new CSV file
df.to_csv(output_file1, index=False)
print(f"Stage 1 process completed; output saved to {output_file1}")

# Stage 2
# Load the input CSV file
data = pd.read_csv(output_file1)

# Create the 'Point' column based on the condition
# If 'Sum' > 'Score', set 'Point' to 'Sum', otherwise set it to None
data['Point'] = data.apply(lambda row: row['Sum'] if pd.notnull(row['Sum']) and pd.notnull(row['Score']) and row['Sum'] > row['Score'] else None, axis=1)

# Save the result to 'output.csv'
data.to_csv(output_file2, index=False)

print(f"Stage 2 process completed; output saved to {output_file2}")
