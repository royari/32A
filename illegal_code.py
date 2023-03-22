
""" 
Search for illegal imports and functions in submissions

Before running this script:

1. export the submissions from gradescope
2. unzip and directory and rename it to `submissions`
3. export the grades from gradescope
3. delete all the columns except first name, last name, submission_id
4. save the file as 'HW3_ID.csv'
5. run this script
"""
#%%
import os
import re
from collections import defaultdict
from dataclasses import dataclass, field

CSV_SEARCH_STR = "import "
MAIN_SEARCH_STR = "__name__"


@dataclass
class CodeSubmission:
    code: str
    file_name: str
    student: str
    has_main: bool = False
    imports: list = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.student},{self.file_name},{' '.join(self.imports)},{self.has_main}\n"





def print_init_message():
    msg = """\ 
    ######################################################################
    1. Export the submissions from gradescope
    2. Unzip and directory and rename it to `submissions`
    3. Export the grades from gradescope
    3. Delete all the columns except first name, last name, submission_id
    4. Save the file as 'HW3_ID.csv'
    5. Run this script
    ######################################################################
    """
    print(msg)



def create_submission_name_map(metadata_file: str = 'HW3.csv') -> dict:
    """
    Creates a map of submission_id and student name from submission metadata file
    """

    with open(metadata_file) as infile:
        line = infile.readline()
        data_dict = {}

        for line in infile:
            line = line.strip()
            data_list = line.split(',')
            status = data_list[7]
            if status.lower() == "missing":
                continue
            ID = data_list[8]
            first_name = data_list[0]
            last_name = data_list[1]
            name = first_name + " " + last_name
            data_dict[ID] = name

    return data_dict
    

def search_file(file_str: str) -> tuple[bool]:
    imports = []
    has_main = False
    match = re.search("import (\w+)", file_str)

    if match:
        imports = list(match.groups())
    
    if MAIN_SEARCH_STR in file_str:
        has_main = True
    return (imports, has_main)




def create_submission_objects(hw_name: str) -> list[CodeSubmission]:
    """
    Parses through all the code files and looks for the search string
    """

    submissions : list[CodeSubmission] = []
    data_dict = create_submission_name_map(hw_name+".csv")
    submissions_directory = "./submissions"
    for pathname in os.listdir(submissions_directory):
        if pathname == '.DS_Store' or pathname == 'submission_metadata.yml':
            continue
        dirname = os.path.basename(pathname)

        _, fileID = dirname.split('_')
        student_name = str(data_dict.get(fileID))
        for submission_file in os.listdir(os.path.join(submissions_directory, pathname)):
            file_name = os.path.basename(submission_file)
            file_path = os.path.join(submissions_directory,pathname,submission_file)

            try:
                with open(file_path, encoding="utf8", errors='ignore') as file:
                    file_str = file.read().strip()

                    submission_obj : CodeSubmission = CodeSubmission(code=file_str, file_name=file_name, student=student_name)
                    submission_obj.imports, submission_obj.has_main = search_file(file_str)

                    submissions.append(submission_obj)

            except IsADirectoryError:
                continue
    return submissions

def filter_guilty_submissions(subs: list[CodeSubmission]) -> list[str]:
    guilty_list = []
    for sub in subs:
        if sub.imports or sub.has_main:
            guilty_list.append(str(sub))

    return guilty_list


def main():
    print_init_message()
    hw_name = "HW5"
    submissions_obj_list = create_submission_objects(hw_name)
    lines = filter_guilty_submissions(submissions_obj_list)


    outfile = f"{hw_name}imports.csv"
    with open(outfile, "w") as fobj:
        fobj.write("student_name,file_name,imports,__name__=='__main__'\n")
        fobj.writelines(lines)


if __name__ == "__main__":
    main()
# %%