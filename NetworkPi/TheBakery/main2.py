import retrieveFiles
import createVideo
import createFigures
import log

logger = log.Logger()
colors = {'totalClients': 'palegreen',
          'QUCONSOLES': '#d1f7ff', 'QUGuest': 'slateblue', 'QUINCY': 'cornflowerblue',
          'border': '#ff2a6d',
          'font': '#05f9ff', 'background': '#01012b',
          'deniedPackets': 'lightcoral', 'allowedPackets': 'palegreen', 'reset-both': 'tan',
          'water': '#00bce1', 'land': 'darkgreen', 'source': 'yellow', 'destination': 'pink', 'both': 'magenta',
          'gauge': 'lightcoral',
          'buildings': 'palegreen'}

try:
    # bandwidthColumns = ["Action", "Receive Time", "Session ID", "Bytes", 'Source Country', 'Destination Country']
    bandwidth = retrieveFiles.retrieveFirewallLogs()
    # bandwidth.to_csv("fwlogs.csv")
    # bandwidth["Receive Time"] = pd.to_datetime(bandwidth["Receive Time"])
    paLogs = True
    print("Done reading bandwidth logs")
    logger.addToLog("Done reading bandwidth logs")
except Exception as e:
    paLogs = False
    print("No PA logs csv at location: ./csvs/pa_logs.csv")
    logger.addToLog(f"No PA logs csv at location: ./csvs/pa_logs.csv: {e}")
    print(e)

if paLogs:
    try:
        createFigures.packetAction(bandwidth, colors)
        print("done with packetAction")
        logger.addToLog("Done with packetAction")
    except Exception as e:
        print("Error in packetAction")
        logger.addToLog(f"Error in packetAction: {e}")
        print(e)
    try:
        createVideo.worldVideo(bandwidth, colors)
        print('done with world video')
        logger.addToLog("Done with world video")
    except Exception as e:
        print('Error in world video')
        logger.addToLog(f"Error in world video: {e}")
        print(e)
    try:
        createVideo.video(bandwidth, colors)
        print("done with video")
        logger.addToLog("Done with video")
    except Exception as e:
        print("Error in video")
        logger.addToLog(f"Error in video: {e}")
        print(e)

logger.writeFile("C:/ScriptLogs/firewallLog.txt")
