import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import openpyxl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Set the initial value for excel_file
excel_file_path = ""
sheet_names = []
start = 0
end = 0
increment = 0

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

# Function to update the graph spacing based on user input
def update_graph():
    # Get the values from the entry fields
    start = float(start_entry.get())
    end = float(end_entry.get())
    increment = float(spacing_entry.get())

    # Generate x-axis values using numpy's arange function
    plt.xticks(np.arange(start, end, increment))
    fig.canvas.draw()

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

def get_selected_sheet():
    global selected_sheet, columnOptions
    selected_indices = sheetBox.curselection()
    if selected_indices:
        selected_index = selected_indices[0]
        selected_sheet = sheetBox.get(selected_index)
        print("Selected sheet:", selected_sheet)
        columnOptions = get_sheet_columns(selected_sheet)
        # Update the dropdown menus
        update_dropdown_menus()
    else:
        messagebox.showwarning("Warning", "No sheet selected!")

def update_dropdown_menus():
    x_dropdown['menu'].delete(0, 'end')
    y_dropdown['menu'].delete(0, 'end')
    filter_listbox.delete(0, 'end')

    for option in columnOptions:
        x_dropdown['menu'].add_command(label=option, command=tk._setit(x_var, option))
        y_dropdown['menu'].add_command(label=option, command=tk._setit(y_var, option))
        filter_listbox.insert(tk.END, option)

def update_sheet_box(sheet_names):
    sheetBox.delete(0, tk.END)
    for sheet in sheet_names:
        sheetBox.insert(tk.END, sheet)

def get_sheet_columns(sheet_name):
    if excel_file_path and sheet_name:
        workbook = openpyxl.load_workbook(excel_file_path)
        sheet = workbook[sheet_name]
        columnOptions = [cell.value for cell in sheet[1]]
        workbook.close()
        return columnOptions
    return columnOptions

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

        # Create a Matplotlib canvas
        canvas = FigureCanvasTkAgg(plt.gcf(), master=scroll_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Update the scrollable window to include the canvas
        canvas_width = canvas.get_tk_widget().winfo_width()
        canvas_height = canvas.get_tk_widget().winfo_height()
        canvas.configure(width=canvas_width, height=canvas_height)
        canvas._tkcanvas.pack(fill=tk.BOTH, expand=True)

        # Set the scrollable window to the canvas size
        scroll_window.configure(scrollregion=scroll_window.bbox(tk.ALL))

        # Display the plot
        plt.show()
    else:
        # Display an error message if any of the required fields are not selected
        messagebox.showerror("Error", "Please select all fields.")

# Create the GUI
window = tk.Tk()
window.title("Graph GUI")

# Create a scrollbar
scrollbar = ttk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a scrollable window
scroll_window = tk.Canvas(window, yscrollcommand=scrollbar.set)
scroll_window.pack(fill=tk.BOTH, expand=True)

# Configure the scrollbar to work with the scrollable window
scrollbar.config(command=scroll_window.yview)

# Create the main frame
frame = tk.Frame(scroll_window)
scroll_window.create_window((0, 0), window=frame, anchor=tk.NW)

# Create the button to open the file
open_file_button = tk.Button(frame, text="Open File", command=openFile)
open_file_button.pack()

# Create the button to set the hardcoded path
hardcoded_file_button = tk.Button(frame, text="Hardcoded Data File (brindha)", command=setHardcodedPath)
hardcoded_file_button.pack()

sheetName = tk.Label(frame, text="Select Sheet Name:")
sheetName.pack()
sheetBox = tk.Listbox(frame, selectmode=tk.SINGLE)
for sheet in sheet_names:
    sheetBox.insert(tk.END, sheet)
sheetBox.pack()

processSheet = tk.Button(frame, text="Process Selected Sheet", command=get_selected_sheet)
processSheet.pack()

file_label = tk.Label(frame, text="No file selected")
file_label.pack()

# Create the dropdown menus for x-axis, y-axis, and filter options
x_label = tk.Label(frame, text="xName:")
x_label.pack()
x_var = tk.StringVar(frame)
x_dropdown = tk.OptionMenu(frame, x_var, *options)
x_dropdown.pack()

y_label = tk.Label(frame, text="yName:")
y_label.pack()
y_var = tk.StringVar(frame)
y_dropdown = tk.OptionMenu(frame, y_var, *options)
y_dropdown.pack()

filter_label = tk.Label(frame, text="filterName:")
filter_label.pack()
filter_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE)
for option in options:
    filter_listbox.insert(tk.END, option)
filter_listbox.pack()

filter_range_label = tk.Label(frame, text="filterRanges (comma-separated):")
filter_range_label.pack()
filter_range_entry = tk.Entry(frame)
filter_range_entry.pack()

# Feature to change spacing on graph x-axis
spacing_frame = tk.Frame(frame)
spacing_frame.pack()

start_label = tk.Label(spacing_frame, text="Start value:")
start_label.pack()
start_entry = tk.Entry(spacing_frame)
start_entry.pack()

end_label = tk.Label(spacing_frame, text="End value:")
end_label.pack()
end_entry = tk.Entry(spacing_frame)
end_entry.pack()

spacing_label = tk.Label(spacing_frame, text="Spacing:")
spacing_label.pack()
spacing_entry = tk.Entry(spacing_frame)
spacing_entry.pack()

update_button = tk.Button(spacing_frame, text="Apply Spacing", command=update_graph)
update_button.pack()

# Create the button to plot the graph
plot_button = tk.Button(frame, text="Plot Graph", command=plotGraph)
plot_button.pack()

# Start the GUI event loop
window.mainloop()
