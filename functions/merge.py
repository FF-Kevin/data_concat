def combine_all(parent_dir):
    import os
    import glob
    import pandas as pd
    import re

    # define the parent directory where all CSVs are stored
    parent_dir = parent_dir + "/Data/00001/B"
    # define the file extension for CSV files
    file_extension = ".csv"

    # define the name of the merged CSV file
    merged_file_name = "merged_data.csv"

    # create an empty list to store all dataframes
    dfs = pd.DataFrame()

    # create list of parameters needed in final merge, based on csv file name
    parameterList = "Air flow|Air primary flow_SP|Air volume|Base flow rate\
                    |Base volume pumped|Base volume since reset\
                    |CER|Clamp plate temperature|DO|Off-gas|pH|stir\
                    |Temperature|Total gas|Volume (mL)|Stir speed"

    # loop through all subdirectories and their CSV files and read them into dataframes
    for root, dirs, files in os.walk(parent_dir):

        # cycle through each subfolderfrom given parent directory
        for dir in dirs:
            # make empty dataframe where all the data for each directory will be stored
            df1 = pd.DataFrame(columns=['VariableKey', 'Tank'])
            df1['VariableKey'] = pd.to_datetime(df1['VariableKey'])

            # pull names of all csv files in directory
            csv_files = glob.glob(os.path.join(
                parent_dir, dir, f"*{file_extension}"))

            # check  to see if the directory is empty, if empty then move on to the next one
            if len(csv_files) == 0:
                next
            else:
                for csv_file in csv_files:
                    # search only for csv files in given list
                    if re.search(parameterList, csv_file):
                        try:
                            # turn csv file into a dataframe and create column for tank number to distinguish
                            df = pd.read_csv(csv_file, skiprows=2,
                                             on_bad_lines='skip')
                            df['VariableKey'] = pd.to_datetime(
                                df['VariableKey'])
                            df['Tank'] = dir

                            # merge csv file with empty directory dataframe
                            joinon = list(df1.columns)
                            df1 = df1.merge(df, how='outer', on=[
                                            'VariableKey', 'Tank'])
                        except:
                            print(f"Error reading file: {csv_file}")
                    else:
                        next
            # stack together into final dataframe to be made into csv
            dfs = pd.concat([dfs, df1])

    # turn final dataframe into csv
    dfs.to_csv(os.path.join(parent_dir, merged_file_name), index=False)
    print("Successfully created file: " +
          str(os.path.join(parent_dir, merged_file_name)))
