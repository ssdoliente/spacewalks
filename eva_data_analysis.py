# Extra Vehicular Activity (eva in this source code) Data Analysis
import matplotlib.pyplot as plt
import pandas as pd

# Data source: https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('./eva-data.json', 'r', encoding='ascii')
output_file = open('./eva-data.csv', 'w', encoding='utf-8')
graph_file = './cumulative_eva_graph.png'

print("--START--")
print(f'Reading JSON file {input_file}')

# Read the JSON file, convert the 'date' column to datetime format, and ensure 'eva' is a float. Remove rows with missing 'duration' or 'date'.
eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
eva_df['eva'] = eva_df['eva'].astype(float)
eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)

print(f'Saving to CSV file {output_file}')
# Save the cleaned DataFrame to a CSV file without the index and with UTF-8 encoding.
eva_df.to_csv(output_file, index=False, encoding='utf-8')

# Sort the DataFrame by 'date' to ensure the cumulative time is calculated in chronological order.
eva_df.sort_values('date', inplace=True)

# Convert the 'duration' column from "HH:MM" format to total hours as a float, then calculate the cumulative time spent in space over time.
eva_df['duration_hours'] = eva_df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
eva_df['cumulative_time'] = eva_df['duration_hours'].cumsum()

# Create a line graph of the cumulative time spent in space over time, with the x-axis representing the date and the y-axis representing the cumulative hours. Save the graph as a PNG file.
print(f'Plotting cumulative spacewalk duration and saving to {graph_file}')
plt.plot(eva_df['date'], eva_df['cumulative_time'], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
print("--END--")
