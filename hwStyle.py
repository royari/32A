"""

Concatinate student submissions from the `submissions` directory 
and copy it to the `result` directory where each file is named after the student


Before running this script:

1. export the submissions from gradescope
2. unzip and directory and rename it to `submissions`
3. export the grades from gradescope
4. save the grades file as 'HW4.csv' or equivalent
5. Updtate the varibles in script (csv file name, hw python files)
6. run this script
"""
#%%
import os 
from shutil import copyfile

 
# Function to rename multiple files 
def main(): 

    infile = open('HW5.csv') # update this for every file
    line = infile.readline()
    data_dict = {}
    for line in infile:
        line = line.strip()
        data_list = line.split(',')
        first_name = data_list[0]
        last_name = data_list[1]
        name = first_name + " " + last_name
        status = data_list[7]
        if status.lower() == "missing":
            continue
        ID = data_list[8]
        data_dict[ID] = name
        
    if not os.path.exists("./result"):
        os.makedirs("result")
        print("created a new directory: result")
    # Update this list with all the files names of the hw
    files = ["read_temp_file.py", "temp_list.py", "first_ave.py", "moving_ave.py", "moving_ave_csv.py", "plot_moving_ave.py"]
    for pathname in os.listdir("./submissions"):
        if pathname == '.DS_Store':
            continue
        dirname = os.path.basename(pathname)

        fileID = dirname.split('_')
        fileID = fileID[1]
        dst = str(data_dict.get(fileID))
    

        output_file_str = ""
        for file in files:
            if os.path.isfile(os.path.join("./submissions",dirname,file)):
                with open(os.path.join("./submissions",dirname,file)) as fobj:
                    fobj_str = fobj.read()
                    output_file_str += f"\n{fobj_str}"

        with open(os.path.join("./result", dst + ".py"), "w") as fobj:
            fobj.write(output_file_str)

# Driver Code 
if __name__ == '__main__': 
      
    main()

# %%

