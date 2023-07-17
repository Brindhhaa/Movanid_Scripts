import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import openpyxl


# Set the initial value for excel_file
excel_file_path = ""
sheet_names = []

options = [
    "Bench", "RF freq [Hz]", "Waveform name", "Ambient Temp [deg]", "chip temp [deg]",
    "SG_PowerLevel", "input_loss", "comp_cable_loss", "splitter_loss", "Pin_casc[dBm]",
    "pwr_out_raw", "bb_output_loss", "matching_loss", "Pout_casc[dBm]", "Gain[dB]",
    "EVM b1 compensated[dB]", "EVM b1 uncompensated[dB]", "b1 Frequency error [Hz]",
    "b1 gain imbalance [dB]", "b1 phase imbalance [deg]", "MV2613_iDC0p9 [mA]",
    "MV2613_iDC1p8 [mA]", "MV2613_Vdd [V]", "TIA Gain at cal [dB]", "MV2613_bias_idx",
    "tiaGn", "mxGn", "bias1", "bias2", "bias3", "MV2650B0_gain_idx", "VDD_2650",
    "MV2650B0_i_ps_6v", "MV2650B0_i_ps_25v", "chip_temp_2650"
]

def parse_filter_ranges(filter_ranges):
    parsed_ranges = []
    for filter_range in filter_ranges:
        if "-" in filter_range:
            # Parse the filter range if it is a range of values
            start, end = map(int, filter_range.split("-"))
            parsed_ranges.append(list(range(start, end + 1)))
        else:
            # Append the single filter value if it is not a range
            parsed_ranges.append([int(filter_range)])
    return parsed_ranges

def openFile():
    global excel_file_path
    file_paths = filedialog.askopenfilenames(filetypes=[("Excel Files", "*.xlsx; *.xls"), ("CSV Files", "*.csv")])
    if file_paths:
        file_path = file_paths[0]
        excel_file_path = file_path
        sheet_names = update_sheet_names()
        update_file_label(excel_file_path)
        update_sheet_box(sheet_names)



def update_file_label(file_path):
    file_label.config(text=file_path)


def update_sheet_box(sheet_names):
    sheetBox.delete(0, tk.END)
    for sheet in sheet_names:
        sheetBox.insert(tk.END, sheet)



def setHardcodedPath():
    global excel_file_path
    excel_file_path = "/Users/brindha/Downloads/movandiData.xlsx"
    sheet_names = update_sheet_names()
    update_file_label(excel_file_path)
    update_sheet_box(sheet_names)


def update_sheet_names():
    if excel_file_path:
        workbook = openpyxl.load_workbook(excel_file_path)
        sheet_names = workbook.sheetnames
        workbook.close()
        return sheet_names
    return []


def plotGraph():
    # Retrieve the selected x-axis, y-axis, filter indices, and filter ranges
    xName = x_var.get()
    yName = y_var.get()
    filterIndices = filter_listbox.curselection()
    filterRanges = parse_filter_ranges(filter_range_entry.get().split(","))

    # Check if all the required fields are selected
    if xName and yName and filterIndices and filterRanges:
        if len(filterIndices) != len(filterRanges):
            # Display an error message if the number of filter names and ranges don't match
            messagebox.showerror("Error", "Number of filter names and ranges should match.")
            return

        # Read the data from the Excel file
        df = pd.read_excel(excel_file_path, sheet_name="EVM", engine="openpyxl")

        filtered_dfs = []
        plot_data = []
        legend_labels = []

        # Iterate over the selected filter indices and their corresponding filter ranges
        for filterIndex, filterRange in zip(filterIndices, filterRanges):
            filter_dfs = []
            filter_legend_labels = []  # Separate list for legend labels per filter range
            for filter_value in filterRange:
                # Filter the dataframe based on the selected filter index and value
                filtered_df = df[df[options[filterIndex]] == filter_value]
                filter_dfs.append(filtered_df)
                filter_legend_labels.append(f"{options[filterIndex]} = {filter_value}")

            filtered_dfs.append(filter_dfs)
            legend_labels.extend(filter_legend_labels)

        # Create a new figure for each plot
        plt.figure()

        # Plot the data for each filtered dataframe
        for filter_dfs, label in zip(filtered_dfs, legend_labels):
            for filtered_df in filter_dfs:
                # Extract the selected x-axis and y-axis data
                new_df = filtered_df[[xName, yName]]
                xpoints = new_df[xName].values
                ypoints = new_df[yName].values
                plot_data.append((xpoints, ypoints))
                plt.plot(xpoints, ypoints, label=label)
                plt.grid(True)  # Add gridlines

        # Set the x-axis, y-axis labels, title, and formatting options
        plt.xlabel(xName)
        plt.ylabel(yName)
        plt.title("Graph of " + xName + " vs " + yName)
        plt.xticks(rotation='vertical')
        plt.ylim(0, 60)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        # Display the plot
        plt.show()
    else:
        # Display an error message if any of the required fields are not selected
        messagebox.showerror("Error", "Please select all fields.")

# Create the GUI
window = tk.Tk()

# Create the button to open the file
open_file_button = tk.Button(window, text="Open File", command=openFile)
open_file_button.pack()

# Create the button to set the hardcoded path
hardcoded_file_button = tk.Button(window, text="Hardcoded Data File (brindha)", command=setHardcodedPath)
hardcoded_file_button.pack()

sheetName = tk.Label(window, text="Select Sheet Name:")
sheetName.pack()
sheetBox = tk.Listbox(window, selectmode=tk.SINGLE)
for sheet in sheet_names:
    sheetBox.insert(tk.END, sheet)
sheetBox.pack()


file_label = tk.Label(window, text="No file selected")
file_label.pack()


# Create the dropdown menus for x-axis, y-axis, and filter options
x_label = tk.Label(window, text="xName:")
x_label.pack()
x_var = tk.StringVar(window)
x_dropdown = tk.OptionMenu(window, x_var, *options)
x_dropdown.pack()

y_label = tk.Label(window, text="yName:")
y_label.pack()
y_var = tk.StringVar(window)
y_dropdown = tk.OptionMenu(window, y_var, *options)
y_dropdown.pack()

filter_label = tk.Label(window, text="filterName:")
filter_label.pack()
filter_listbox = tk.Listbox(window, selectmode=tk.MULTIPLE)
for option in options:
    filter_listbox.insert(tk.END, option)
filter_listbox.pack()

filter_range_label = tk.Label(window, text="filterRanges (comma-separated):")
filter_range_label.pack()
filter_range_entry = tk.Entry(window)
filter_range_entry.pack()



# Create the button to plot the graph
plot_button = tk.Button(window, text="Plot Graph", command=plotGraph)
plot_button.pack()

# Start the GUI event loop
window.mainloop()