#!/usr/bin/env python3
"""
Before running the script
1. updated csv file name 
2. course id and assignment id variables
"""
#%%
import requests
import getpass
import os 
from shutil import copyfile

BASE_URL = 'https://www.gradescope.com'

class APIClient:
    def __init__(self):
        self.session = requests.Session()

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def log_in(self, email, password):
        url = "{base}/api/v1/user_session".format(base=BASE_URL)

        form_data = {
            "email": email,
            "password": password
        }
        r = self.post(url, data=form_data)

        self.token = r.json()['token']

    def upload_pdf_submission(self, course_id, assignment_id, student_email, filename):
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions".format(
            course_id, assignment_id, base=BASE_URL
        )

        form_data = {
            "owner_email": student_email
        }
        files = {'pdf_attachment': open(filename, 'rb')}

        request_headers = {'access-token': self.token}
        r = self.post(url, data=form_data, headers=request_headers, files=files)
        return r

    def replace_pdf_submission(self, course_id, assignment_id, student_email, filename):
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions/replace_pdf".format(
            course_id, assignment_id, base=BASE_URL
        )

        form_data = {
            "owner_email": student_email
        }
        files = {'pdf_attachment': open(filename, 'rb')}

        request_headers = {'access-token': self.token}
        r = self.post(url, data=form_data, headers=request_headers, files=files)
        return r

    def upload_programming_submission(self, course_id, assignment_id, student_email, filenames):
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions".format(
            course_id, assignment_id, base=BASE_URL
        )

        form_data = {
            "owner_email": student_email
        }
        files = [('files[]', (filename, open(filename, 'rb'))) for filename in filenames]

        request_headers = {'access-token': self.token}
        r = self.post(url, data=form_data, headers=request_headers, files=files)
        # print(f"{r=} {r.content} {r.text}")
        return r
    
    

if __name__ == '__main__':
    client = APIClient()
    #email = input("Please provide the email address on your Gradescope account: ")
    email = 'aroy@ucdavis.edu'
    password = getpass.getpass('Password: ')
    client.log_in(email, password)
    # Use the APIClient to upload submissions after logging in, e.g:
    # client.upload_pdf_submission(66777, 309912, '841154914@qq.com', 'LTE_OUR_2.pdf')


    
    infile = open('HW4.csv') # update this for HWs 
    line = infile.readline()
    data_dict = {}
    for line in infile:
        line = line.strip()
        data_list = line.split(',')

        status = data_list[7]
        if status.lower() == "missing":
            continue

        first_name = data_list[0]
        last_name = data_list[1]
        name = first_name + " " + last_name
        std_email = data_list[3]
        data_dict[name] = std_email
        
    for pathname in os.listdir("./result"):
        if pathname == '.DS_Store':
            continue
        pathname1 = pathname.split('.')
        name = pathname1[0]
        course_id = 475090
        assignment_id = 2746893
        client.upload_programming_submission(course_id, assignment_id, data_dict.get(name), ['./result/'+name+'.py'])
            
    # You can get course and assignment IDs from the URL, e.g.
    # https://www.gradescope.com/courses/1234/assignments/5678
    # course_id = 1234, assignment_id = 5678


# %%
