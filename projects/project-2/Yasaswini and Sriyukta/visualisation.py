import matplotlib.pyplot as plt

# Data from your output (zip code counts)
warehouse = {'10001': 4, '10002': 4, '10003': 4, '10004': 4, '10005': 4}

# Extract zip codes and counts
zip_codes = list(warehouse.keys())
counts = list(warehouse.values())

# Create a bar chart
plt.figure(figsize=(8, 6))
plt.bar(zip_codes, counts, color='skyblue')

# Add labels and title
plt.xlabel('Zip Code')
plt.ylabel('Count')
plt.title('Zip Code Count Distribution')

# Display the chart
plt.show()
