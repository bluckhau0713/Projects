import paramiko
import datetime
import getLists
import pandas as pd
import checkWhatCommand
import subprocess
import python_weather
import asyncio
import os


def command_getRoomAvailability(dbCursor, buildingCode, day, room):

    response = getRoomHours(dbCursor, building=buildingCode, day=day, room=room)
    # print(response)
    return getAvailability(response, buildingCode, room)


def command_getWhatsForLunch(phrase, days):
    day = checkWhatCommand.extractDay(phrase,days)
    column = [day]
    menu = pd.read_excel("C:/Users/luckhbr/Desktop/Fall 2024 Cycle Menu V2 AG.xls", skiprows=2,
                         sheet_name=f"Cycle {getLists.getCycle()}", usecols=column)
    menu = menu.dropna()
    return f"According to the VIP menu, {cleanMenu(menu).str.cat(sep=', ')}"


def command_sendFanControl(control):
    hostname = "secretIP"
    username = "secretUsername"
    password = "secretPassword"
    command = f"python3 /home/pi/Desktop/ArduinoPi/voiceFans.py {control}"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the Raspberry Pi
        ssh.connect(hostname, username=username, password=password)
        # Execute the command
        ssh.exec_command(command)
    finally:
        # Close the connection
        ssh.close()


def command_unlockJulieFischer():
    try:
        script = "//netdrives/ITServices/Scripts and Code/Powershell/unlockJulieFisher.ps1"
        process = subprocess.Popen(["powershell", "-File", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        result = stdout.decode('utf-8')
        error = stderr.decode('utf-8')
    except:
        return "Could not unlock Julie Fischer"
    return "Julie Fischer is now unlocked"


def command_syncAzure():
    try:
        script = "//netdrives/ITServices/Scripts and Code/Powershell/Computer Management/DoAzureSync.ps1"
        process = subprocess.Popen(["powershell", "-File", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        result = stdout.decode('utf-8')
        error = stderr.decode('utf-8')
        script = "//netdrives/ITServices/Account Management/Account Creation/Google Sync for Account Creation.ps1"
        process = subprocess.Popen(["powershell", "-File", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        result = stdout.decode('utf-8')
        error = stderr.decode('utf-8')
    except:
        return "Azure is already being synced"
    return "Azure and Google have been synced"


def command_whenMikeTeaches(cursor, day):
    query = f"""
        SELECT

        FORMAT(schedules.BEGIN_TIM, 'HH:mm') as BEGIN_TIME,
        FORMAT(schedules.END_TIM, 'HH:mm') as END_TIME

        FROM

        TmsEPrd.dbo.SECTION_SCHEDULES as schedules

        WHERE
        schedules.PROFESSOR_ID_NUM = '1039182'
        AND
        schedules.YR_CDE LIKE {getLists.getYear()}
        AND
        schedules.TRM_CDE LIKE '{getLists.getTerm()}'
        AND
        {getLists.getClassDate(day)}
        """
    cursor.execute(query)
    rows = cursor.fetchall()

    if len(rows) == 0:
        return f"Mike does not teach today"
    sortedResponse = sorted(rows, key=lambda x: datetime.datetime.strptime(x[0], '%H:%M'))
    now = datetime.datetime.now().strftime("%H:%M")
    for session in sortedResponse:
        if session[0] > now:
            # print(f"Mike teaches at {session[0]}")
            return f"Mike teaches at {session[0]}"
        if session[0] == now or session[1] > now: # > session[0]:
            # print("Uh oh, Mike should be teaching right now!")
            return "Uh oh, Mike should be teaching right now!"
    # print("Mike does not teach for the rest of the day")
    return "Mike is done teaching for the rest of the day"


def command_getWeather():
    async def getWeather():
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            weather = await client.get('quincy illinois')
            return f"It is currently {weather.kind} with {weather.wind_speed} mph wind and it feels like {weather.feels_like} degrees"

    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return asyncio.run(getWeather())


##################################################### INTERNAL USE #####################################################
def getRoomHours(cursor, building, room, day):
    query = f"""
    SELECT
    DISTINCT

    -- schedules.BLDG_CDE,
    -- schedules.ROOM_CDE,
    FORMAT(schedules.BEGIN_TIM, 'HH:mm') as BEGIN_TIME,
    FORMAT(schedules.END_TIM, 'HH:mm') as END_TIME

    FROM

    TmsEPrd.dbo.SECTION_SCHEDULES as schedules

    WHERE
    schedules.BLDG_CDE = '{building}'   AND   -- This is where the speech will come in 
    schedules.ROOM_CDE = '{room}'       AND   -- This is where the speech will come in    
    schedules.YR_CDE LIKE {getLists.getYear()}   AND
    schedules.TRM_CDE LIKE '{getLists.getTerm()}'         AND
    schedules.LOC_CDE NOT LIKE 'WEB'    AND
    schedules.LOC_CDE NOT LIKE 'OFF'    AND
    {getLists.getClassDate(day)}
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def extractFanCommand(phrase, fanModes):
    for mode in fanModes:
        if mode in phrase:
            return mode


def getAvailability(response, building, room):
    if len(response) == 0:
        return f"{building} {room} is free all day, or is not a valid classroom"
    sortedResponse = sorted(response, key=lambda x: datetime.datetime.strptime(x[0], '%H:%M'))
    # print(sortedResponse)
    # print(len(sortedResponse))
    amountOfSessions = len(sortedResponse)

    beginClassCounter = 0
    endClassCounter = 0

    toSpeech = f"{building} {room} is free before {sortedResponse[beginClassCounter][endClassCounter]}"
    endClassCounter = 1
    if amountOfSessions == 1:
        toSpeech += f", and then after {sortedResponse[beginClassCounter][endClassCounter]}"
    else:
        while beginClassCounter < amountOfSessions - 1:
            # print(toSpeech)
            toSpeech += f", and then from {sortedResponse[beginClassCounter][endClassCounter]} to {sortedResponse[beginClassCounter + 1][endClassCounter - 1]}"
            beginClassCounter += 1
        toSpeech += f", and then after {sortedResponse[-1][1]}"
    return toSpeech


def cleanMenu(menu):
    # Find out where LUNCH appears
    start_index = menu.apply(lambda row: row.astype(str).str.contains('LUNCH')).any(axis=1).idxmax() + 1
    # Find out where DINNER appears
    end_index = menu.apply(lambda row: row.astype(str).str.contains('DINNER')).any(axis=1).idxmax() - 1
    filteredMenu = menu.loc[start_index:end_index].reset_index(drop=True)
    filteredMenuSeries = filteredMenu.iloc[:, 0]
    return filteredMenuSeries[filteredMenuSeries != 'GRILL STATION']
