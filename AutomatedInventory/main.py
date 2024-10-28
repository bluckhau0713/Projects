import pandas as pd
import graph
import log

# graph is a py file that is used to modularize the talking to MS Graph API
graph.getDevices()
graph.unzipFolder()

logger = log.Logger()

def mergeDataframes(asset, serialsFromIntune):
    columnIndexesInInventory = dict()
    columnIndexesInAsset = dict()
    # get the column index numbers to reduce searching
    for column in columnsToAdd:
        columnIndexesInInventory[column] = newInventory.columns.get_loc(column)
        columnIndexesInAsset[column] = asset.columns.get_loc(column)

    for serial in serialsFromIntune:
        try:    # Serial is in asset tag list
            assetRow = list(asset["Serial"]).index(serial)                  # what row in AssetTags.xlsx is the serial number at
            intuneRow = list(newInventory["Serial number"]).index(serial)   # what row in the newInventory dataframe is the serial number at
            newInventory.iat[intuneRow, 0] = asset.iat[assetRow, 0]         # add the asset tag to the new df

            for column in columnsToAdd:     # adds the remaining columns in AssetTags.xlsx without having to search each time
                newInventory.iat[intuneRow, columnIndexesInInventory[column]] = asset.iat[assetRow, columnIndexesInAsset[column]]
        except Exception as e:  # Serial is not in asset tag list, so leave it blank
            print(e)
            logger.addToLog(e)


# any columns added after "Serial" should be added automatically
assetColumns = ["Asset Tag", "Serial", "Purchase Date", "Notes"]
columnsToAdd = assetColumns[2:]     # used to automatically add later columns

intuneColumns = ["Device name", "Last check-in", "Serial number", "Manufacturer", "Model", "Wi-Fi MAC", "Total storage",
                 "Free storage", "Primary user display name"]

# read the two files needed
assetInventory = pd.read_excel("//netdrives/ITinventory/AssetTags.xlsx", usecols=assetColumns)
intuneInventory = pd.read_csv("C:/PythonScripts/Inventory/IntuneReports/csvs/DevicesWithInventory.csv", usecols=intuneColumns)

newInventory = intuneInventory.copy(deep=True)

# Add the columns to the inventory, so they can be written to later
for column in assetColumns:
    if column == "Asset Tag":
        newInventory.insert(0, "Asset tag", pd.Series(dtype='object'))
    elif column == "Serial":
        continue
    else:
        # Add new columns automatically
        newInventory[column] = pd.Series(dtype='object')


mergeDataframes(assetInventory, intuneInventory["Serial number"])

newInventory = newInventory.sort_values('Asset tag', ascending=True)

# create the inventory files for the user's reading pleasure
try:
    newInventory.to_excel("//netdrives/ITinventory/AutomaticInventory.xlsx", index=False)
    print("File created on K drive")
    logger.addToLog("File created on K drive")
except Exception as e:
    print(f"Failed to create file on K drive due to: {e}")
    logger.addToLog("Failed to create file on K drive due to: {e}")

logger.writeFile("C:/ScriptLogs/inventoryLog.txt")
