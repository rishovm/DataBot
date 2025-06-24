# DataBot
Databot is an intelligent Python script that automates data analysis and visualization from CSV or Excel files, offering user-guided insights and saving results with interpretations.
📘 Databot User Manual
🔹 Overview
Databot is a Python-based tool for automated data analysis and visualization. It accepts .csv or .xlsx files as input, guides the user through available analysis and visualization options, performs comparisons of numerical data across rows, and generates plots with suggested interpretations — saving everything in a structured outputs folder.

🔹 Features
Accepts both .csv and .xlsx files (auto-detects the format).

Handles different encodings (utf-8, latin1, etc.).

Suggests 10+ analysis techniques and 10+ visualizations.

Performs comparisons of rows across all columns (from column B onward).

Generates visualizations (e.g., bar plots) with labels and legends.

Creates PNG files for each visualization.

Writes a text interpretation file for each analysis.

Organizes all results in a clean outputs folder.

🔹 Requirements
Python 3.x

Required libraries:

bash
Copy
Edit
pip install pandas matplotlib seaborn openpyxl
🔹 How to Use
1. 📁 Prepare Your Dataset
Ensure your dataset:

Is saved in .csv or .xlsx format.

Has row identifiers (like Drug names) in Column A.

Contains numeric values from Column B onward (for comparison and visualization).

2. ▶️ Run Databot
From the terminal or command prompt:

bash
Copy
Edit
python databot.py
3. 🗂️ Input File
You'll be prompted to enter the path to your data file:

pgsql
Copy
Edit
Enter the path to your data file (.csv or .xlsx):
Example input:

swift
Copy
Edit
C:/Users/YourName/Documents/data.xlsx
🔸 You can drag and drop the file into the terminal for quick path input (remove quotes if present).

🔹 User Interaction
4. 📊 Choose Data Analysis Techniques
Databot displays a list of data analysis methods like:

markdown
Copy
Edit
1. Mean Calculation
2. Median Calculation
3. Standard Deviation
...
💡 Databot suggests appropriate techniques based on the dataset, but you can choose manually by number.

5. 📈 Choose Visualization Types
Options like:

mathematica
Copy
Edit
1. Bar Plot
2. Line Plot
3. Box Plot
...
Again, Databot provides suggestions, but you can choose from the list.

🔹 What Databot Does Internally
Extracts all rows (from Row 2 onward) and compares values across all columns (B onwards).

For each column (criteria), it:

Plots the values across all rows (entities).

Saves the plot as a .png in the outputs folder.

Generates a text interpretation of the data, indicating highest/lowest performers, mean, and deviation.

🔹 Output Structure
After completion, the following files are generated inside the outputs/ folder (auto-created):

Copy
Edit
outputs/
├── comparison_Cmax.png
├── interpretation_Cmax.txt
├── comparison_Clearance.png
├── interpretation_Clearance.txt
├── ...
Each:

comparison_*.png = Data visualization of a column (criteria).

interpretation_*.txt = Suggested interpretation for the plot.

🔹 Error Handling
Databot gracefully handles:

Unsupported encodings (tries utf-8, then latin1).

Special characters in column names (sanitized for filenames).

Missing or malformed data (skips problematic columns).

🔹 Best Practices
Use clear headers for each column.

Ensure numeric consistency for analytical columns (avoid mixed data types).

Rename special characters in headers if possible (Databot handles it, but clarity helps).

View output .png plots with any image viewer and .txt interpretations in Notepad or any text editor.

🔹 Example Use Case
Imagine a CSV file comparing 10 drugs on ADMET criteria:

Drug Name	Solubility	Cmax	Half-life	Clearance
Drug A	0.9	2.1	8	5.3
Drug B	0.7	1.5	6	6.1
...	...	...	...	...

Databot will:

Compare each drug across all 4 parameters.

Create plots like “Comparison of Drugs based on Clearance”.

Save interpretation_Clearance.txt with insights (e.g., Drug B has highest clearance, Drug A has lowest, etc.).

🔹 Troubleshooting
Issue	Solution
Encoding error	Ensure correct encoding or use .xlsx
Path error	Make sure the path exists and has no typos
No output files	Check if the data columns contain valid numeric values
Visualizations not saved	Ensure no permission issues in the folder
Unicode errors	Avoid special characters in filenames or paths

