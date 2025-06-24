import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import re

print ("Welcome to the world of data modelling and simulation")
print ("Please enter the path of your data file to be analysed")

# Auto-create output folder
def create_outputs_folder():
    output_dir = os.path.join(os.getcwd(), 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# Make filename safe
def sanitize_filename(name):
    return re.sub(r'[\\/*?"<>|\s]', "_", name)

# Load data file
def load_file(file_path):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        else:
            df = pd.read_excel(file_path)
        return df
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding='latin1')
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

# Analysis techniques list
analysis_techniques = [
    "Mean Calculation",
    "Median Calculation",
    "Standard Deviation",
    "Min/Max Values",
    "Correlation Matrix",
    "Outlier Detection",
    "Normalization",
    "Z-score Calculation",
    "Missing Value Analysis",
    "Distribution Analysis"
]

# Visualization options list
visualization_options = [
    "Bar Plot",
    "Line Plot",
    "Box Plot",
    "Violin Plot",
    "Histogram",
    "Scatter Plot",
    "Heatmap",
    "Pie Chart",
    "Area Plot",
    "Swarm Plot"
]

# Function to perform selected data analysis
def perform_analysis(values, technique):
    if technique == "Mean Calculation":
        return f"Mean: {values.mean():.2f}"
    elif technique == "Median Calculation":
        return f"Median: {values.median():.2f}"
    elif technique == "Standard Deviation":
        return f"Standard Deviation: {values.std():.2f}"
    elif technique == "Min/Max Values":
        return f"Min: {values.min():.2f}, Max: {values.max():.2f}"
    elif technique == "Correlation Matrix":
        return "See heatmap visualization."
    elif technique == "Outlier Detection":
        outliers = values[(np.abs(values - values.mean()) > 2 * values.std())]
        return f"Outliers: {outliers.tolist()}"
    elif technique == "Normalization":
        norm = (values - values.min()) / (values.max() - values.min())
        return f"Normalized values: {norm.tolist()}"
    elif technique == "Z-score Calculation":
        z_scores = (values - values.mean()) / values.std()
        return f"Z-scores: {z_scores.tolist()}"
    elif technique == "Missing Value Analysis":
        return f"Missing values: {values.isna().sum()}"
    elif technique == "Distribution Analysis":
        return f"Skew: {values.skew():.2f}, Kurtosis: {values.kurtosis():.2f}"
    else:
        return "No analysis performed."

# Visualize selected type
def visualize_data(row_labels, values, column_name, vis_type, output_dir):
    safe_col = sanitize_filename(column_name)
    plt.figure(figsize=(10, 6))

    if vis_type == "Bar Plot":
        sns.barplot(x=row_labels, y=values)
    elif vis_type == "Line Plot":
        sns.lineplot(x=row_labels, y=values)
    elif vis_type == "Box Plot":
        sns.boxplot(data=values)
    elif vis_type == "Violin Plot":
        sns.violinplot(data=values)
    elif vis_type == "Histogram":
        sns.histplot(values, kde=True)
    elif vis_type == "Scatter Plot":
        sns.scatterplot(x=row_labels, y=values)
    elif vis_type == "Heatmap":
        sns.heatmap(pd.DataFrame(values).T, annot=True, cmap='coolwarm')
    elif vis_type == "Pie Chart":
        plt.pie(values, labels=row_labels, autopct='%1.1f%%')
    elif vis_type == "Area Plot":
        plt.fill_between(range(len(values)), values)
        plt.xticks(ticks=range(len(row_labels)), labels=row_labels, rotation=45)
    elif vis_type == "Swarm Plot":
        sns.swarmplot(y=values)
    else:
        print("Invalid visualization selected.")
        return

    plt.title(f"{vis_type} - {column_name}")
    plt.ylabel(column_name)
    plt.xlabel("Drugs" if vis_type not in ["Box Plot", "Violin Plot", "Histogram", "Swarm Plot"] else "")
    plt.tight_layout()
    file_path = os.path.join(output_dir, f"{vis_type}_{safe_col}.png")
    plt.savefig(file_path)
    plt.close()

# Analyze and visualize
def analyze_and_visualize(df, analysis_choice, vis_choice, output_dir):
    row_labels = df.iloc[:, 0].astype(str)
    data = df.iloc[:, 1:]

    for col in data.columns:
        try:
            values = pd.to_numeric(data[col], errors='coerce')

            # Data analysis
            analysis_result = perform_analysis(values, analysis_choice)

            # Visualization
            visualize_data(row_labels, values, col, vis_choice, output_dir)

            # Interpretation
            max_idx = values.idxmax()
            min_idx = values.idxmin()
            if pd.notna(max_idx) and pd.notna(min_idx):
                max_drug = row_labels.iloc[max_idx]
                min_drug = row_labels.iloc[min_idx]
                interp = (
                    f"Interpretation for {col}:\n"
                    f"{max_drug} has the highest value ({values[max_idx]:.2f}), "
                    f"{min_drug} has the lowest value ({values[min_idx]:.2f}).\n"
                    f"{analysis_result}"
                )
            else:
                interp = f"Interpretation for {col}:\n{analysis_result}"

            # Save interpretation
            with open(os.path.join(output_dir, f"interpretation_{sanitize_filename(col)}.txt"), 'w') as f:
                f.write(interp)

        except Exception as e:
            print(f"Skipping column '{col}' due to error: {e}")

# Main
if __name__ == "__main__":
    file_path = input("Enter the path to your data file (.csv or .xlsx): ").strip('"')
    df = load_file(file_path)

    if df is not None:
        output_dir = create_outputs_folder()
        print("\nAvailable Data Analysis Techniques:")
        for i, technique in enumerate(analysis_techniques, 1):
            print(f"{i}. {technique}")

        analysis_index = int(input("Choose a data analysis technique by number: ")) - 1
        analysis_choice = analysis_techniques[analysis_index]

        print("\nAvailable Visualization Techniques:")
        for i, viz in enumerate(visualization_options, 1):
            print(f"{i}. {viz}")

        vis_index = int(input("Choose a visualization type by number: ")) - 1
        vis_choice = visualization_options[vis_index]

        print(f"\nRunning {analysis_choice} with {vis_choice}...")

        analyze_and_visualize(df, analysis_choice, vis_choice, output_dir)
        print(f"\n✅ All outputs saved in: {output_dir}")
    else:
        print("❌ Failed to load the data file. Please check the path and format.")
