import pandas as pd
import requests
import time
import zipfile
import os
import glob
import shutil


def unzip_folder(zip_file_path, extract_to_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)


def cleanFolder():
    files = os.listdir("./csvs/PiReports/")
    for file in files:
        os.remove(f"csvs/PiReports/{file}")


def modifyAirwaveZip():
    zip_file_pattern = '//transporter/PiReporting/PiReports*.zip'
    extract_to_path = 'C:/PythonScripts/NetworkPi/csvs/'

    # Find the zip file with the specified pattern
    zip_file_path = glob.glob(zip_file_pattern)[0]  # Assumes there is only one matching file

    unzip_folder(zip_file_path, extract_to_path)

    os.remove(glob.glob(zip_file_pattern)[0])

    newCsv = glob.glob('C:/PythonScripts/NetworkPi/csvs/PiReports/usage_by_ssid_*.csv')[0]
    replaceCsv = 'C:/PythonScripts/NetworkPi/csvs/usage_by_ssid.csv'

    shutil.move(newCsv, replaceCsv)

    newBuilding = glob.glob('C:/PythonScripts/NetworkPi/csvs/PiReports/total_usage_by_folder_*.csv')[0]
    replaceBuilding = 'C:/PythonScripts/NetworkPi/csvs/total_usage_by_folder.csv'

    shutil.move(newBuilding, replaceBuilding)


def retrieveFirewallLogs():
    username = 'user'
    password = 'pass'

    url = f"url"

    payload = {
        'user': username,
        'password': password,
        'type': 'keygen'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=payload, headers=headers, verify=False)

    keyStart = response.text.index("y>") + 2
    keyEnd = response.text.index("<", keyStart)

    key = response.text[keyStart:keyEnd]

    query = f"?type=report&async=yes&reporttype=custom&reportname=PiReporting&key={key}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {username}:{password}'
    }

    response = requests.post(url=url + query, headers=headers, verify=False)

    jobIDStart = response.text.index("<job>") + 5
    jobIDEnd = response.text.index("</", jobIDStart)
    jobID = response.text[jobIDStart:jobIDEnd]

    time.sleep(10)

    jobQuery = f"?key={key}&type=report&action=get&job-id={jobID}"
    response = requests.post(url=url + jobQuery, headers=headers, verify=False)

    # Extract data from XML and store in a list of dictionaries
    data = []
    xml = response.text
    while True:
        entry_data = {}
        entry_data['Receive Time'] = xml[xml.index('time_generated>') + 15: xml.index('</time')]

        tempIndex = xml.index('>', xml.index('code')) + 1
        entry_data['Destination Country'] = xml[tempIndex: xml.index('<', tempIndex)]

        tempIndex = xml.index('>', xml.index('code', tempIndex)) + 1
        entry_data['Source Country'] = xml[tempIndex: xml.index('<', tempIndex)]

        entry_data['Session ID'] = xml[xml.index('sessionid>') + 10: xml.index('</sessionid')]

        entry_data['Action'] = xml[xml.index('action>') + 7: xml.index('</action')]

        entry_data['Bytes'] = xml[xml.index('bytes>') + 6: xml.index('</byt')]
        data.append(entry_data)
        # counter += 1
        try:
            xml = xml[xml.index('entry', xml.index('/entry') + 6):]
        except Exception as e:
            print(e)
            break

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(data)

    df = df.sort_values(by='Receive Time', ascending=False)
    df['Bytes'] = df['Bytes'].astype(int)
    df['Receive Time'] = pd.to_datetime(df['Receive Time'])

    return df


def retrieveAirwaveLogs():
    # hostname = 'host'
    # port = 22
    # username = 'user'
    # password = 'pass'
    #
    # ssh = paramiko.SSHClient()
    #
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #
    # ssh.connect(hostname, port, username, password)
    #
    # sftp = ssh.open_sftp()
    #
    # remote_file_path = ".\\"
    # try:
    #     remote_files = sftp.listdir(remote_file_path)
    #     for remote_file in remote_files:
    #         local_file_path = "./csvs/"
    #         local_file_path += remote_file
    #         remote_file_path = remote_file
    #         sftp.get(remote_file_path, local_file_path)
    #         sftp.remove(remote_file)
    # except Exception as e:
    #     print("No file at location on remote computer")
    #     print(e)
    # sftp.close()
    # ssh.close()

    modifyAirwaveZip()

# cleanFolder()
# retrieveAirwaveLogs()
