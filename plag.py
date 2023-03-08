import os
from collections import defaultdict
from dataclasses import dataclass, field

@dataclass
class SameCode:
    code: str
    file_name: str
    students: list = field(default_factory=list)
    copies: int = field(default_factory=int)


CLUSTER_THRESH = 2


def create_submission_name_map(metadata_file: str = 'HW3_ID.csv') -> dict:
    """
    Creates a map of submission_id and student name from submission metadata file
    """

    with open(metadata_file) as infile:
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

    return data_dict
    
def _lstrip_lines(lines: str):
    """
    - Gets rid of all the initial lines that starts with # 
    - Once code line starts, it does not strip any more lines
    """
    new_lines = []
    idx = 0
    lines_list = lines.strip().split("\n")
    for line in lines_list:
        
        if line.strip().startswith("#"):
            idx += 1
        else:
            break
    lines_list = lines_list[idx:]
    return " ".join(lines_list)
        


def create_same_code_clusters() -> list[SameCode]:
    """
    Parses through all the code files and creates a SameCode dataclass for every unique code (after stripping)
    All the SameCode dataclass is returned in a list
    """
    cluster_dict : dict[str, SameCode] = {}
    data_dict = create_submission_name_map()
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
                with open(file_path) as file:
                    file_str = file.read().strip()
                    file_str = _lstrip_lines(file_str)
                    print(f"{file_str=}")
                    if file_str not in cluster_dict:
                        same_code_obj = SameCode(code=file_str, file_name=file_name)
                        cluster_dict[file_str] = same_code_obj

                    else:
                        same_code_obj = cluster_dict[file_str]

                    same_code_obj.copies += 1
                    same_code_obj.students.append(student_name)

            except IsADirectoryError:
                continue
    return list(cluster_dict.values())


def filter_same_code_cluster_and_format_lines(same_code_cluster: list[SameCode]) -> list[str]:
    """
    filter the same_code_obj objects based off the clustering threshold and format lines
    """

    
    lines = []
    for same_code_obj in same_code_cluster:
        if same_code_obj.copies >= CLUSTER_THRESH:
            line = f"{same_code_obj.file_name},{' & '.join(same_code_obj.students)}\n"
            lines.append(line)

    return lines

def main():
    same_code_cluster : list[SameCode] = create_same_code_clusters()
    lines : list = filter_same_code_cluster_and_format_lines(same_code_cluster)
    outfile = "output.csv"
    with open(outfile, "w") as fobj:
        fobj.write("problem_name,student_names\n")
        fobj.writelines(lines)


if __name__ == "__main__":
    main()



