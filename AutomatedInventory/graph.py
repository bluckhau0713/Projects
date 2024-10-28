import subprocess
import zipfile
import os
import log

logger = log.Logger()


def getDevices():
    logger = log.Logger()
    print("Getting devices from Intune")
    logger.addToLog("Getting devices from Intune")
    script = "C:/PythonScripts/Inventory/getDevices.ps1"

    process = subprocess.Popen(["powershell", "-File", script], stdout=subprocess.PIPE)
    result = process.communicate()[0]

    #print("Result:", result.decode("utf-8"))
    print("Retrieved devices from Intune")
    logger.addToLog("Retrieved devices from Intune")
    logger.writeFile("C:/ScriptLogs/getDevicesLog.txt")

def unzipFolder():
    zip_file_path = "C:/PythonScripts/Inventory/IntuneReports/Devices.zip"
    extract_to_path = "C:/PythonScripts/Inventory/IntuneReports"
    oldFile = ""
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)
    files = os.listdir(extract_to_path)
    for file in files:
        if file.endswith('.csv'):
            oldFile = os.path.join(extract_to_path, file)

    os.remove(f"{extract_to_path}/csvs/DevicesWithInventory.csv")
    os.rename(f"{oldFile}", f"{extract_to_path}/csvs/DevicesWithInventory.csv")

    os.remove(zip_file_path)
