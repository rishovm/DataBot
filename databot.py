import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import re
import plotly.express as px
print ("Welcome to the world of data modelling and simulation")
print ("Please enter the path of your data file to be analysed")
# Auto-create output folder
def create_outputs_folder():
    output_dir = os.path.join(os.getcwd(), 'outputs')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def sanitize_filename(name):
    return re.sub(r'[\\/*?"<>|\s]', "_", name)

# Load file
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

# Data analysis techniques
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

# Data visualization options
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
    "Swarm Plot",
    "Sales Territory Mapping"
]

def perform_analysis(df, analysis_choices, output_dir):
    numeric_df = df.select_dtypes(include=np.number)
    summary = {}

    if "Mean Calculation" in analysis_choices:
        summary["Mean"] = numeric_df.mean()
    if "Median Calculation" in analysis_choices:
        summary["Median"] = numeric_df.median()
    if "Standard Deviation" in analysis_choices:
        summary["Std"] = numeric_df.std()
    if "Min/Max Values" in analysis_choices:
        summary["Min"] = numeric_df.min()
        summary["Max"] = numeric_df.max()
    if "Correlation Matrix" in analysis_choices:
        summary["Correlation"] = numeric_df.corr()
    if "Outlier Detection" in analysis_choices:
        summary["Outliers"] = ((numeric_df - numeric_df.mean()).abs() > 2 * numeric_df.std())
    if "Normalization" in analysis_choices:
        summary["Normalized"] = (numeric_df - numeric_df.min()) / (numeric_df.max() - numeric_df.min())
    if "Z-score Calculation" in analysis_choices:
        summary["Z-score"] = (numeric_df - numeric_df.mean()) / numeric_df.std()
    if "Missing Value Analysis" in analysis_choices:
        summary["Missing Values"] = df.isnull().sum()
    if "Distribution Analysis" in analysis_choices:
        summary["Distribution"] = numeric_df.apply(lambda x: x.value_counts().head())

    for key, val in summary.items():
        val.to_csv(os.path.join(output_dir, f"{sanitize_filename(key)}.csv"))

def visualize(df, visual_choices, output_dir):
    row_labels = df.iloc[:, 0].astype(str)
    data = df.iloc[:, 1:]

    for col in data.columns:
        try:
            values = data[col].astype(float)

            for vis in visual_choices:
                plt.figure(figsize=(10, 6))

                if vis == "Bar Plot":
                    bars = plt.bar(row_labels, values, color='skyblue')
                    plt.title(f"Bar Plot: {col}")
                    plt.xlabel("Label")
                    plt.ylabel(col)
                    for bar in bars:
                        yval = bar.get_height()
                        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.05, f'{yval:.2f}', ha='center', va='bottom', fontsize=8)

                elif vis == "Line Plot":
                    plt.plot(row_labels, values, marker='o')
                    plt.title(f"Line Plot: {col}")
                    plt.xlabel("Label")
                    plt.ylabel(col)

                elif vis == "Box Plot":
                    sns.boxplot(y=values)
                    plt.title(f"Box Plot: {col}")

                elif vis == "Violin Plot":
                    sns.violinplot(y=values)
                    plt.title(f"Violin Plot: {col}")

                elif vis == "Histogram":
                    plt.hist(values, bins=10, color='orange', edgecolor='black')
                    plt.title(f"Histogram: {col}")
                    plt.xlabel(col)
                    plt.ylabel("Frequency")

                elif vis == "Scatter Plot":
                    plt.scatter(range(len(values)), values)
                    plt.title(f"Scatter Plot: {col}")
                    plt.xlabel("Index")
                    plt.ylabel(col)

                elif vis == "Heatmap":
                    sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
                    plt.title("Heatmap of Correlation")
                    break  # Only once for entire dataset

                elif vis == "Pie Chart":
                    plt.pie(values, labels=row_labels, autopct='%1.1f%%')
                    plt.title(f"Pie Chart: {col}")

                elif vis == "Area Plot":
                    plt.fill_between(range(len(values)), values)
                    plt.title(f"Area Plot: {col}")
                    plt.xlabel("Index")
                    plt.ylabel(col)

                elif vis == "Swarm Plot":
                    sns.swarmplot(y=values)
                    plt.title(f"Swarm Plot: {col}")

                elif vis == "Sales Territory Mapping":
                    if "Region" in df.columns and col != "Region":
                        region_df = df[["Region", col]].dropna()
                        region_df.columns = ["Region", "Value"]
                        fig = px.choropleth(region_df,
                                            locations="Region",
                                            locationmode="country names",
                                            color="Value",
                                            color_continuous_scale="Blues",
                                            title=f"Sales Territory Mapping: {col}",
                                            labels={'Value': col})
                        fig.update_layout(geo=dict(showframe=False, showcoastlines=False),
                                          legend_title_text="Sales")
                        html_path = os.path.join(output_dir, f"territory_map_{sanitize_filename(col)}.html")
                        fig.write_html(html_path)

                        # Static PNG
                        fig.write_image(os.path.join(output_dir, f"territory_map_{sanitize_filename(col)}.png"))

                        with open(os.path.join(output_dir, f"interpretation_territory_{sanitize_filename(col)}.txt"), 'w') as f:
                            f.write(f"This map shows regional distribution of {col}. Darker regions indicate higher values.")

                        continue

                plt.tight_layout()
                fig_path = os.path.join(output_dir, f"{vis.lower().replace(' ', '_')}_{sanitize_filename(col)}.png")
                plt.savefig(fig_path)

                # Save in SVG format for Illustrator
                svg_path = os.path.join(output_dir, f"{vis.lower().replace(' ', '_')}_{sanitize_filename(col)}.svg")
                plt.savefig(svg_path, format='svg')
                plt.close()

        except Exception as e:
            print(f"Skipping visualization for {col} due to error: {e}")

# Main
if __name__ == "__main__":
    file_path = input("Enter the path to your data file (.csv or .xlsx): ").strip('"')
    df = load_file(file_path)

    if df is not None:
        output_dir = create_outputs_folder()
        print("\n✅ File loaded successfully!")

        print("\n📊 Available Data Analysis Techniques:")
        for i, tech in enumerate(analysis_techniques, 1):
            print(f"{i}. {tech}")
        chosen_analyses = input("Enter comma-separated numbers of analysis techniques you'd like to run: ").split(",")
        chosen_analysis_names = [analysis_techniques[int(i)-1] for i in chosen_analyses if i.strip().isdigit()]

        print("\n📈 Available Data Visualization Options:")
        for i, vis in enumerate(visualization_options, 1):
            print(f"{i}. {vis}")
        chosen_visuals = input("Enter comma-separated numbers of visualizations you'd like to create: ").split(",")
        chosen_visual_names = [visualization_options[int(i)-1] for i in chosen_visuals if i.strip().isdigit()]

        print("\n🧮 Running selected data analyses...")
        perform_analysis(df, chosen_analysis_names, output_dir)

        print("📊 Creating selected visualizations...")
        visualize(df, chosen_visual_names, output_dir)

        print(f"\n✅ All outputs saved in: {output_dir}")

    else:
        print("❌ Failed to load the data file. Please check the format and try again.")
