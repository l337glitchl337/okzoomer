### Zoom Recording downloader
### written by BJH
### 09/05/2021

import requests
import jwt
import time
import datetime
import os
import re
import dotenv
import logging

class Zoom:

    def __init__(self):

        dotenv.load_dotenv()
        logging.basicConfig(filename="info.log", level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        self.email_suffix = os.getenv("EMAIL_SUFFIX")
        self.key = os.getenv("API_KEY")
        self.secret = os.getenv("API_SEC")
        self.directory = os.getenv("DOWNLOAD_DIRECTORY")
        self.session = requests.session()
        self.payload = {
            'iss' : self.key,
            'exp' : time.time() + 8000000
            }
        self.jwt_token = jwt.encode(payload=self.payload, key=self.secret) #generate a JWT token to include in the authorization header
        self.headers = {
            "Authorization": f"Bearer {self.jwt_token}"
        }
        self.emails = []
        self.start_time = datetime.datetime.now().strftime("%m-%d-%Y @ %I:%M:%S %p")
        logging.info(f"Script start time: {self.start_time}")

    def get_recordings(self):
        try:
            if not os.path.exists("lastran.txt"):
                with open("lastran.txt", "w") as f:
                    pass
            else:      
                with open("lastran.txt", "r") as f: #opens up the lastran file to check to see when the last time the script was ran
                lastran = f.read().strip()
                if lastran == "":
                    lastran = "2022-01-01"
                f.close()
        except Exception as e:
            logging.error(e)
        

        for email in self.emails:
            if not os.path.exists(f"{self.directory}/{email.replace(self.email_suffix, '')}"): #create a directory for user if one does not exist
                os.mkdir(f"{self.directory}/{email.replace(self.email_suffix, '')}")
            retry = 0
            
            while True:
                today = datetime.datetime.today().strftime("%Y-%m-%d") #get the current time so we can pass both the lastran time and todays time to the API
                endpoint = f"https://api.zoom.us/v2/users/{email}/recordings"
                params = {
                    "from": f"{lastran}",
                    "to": f"{today}",
                    "page_size": "300"
                }
                r = self.session.get(endpoint, headers=self.headers, params=params)
                try:

                    for meeting in r.json()["meetings"]:
                        for url in meeting["recording_files"]:
                            if url["file_type"] == "MP4":
                                link = url["download_url"]
                                topic = re.sub('[^a-zA-Z0-9 \n\.]', "", meeting["topic"]).replace(" ", "_") #replace all special characters and spaces that would be in the title of the file
                                title = f"{self.directory}/{email.replace(self.email_suffix, '')}/{topic}_{url['recording_start'].replace(':', '-')}.{url['file_type']}" #name the file with full path
                                with self.session.get(link, stream=True) as data:
                                    with open(title, "wb") as f:
                                        for chunk in data.iter_content(chunk_size=8192):
                                            f.write(chunk)
                                logging.info(f"Downloaded {topic} for {email} from {url['recording_start']}")
                except Exception as e:
                    logging.error(e)
                    if retry != 3:
                        logging.info(f"Retrying download for {topic} for {email}")
                        retry += 1
                        continue
                    else:
                        break
                break

        self.log_rundate() #logs new date for this script being ran


    def log_rundate(self): #run this function to record the run date of the script for future runs

        try:
            with open("lastran.txt", "w") as f:
                today = datetime.datetime.today().strftime("%Y-%m-%d")
                f.write(today)
                f.close()
        except Exception as e:
            logging.error(e)
        return
    


    def download_recordings(self): #get instructors emails from the file passed to the function
        file = os.getenv("EMAIL_FILE")
        try:
            with open(file, "r") as f:
                while True:
                    line = f.readline().strip()
                    if line == "":
                        break
                    else:
                        self.emails.append(line)
        except Exception as e:
            logging.error(e)
            return
        self.get_recordings()




if __name__ == "__main__":
    c = Zoom()
    c.download_recordings()
