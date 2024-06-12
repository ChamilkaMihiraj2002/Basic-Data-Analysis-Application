import tkinter as tk
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


root = tk.Tk()
root.title("Data Analysis App")
root.geometry("800x450")
root.resizable(False, False)

def open_csv_file ():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    if file_path:
        try:
            global dataset_path
            dataset_path = file_path

        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
    else:
        messagebox.showinfo("No file selected", "Please select a CSV file.")


def calculate():
    global df
    df = pd.read_csv(dataset_path)
    print(df.describe())
    main_display = tk.Label(root, text=df.describe(), bg="white").place(x=250, y=20)
def plot_chart():
    selected_chart = chart_var.get()
    if selected_chart == "Histogram":
        plt.figure(figsize=(6, 4))  # Set figure size for readability
        plt.hist(df.select_dtypes(include=[int, float]))  # Plot numerics only
        plt.xlabel("Data Values")
        plt.ylabel("Frequency")
        plt.title("Histogram of Data")
        plt.grid(True)
        plt.show()  # Display the histogram outside the GUI

    elif selected_chart == "Bar Chart":
        selected_column = column_entry.get()  # Get the column name from the entry field
        if selected_column:
            plt.figure(figsize=(6, 4))
            sns.countplot(x=selected_column, data=df, alpha=0.9)
            plt.xlabel(selected_column)
            plt.ylabel("Count")
            plt.title(f"Bar Chart of {selected_column}")
            plt.grid(True)
            plt.show()  # Display the bar chart outside the GUI
        else:
            messagebox.showinfo("Select Column", "Please enter a column name for the Bar Chart")

    elif selected_chart == "frequency polygon":
        selected_column = column_entry.get()
        if selected_column:
            try:
                # Check if data is numerical (required for frequency polygon)
                if not pd.api.types.is_numeric_dtype(df[selected_column]):
                    messagebox.showerror("Error", "Frequency Polygon requires a numerical column.")
                    return

                # Sort data by the chosen column
                df_sorted = df.sort_values(by=selected_column)

                # Create frequency table (count of unique values)
                freq_table = df_sorted[selected_column].value_counts()

                # Extract data for plotting
                x_vals = freq_table.index.to_numpy()
                y_vals = freq_table.to_numpy()

                # Plot frequency polygon
                plt.figure(figsize=(6, 4))
                plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='b')
                plt.xlabel(selected_column)
                plt.ylabel("Frequency")
                plt.title(f"Frequency Polygon of {selected_column}")
                plt.grid(True)
                plt.show()  # Display the frequency polygon outside the GUI
            except Exception as e:
                messagebox.showerror("Error", f"Failed to plot frequency polygon: {e}")
        else:
            messagebox.showinfo("Select Column", "Please choose a column for the Frequency Polygon")

#Frame 01
frame_1 = tk.Frame(root, bg="white", bd=1, width=200, height=100)
frame_1.place(x=20, y=20)

tk.Label(frame_1, text="Select your CSV file ", width=20 , font=("Helvetica", 11)).place(x=5, y=20)
tk.Button(frame_1, text="Open CSV File", width=25 , bg="Teal", fg="white" ,command=open_csv_file).place(x=5, y=50)


tk.Button(root, text="Calculate", width=24, height=4 , bg="DarkSalmon", fg="white", font=("Helvetica", 10,'bold'), command=calculate).place(x=20, y=135)

#Frame 02
frame_2 = tk.Frame(root, bg="white", bd=1, width=200, height=200)
frame_2.place(x=20, y=225)

chart_var = tk.StringVar()
tk.Label(frame_2, text="Select Graph", width=20 , font=("Helvetica", 12)).place(x=5, y=5)
tk.Radiobutton(frame_2, text="Histogram", variable=chart_var, value="Histogram", bg="white").place(x=5, y=35)
tk.Radiobutton(frame_2, text="Bar Chart", variable=chart_var, value="Bar Chart", bg="white").place(x=5, y=55)
tk.Radiobutton(frame_2, text="frequency polygon", variable=chart_var, value="frequency polygon", bg="white").place(x=5, y=75)

column_label = tk.Label(frame_2, text="Enter Column Name:", bg="white")
column_label.place(x=5, y=105)
column_entry = tk.Entry(frame_2,width=30)
column_entry.place(x=5, y=125)
tk.Button(frame_2, text="Plot Chart", command=plot_chart, width=25, bg="Teal", fg="white").place(x=5, y=155)

#Frame 03
frame_3 = tk.Frame(root, bg="white", bd=1, width=535, height=405)
frame_3.place(x=250, y=20)


root.mainloop()
