"""

Concatinate student submissions from the `submissions` directory 
and copy it to the `result` directory where each file is named after the student


Before running this script:

1. export the submissions from gradescope
2. unzip and directory and rename it to `submissions`
3. export the grades from gradescope
3. delete all the columns except first name, last name, submission_id
4. save the file as 'HW4_ID.csv' or equivalent
5. Updtate the varibles in script
5. run this script
"""
#%%
import os 
from shutil import copyfile

 
# Function to rename multiple files 
def main(): 
    i = 0
    infile = open('HW4_ID.csv')
    line = infile.readline()
    data_dict = {}
    for line in infile:
        line = line.strip()
        data_list = line.split(',')
        first_name = data_list[0]
        last_name = data_list[1]
        name = first_name + " " + last_name
        ID = data_list[2]
        data_dict[ID] = name
        
    # Update this list with all the files names of the hw
    files = ["parrot.py", "password.py", "phone.py", "extract.py", "translate.py", "cat.py", "cash.py", "cash2.py", "check.py"]
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

