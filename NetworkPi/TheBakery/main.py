import createFigures
import retrieveFiles
import pandas as pd
import log

logger = log.Logger()

try:
    retrieveFiles.retrieveAirwaveLogs()
    print("Airwave logs retrieved")
    logger.addToLog("Airwave logs retrieved")
except Exception as e:
    # retrieveFiles.cleanFolder()
    print("Error retrieving Airwave Logs")
    logger.addToLog(f"Error retrieving Airwave Logs: {e}")
    logger.addToLog(e)

# colors = {'totalClients': 'blue',
#           'QUCONSOLES': 'aqua', 'QUGuest': 'olive', 'QUINCY': 'cornflowerblue',
#           'border': 'white',
#           'font': 'white', 'background': 'black',
#           'deniedPackets': 'indianred', 'allowedPackets': 'seagreen', 'reset-both': 'tan',
#           'water': 'dodgerblue', 'land': 'forestgreen', 'source': 'yellow', 'destination': 'pink', 'both': 'magenta',
#           'gauge': 'red',
#           'buildings': 'slateblue'}

# Cyber-punk theme
colors = {'totalClients': 'palegreen',
          'QUCONSOLES': '#d1f7ff', 'QUGuest': 'slateblue', 'QUINCY': 'cornflowerblue',
          'border': '#ff2a6d',
          'font': '#05d9e8', 'background': '#01012b',
          'deniedPackets': 'lightcoral', 'allowedPackets': 'lightgreen', 'reset-both': 'tan',
          'water': '#00bce1', 'land': 'darkgreen', 'source': 'yellow', 'destination': 'pink', 'both': 'magenta',
          'gauge': 'lightcoral',
          'buildings': 'palegreen'}

try:
    usage = pd.read_csv("C:/PythonScripts/NetworkPi/csvs/usage_by_ssid.csv")
    ssidExists = True
    print("Done reading usage logs")
    logger.addToLog("Done reading usage logs")
except Exception as e:
    ssidExists = False
    print("No usage csv at location: csvs/usage_by_ssid.csv")
    logger.addToLog(f"No usage csv at location: csvs/usage_by_ssid.csv: {e}")
    print(e)
try:
    usageBuilding = pd.read_csv("C:/PythonScripts/NetworkPi/csvs/total_usage_by_folder.csv")
    buildingExists = True
    print("Done reading folder usage logs")
    logger.addToLog("Done reading folder usage logs")
except Exception as e:
    buildingExists = False
    print("No usage csv at location: csvs/total_usage_by_folder.csv")
    logger.addToLog(f"No usage csv at location: csvs/total_usage_by_folder.csv: {e}")
    print(e)
if ssidExists:
    try:
        usageBySSID, usageBySSIDClients = createFigures.usageOverTime(usage, colors)
        print("done with usageOverTime")
        logger.addToLog("Done reading usageOverTime logs")
    except Exception as e:
        print("Error in usageOverTime")
        logger.addToLog(f"Error in usageOverTime: {e}")
        print(e)
    try:
        createFigures.clientsEverySixty(usageBySSID, usageBySSIDClients, colors)
        print("done with clientsEverySixty")
        logger.addToLog("Done reading clientsEverySixty logs")
    except Exception as e:
        print("Error in clientsEverySixty")
        logger.addToLog(f"Error in clientsEverySixty: {e}")
        print(e)
    try:
        createFigures.usageByPie(usageBySSID, colors)
        print("done with usageByPie")
        logger.addToLog("Done reading usageByPie logs")
    except Exception as e:
        print("Error in usageByPie")
        logger.addToLog(f"Error in usageByPie: {e}")
        print(e)
if buildingExists:
    try:
        createFigures.usageByBuilding(usageBuilding, colors)
        print("done with usageByBuilding")
        logger.addToLog("Done reading usageByBuilding logs")
    except Exception as e:
        print("Error in usageByBuilding")
        logger.addToLog(f"Error in usageByBuilding: {e}")
        print(e)

logger.writeFile("C:/ScriptLogs/airwaveLog.txt")