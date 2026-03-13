import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load the dataset
try:
    df = pd.read_csv('All_Diets.csv')
    print("✅ Dataset loaded successfully!")
except FileNotFoundError:
    print("❌ Error: All_Diets.csv file not found")
    exit()

# 2. Data Cleaning: Handling missing values
# Fill missing values in nutrient columns with their respective mean values
numeric_cols = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
print("✅ Data cleaning completed (missing values handled).")

# 3. Data Analysis and Metrics Calculation
# A. Calculate average macronutrient content for each diet type
avg_macros = df.groupby('Diet_type')[numeric_cols].mean()
print("\n--- Average Macronutrients by Diet Type ---")
print(avg_macros)

# B. Create new metrics: Protein-to-Carbs ratio and Carbs-to-Fat ratio
# Using .replace(0, 0.001) to avoid division by zero errors
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)'].replace(0, 0.001)
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)'].replace(0, 0.001)

# C. Identify the top 5 protein-rich recipes for each diet type
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
print("✅ Metrics calculation and top 5 analysis completed.")

# 4. Data Visualization
# Set visual style
sns.set_theme(style="whitegrid")

# A. Bar Chart: Average Protein content for each diet type
plt.figure(figsize=(12, 6))
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'], palette='viridis')
plt.title('Average Protein Content by Diet Type')
plt.ylabel('Average Protein (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('avg_protein_bar_chart.png')
print("✅ Bar chart saved: avg_protein_bar_chart.png")

# B. Heatmap: Relationship between nutrients and diet types
plt.figure(figsize=(10, 8))
sns.heatmap(avg_macros, annot=True, cmap='YlGnBu', fmt=".2f")
plt.title('Nutritional Heatmap (Mean Values) by Diet Type')
plt.savefig('macros_heatmap.png')
print("✅ Heatmap saved: macros_heatmap.png")

# C. Scatter Plot: Top 5 protein-rich recipes across cuisines
plt.figure(figsize=(12, 7))
sns.scatterplot(data=top_protein, x='Diet_type', y='Protein(g)', hue='Cuisine_type', s=100, alpha=0.7)
plt.title('Distribution of Top 5 Protein-Rich Recipes per Diet Type')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('top_protein_scatter.png')
print("✅ Scatter plot saved: top_protein_scatter.png")

# Show plots (optional, depending on VM graphical support)
# plt.show()