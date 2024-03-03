import requests
import os

base_url = 'http://localhost:8080/'

base_path = os.path.join(os.getcwd(), 'downloaded_files')
file = 'abc.txt'
get_file_url = "{base_url}file/{filename}".format(base_url=base_url, filename=file)
result = requests.get(get_file_url)
if result.text != "KO":
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    path = os.path.join(base_path, file)
    if os.path.exists(path):
        os.remove(path)
    print("downloading file to %s" %path)

    with open(path, 'a') as f:
        f.write(result.text)

else:
    print("file not found on server")
    
