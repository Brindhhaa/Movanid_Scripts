

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

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
        plotGraph(xName, yName, filterName)"""

'''if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--xName", help="Value for xName")
    parser.add_argument("-y", "--yName", help="Value for yName")
    parser.add_argument("-f", "--filterName", help="Value for filterName")
    args = parser.parse_args()

    xName = args.xName
    yName = args.yName
    filterName = args.filterName

    plotGraph(xName, yName, filterName)
        

#x --> "Pout_casc[dBm]"
#y --> Gain[dB]
#filter --> MV2650B0_gain_idx

#to run from command lines: python graph_plotter.py "Pin_casc[dBm]" "Gain[dB]" "MV2650B0_gain_idx"
#can also use: