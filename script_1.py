

'''import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import tkinter as tk

excel_file_path = "/Users/brindha/Downloads/movandiData.xlsx"



def plotGraph(xName, yName,filterName):
    df = pd.read_excel(excel_file_path, sheet_name="EVM", engine="openpyxl")

    filter_range = range(30)
    filtered_dfs = []
    plot_data = []

    for filter_value in filter_range:
        filtered_df = df[df[filterName] == filter_value]
        filtered_dfs.append(filtered_df)

    plt.grid(True)  # Add gridlines

    for filtered_df in filtered_dfs:
        new_df = filtered_df[[xName, yName]]
        xpoints = new_df[xName].values
        ypoints = new_df[yName].values
        plot_data.append((xpoints, ypoints))
        plt.plot(xpoints, ypoints)
        #plt.scatter(xpoints, ypoints, s=30)

        x_ticks = np.linspace(min(xpoints), max(xpoints), num=30)
        plt.grid()
        plt.xlabel(xName)
        plt.ylabel(yName)
        plt.title("Graph of " + xName + " vs " + yName)
        plt.xticks(rotation='vertical')
        plt.ylim(0, 60)

    plt.legend([f"{i}" for i in range(len(filtered_dfs))], loc='center left', bbox_to_anchor=(1, 0.5))

    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script_1.py xName yName filterName")
    else:
        xName = sys.argv[1]
        yName = sys.argv[2]
        filterName = sys.argv[3]
        plotGraph(xName, yName, filterName)'''

'''if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--xName", help="Value for xName")
    parser.add_argument("-y", "--yName", help="Value for yName")
    parser.add_argument("-f", "--filterName", help="Value for filterName")
    args = parser.parse_args()

    xName = args.xName
    yName = args.yName
    filterName = args.filterName

    plotGraph(xName, yName, filterName)'''

        

#x --> "Pout_casc[dBm]"
#y --> Gain[dB]
#filter --> MV2650B0_gain_idx

#to run from command lines: python graph_plotter.py "Pin_casc[dBm]" "Gain[dB]" "MV2650B0_gain_idx"
#can also use:

#this is changed
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import OptionMenu, messagebox

excel_file_path = "/Users/brindha/Downloads/movandiData.xlsx"

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
            start, end = map(int, filter_range.split("-"))
            parsed_ranges.append(list(range(start, end + 1)))
        else:
            parsed_ranges.append([int(filter_range)])
    return parsed_ranges

def plotGraph():
    xName = x_var.get()
    yName = y_var.get()
    filterNames = filter_var.get()
    filterRanges = parse_filter_ranges(filter_range_entry.get().split(","))

    if xName and yName and filterNames and filterRanges:
        if len(filterNames) != len(filterRanges):
            messagebox.showerror("Error", "Number of filter names and ranges should match.")
            return

        df = pd.read_excel(excel_file_path, sheet_name="EVM", engine="openpyxl")

        filtered_dfs = []
        plot_data = []

        for filterName, filterRange in zip(filterNames, filterRanges):
            filter_dfs = []
            for filter_value in filterRange:
                filtered_df = df[df[filterName] == filter_value]
                filter_dfs.append(filtered_df)

            filtered_dfs.append(filter_dfs)

        plt.grid(True)  # Add gridlines

        for filter_dfs in filtered_dfs:
            for filtered_df in filter_dfs:
                new_df = filtered_df[[xName, yName]]
                xpoints = new_df[xName].values
                ypoints = new_df[yName].values
                plot_data.append((xpoints, ypoints))
                plt.plot(xpoints, ypoints)

                x_ticks = np.linspace(min(xpoints), max(xpoints), num=30)
                plt.grid()
                plt.xlabel(xName)
                plt.ylabel(yName)
                plt.title("Graph of " + xName + " vs " + yName)
                plt.xticks(rotation='vertical')
                plt.ylim(0, 60)

        plt.legend([f"Filter {i+1}" for i in range(len(filtered_dfs))], loc='center left', bbox_to_anchor=(1, 0.5))

        plt.show()
    else:
        messagebox.showerror("Error", "Please select all fields.")

# Create the GUI
window = tk.Tk()

# Create the dropdown menus
x_label = tk.Label(window, text="xName:")
x_label.pack()
x_var = tk.StringVar(window)
x_dropdown = OptionMenu(window, x_var, *options)
x_dropdown.pack()

y_label = tk.Label(window, text="yName:")
y_label.pack()
y_var = tk.StringVar(window)
y_dropdown = OptionMenu(window, y_var, *options)
y_dropdown.pack()

filter_label = tk.Label(window, text="filterName:")
filter_label.pack()
filter_var = tk.StringVar(window)
filter_dropdown = OptionMenu(window, filter_var, *options, multiple=True)
filter_dropdown.pack()

filter_range_label = tk.Label(window, text="filterRanges (comma-separated):")
filter_range_label.pack()
filter_range_entry = tk.Entry(window)
filter_range_entry.pack()

# Create the button to plot the graph
plot_button = tk.Button(window, text="Plot Graph", command=plotGraph)
plot_button.pack()

# Start the GUI event loop
window.mainloop()

