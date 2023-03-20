from functions import merge

rerun = True
while rerun:
    parent_dir = input("What is the file path of the AMBR data?: ")
    merge.combine_all(parent_dir)
    again = input("Do you have any more data? (Y/N):")
    if again.upper() == 'N':
        rerun = False
