import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MinuteLocator, DateFormatter
from matplotlib.ticker import FuncFormatter
import matplotlib.patches as patches
from _datetime import datetime
import math


def makeFloat(value, _):
    return f"{float(value)}"


def makeInt(value, _):
    return f"{int(value)}"


def convertToBits(speed):
    if speed == '-':    # if speed is 0
        return 0
    value, unit = speed.split()     # split at the space
    value = float(value)
    # print(unit)
    if unit == 'Mbps':
        return value
    elif unit == 'Kbps':    # convert to Mbps
        return value / 1000


def convertDateTime(dateRange):
    startTime, endTime = dateRange.split(' - ')
    startTime = startTime.replace(' CDT', '')   # remove the time zone
    startTime = startTime.replace(' CST', '')  # remove the time zone
    # endTime = endTime.replace(' CST', '')
    startTime = datetime.strptime(startTime, '%m/%d/%Y %I:%M %p')
    # endTime = datetime.strptime(endTime, '%m/%d/%Y %I:%M %p')
    # print(startTime, endTime)
    return startTime


def removeDate(dateTime):
    space = str(dateTime).index(" ")
    return str(dateTime)[space + 1:]


def makeNewDf(usage):
    # dictionaries used to plot the data
    usageBySSID = dict()
    usageBySSIDClients = dict()

    # temporary table to not modify the original
    tempUsage = usage.sort_values(by="Interval")
    tempUsage["Interval"] = tempUsage["Interval"].apply(removeDate)
    counter = 0
    clientCount = 0
    while counter < len(tempUsage["Interval"]):     # while there are still rows
        if not ("Date" in usageBySSID):     # if the timeframe list has not been made, make it
            usageBySSID["Date"] = [tempUsage["Interval"].iloc[counter]]
        elif not (tempUsage["Interval"].iloc[counter] in usageBySSID["Date"]):  # if the timeframe list is made, but the timeframe has not been added, add it
            usageBySSID["Date"] += [tempUsage["Interval"].iloc[counter]]

        if not(tempUsage["SSID"].iloc[counter] in usageBySSID):     # if the SSID does not have a list for usage, make it
            usageBySSID[tempUsage["SSID"].iloc[counter]] = [tempUsage["Max Usage In"].iloc[counter]]
        else:   # the current SSID has a list, so add the usage for that time in the list
            usageBySSID[tempUsage["SSID"].iloc[counter]] += [tempUsage["Max Usage In"].iloc[counter]]

        if not(tempUsage["SSID"].iloc[counter] in usageBySSIDClients):  # if the SSID does not have a list for clients, make it
            usageBySSIDClients[tempUsage["SSID"].iloc[counter]] = [tempUsage["Max Clients"].iloc[counter]]
        else:   # the current SSID has a client list, so add to that list
            usageBySSIDClients[tempUsage["SSID"].iloc[counter]] += [tempUsage["Max Clients"].iloc[counter]]

        if not ("Clients" in usageBySSID):  # no count yet
            usageBySSID["Clients"] = [tempUsage["Max Clients"].iloc[counter]]
        elif clientCount % 3 == 0:  # new client count --> this is possible due to how the file is formatted
            usageBySSID["Clients"] += [tempUsage["Max Clients"].iloc[counter]]
        else:   # not a new client count, so add to the current client amount
            usageBySSID["Clients"][-1] += tempUsage["Max Clients"].iloc[counter]
        counter += 1
        clientCount += 1
    return usageBySSID, usageBySSIDClients


def usageOverTime(usage, colors):
    usage["Max Usage In"] = usage["Max Usage In"].apply(convertToBits)  # standardize to Mbps
    usage["Interval"] = usage["Interval"].apply(convertDateTime)   # convert the string to a dateTime object
    usage = usage.sort_values(by="SSID")

    usageBySSID, usageBySSIDClients = makeNewDf(usage)  # makes two dicts that are used for plotting
    usageBySSID = pd.DataFrame(usageBySSID)     # turns the dict into a pandas dataframe
    usageBySSID = usageBySSID.sort_values(by='Date')

    usageBySSID['Date'] = pd.to_datetime(usageBySSID['Date'], format='%H:%M:%S')    # make the dataframe understand the dateTime format
    # plot the three usages in a line graph
    plt.plot(usageBySSID['Date'], usageBySSID['QUCONSOLES'], label='QUCONSOLES', color=colors['QUCONSOLES'])
    plt.plot(usageBySSID['Date'], usageBySSID['QUGuest'], label='QUGuest', color=colors['QUGuest'])
    plt.plot(usageBySSID['Date'], usageBySSID['QUINCY'], label='QUINCY', color=colors['QUINCY'])

    # deal with the s-axis, make it 5 minute intervals
    locator = MinuteLocator(interval=5)
    plt.gca().xaxis.set_major_locator(locator)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))
    plt.xticks(rotation=45, ha='right', color=colors['border'])

    # make the y-axis a float
    plt.gca().yaxis.set_major_formatter(FuncFormatter(makeFloat))

    # deal with the text for x, y, and title
    # plt.xlabel('Time', color=colors['font'])
    # plt.ylabel('Usage', color=colors['font'])
    plt.title('Wi-Fi Usage (Megabits per second)', color=colors['font'])

    plt.legend()    # creates a legend automatically

    # Set the color of x-axis tick indicators and tick labels to white
    plt.tick_params(axis='x', colors=colors['font'])

    # Set the color of y-axis tick indicators and tick labels to white
    plt.tick_params(axis='y', colors=colors['font'])

    # set the background colors
    plt.gcf().set_facecolor(colors['background'])
    plt.gca().set_facecolor(colors['background'])

    # make the border thicker and white
    plt.gca().spines['top'].set_color(colors['border'])
    plt.gca().spines['top'].set_linewidth(2)
    plt.gca().spines['bottom'].set_color(colors['border'])
    plt.gca().spines['bottom'].set_linewidth(2)
    plt.gca().spines['left'].set_color(colors['border'])
    plt.gca().spines['left'].set_linewidth(2)
    plt.gca().spines['right'].set_color(colors['border'])
    plt.gca().spines['right'].set_linewidth(2)

    # save the figure
    plt.savefig("//transporter/PiReporting/toPi/airwave/UsageOverTime.png")

    # plt.show()
    plt.close()
    return usageBySSID, usageBySSIDClients      # return both dicts for later use


def clientsEverySixty(usageBySSID, usageBySSIDClients, colors):
    # plot the total clients and the amount per SSID over an hour
    plt.plot(usageBySSID['Date'], usageBySSID['Clients'], label='Total Devices', color=colors['totalClients'])
    plt.plot(usageBySSID['Date'], usageBySSIDClients['QUCONSOLES'], label='QUCONSOLES', color=colors['QUCONSOLES'])
    plt.plot(usageBySSID['Date'], usageBySSIDClients['QUGuest'], label='QUGuest', color=colors['QUGuest'])
    plt.plot(usageBySSID['Date'], usageBySSIDClients['QUINCY'], label='QUINCY', color=colors['QUINCY'])
    plt.xticks(rotation=45, ha='right')

    # make the title
    plt.title("Wi-Fi Devices", color=colors['font'])

    # deal with the x-axis, make it 5 minute intervals
    locator = MinuteLocator(interval=5)
    plt.gca().xaxis.set_major_locator(locator)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))

    # set the background color
    plt.gcf().set_facecolor(colors['background'])
    plt.gca().set_facecolor(colors['background'])

    # make the y-axis an int, can't have part of a device
    plt.gca().yaxis.set_major_formatter(FuncFormatter(makeInt))

    # Set the color of x-axis tick indicators and tick labels to white
    plt.tick_params(axis='x', colors=colors['font'])

    # Set the color of y-axis tick indicators and tick labels to white
    plt.tick_params(axis='y', colors=colors['font'])

    # make the border thicker and white
    plt.gca().spines['top'].set_color(colors['border'])
    plt.gca().spines['top'].set_linewidth(2)
    plt.gca().spines['bottom'].set_color(colors['border'])
    plt.gca().spines['bottom'].set_linewidth(2)
    plt.gca().spines['left'].set_color(colors['border'])
    plt.gca().spines['left'].set_linewidth(2)
    plt.gca().spines['right'].set_color(colors['border'])
    plt.gca().spines['right'].set_linewidth(2)

    plt.legend()    # creates a legend automatically

    # save the figure
    plt.savefig("//transporter/PiReporting/toPi/airwave/Clients60Minutes.png")
    
    # plt.show()
    plt.close()


def usageByPie(usageBySSID, colors):
    # get the amount per SSID
    quc = sum(usageBySSID['QUCONSOLES'])
    qug = sum(usageBySSID['QUGuest'])
    qu = sum(usageBySSID['QUINCY'])

    # lists used for plotting
    totalUsageBySSID = [quc, qug, qu]
    total = sum(totalUsageBySSID)
    percentages = [quc / total, qug / total, qu / total]
    labels = ['QUCONSOLES', 'QUGuest', 'QUINCY']
    internalColors = [colors['QUCONSOLES'], colors['QUGuest'], colors['QUINCY']]

    radius = 0.4

    # determine the size of the figure
    fig, ax = plt.subplots(figsize=(4, 4), dpi=200)

    # set the background color
    plt.gcf().set_facecolor(colors['background'])
    plt.gca().set_facecolor(colors['background'])

    # Set aspect ratio to 'equal' to ensure the circle is drawn as a circle, and not an egg
    ax.set_aspect('equal', adjustable='box')

    # determine the angles for the wedges
    angles = [2 * math.pi * value / total for value in totalUsageBySSID]
    angles_degrees = [math.degrees(value) for value in angles]
    start_angle = 126  # start the first wedge as 126 degrees, so it's not boring

    # draw the wedges and put the percentage on them
    for angle, color, percentage in zip(angles_degrees, internalColors, percentages):
        ax.add_patch(patches.Wedge((.5, .5), radius, start_angle, start_angle + angle, color=color))
        text_angle = start_angle + angle / 2
        text_radius = radius * 0.7
        text_x = 0.5 + text_radius * math.cos(math.radians(text_angle))
        text_y = 0.5 + text_radius * math.sin(math.radians(text_angle))

        # Add text to the center of the wedge
        ax.text(text_x, text_y, f'{percentage * 100:.1f}%', ha='center', va='center', color=colors['font'], fontsize=10)

        start_angle += angle

    # turn the black border off --> this is needed because I manually made the pie rather than use the api
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    # set aspect ratio to be equal to ensure the circle stays circular, and not an egg
    ax.set_aspect('equal', adjustable='box')

    # add the legend manually
    ax.legend(bbox_to_anchor=(0.5, .9), loc='center left', labels=labels, fontsize=10)

    plt.title('Usage by SSID', color=colors['font'])
    plt.savefig("//transporter/PiReporting/toPi/airwave/UsageBySSID.png")
    # # plt.show()
    plt.close()


def usageByBuilding(byBuildings, colors):
    # modify the dataframes
    byBuildings["Max Usage In"] = byBuildings["Max Usage In"].apply(convertToBits)
    byBuildings["Max Usage Out"] = byBuildings["Max Usage Out"].apply(convertToBits)
    byBuildings['Interval'] = byBuildings['Interval'].apply(convertDateTime)
    byBuildings['Interval'] = byBuildings['Interval'].apply(removeDate)

    buildings = dict()
    counter = 0
    for folder in byBuildings["Folder"]:    # iterate through the items
        current = folder.split(' > ')   # splits the path --> Top > MainCampus > Residence Halls > FriarsHall
        # there are three criteria to determine what builing it is
        if 'Residence Halls' in current:    # if it is a residence hall
            if not current[current.index('Residence Halls') + 1] in buildings:  # if the hall has not been counted yet
                buildings[current[current.index('Residence Halls') + 1]] = (byBuildings['Max Usage In'].iloc[counter] +
                                                                            byBuildings['Max Usage Out'].iloc[counter])
            else:   # the hall has already been counted, so add to it
                buildings[current[current.index('Residence Halls') + 1]] += (byBuildings['Max Usage In'].iloc[counter] +
                                                                             byBuildings['Max Usage Out'].iloc[counter])
        elif 'NorthCampus' in current:  # if it is at north campus, grouped all NC to one count
            if 'NorthCampus' not in buildings:  # if NC hasn't been accounted for yet
                buildings['NorthCampus'] = (byBuildings['Max Usage In'].iloc[counter] +
                                            byBuildings['Max Usage Out'].iloc[counter])
            else:   # NC has been accounted for, so add to it
                buildings['NorthCampus'] += (byBuildings['Max Usage In'].iloc[counter] +
                                             byBuildings['Max Usage Out'].iloc[counter])
        else:   # if it does not match one of those, the last name is the name of the building
            if not current[-1] in buildings:    # if it has not been accounted for, count it
                buildings[current[-1]] = (byBuildings['Max Usage In'].iloc[counter] +
                                          byBuildings['Max Usage Out'].iloc[counter])
            else:   # if the current building has been accounted for, add t it
                buildings[current[-1]] += (byBuildings['Max Usage In'].iloc[counter] +
                                           byBuildings['Max Usage Out'].iloc[counter])
        counter += 1

    # delete a few categories
    del buildings['Top']
    del buildings['PresidentHouse']

    # combine and rename certain buildings
    buildings['HFC'] = buildings.pop('HealthAndFitnessCenter')
    buildings['SLC'] = buildings.pop('StudentLivingCenter')
    buildings['FrancisHall'] += buildings.pop('NetAdminStage')
    buildings['Cafe'] = buildings.pop('HawksHangout') + buildings.pop('StudentUnion')
    buildings = dict(sorted(buildings.items()))

    # make a bar graph
    plt.bar(list(buildings.keys()), list(buildings.values()), align='center', color=colors['buildings'])
    plt.title('Building usage in the last hour (Mb)', color=colors['font'], fontsize=20)

    # set the color of x-axis tick indicators and tick labels to white, rotate the text for flare
    plt.tick_params(axis='x', colors=colors['font'])
    plt.xticks(rotation=40, ha='right', color=colors['font'])

    # set the color of y-axis tick indicators and tick labels to white
    plt.tick_params(axis='y', colors=colors['font'])

    # set the background color
    plt.gcf().set_facecolor(colors['background'])
    plt.gca().set_facecolor(colors['background'])

    # make the border thicker and white
    plt.gca().spines['top'].set_color(colors['border'])
    plt.gca().spines['top'].set_linewidth(4)
    plt.gca().spines['bottom'].set_color(colors['border'])
    plt.gca().spines['bottom'].set_linewidth(4)
    plt.gca().spines['left'].set_color(colors['border'])
    plt.gca().spines['left'].set_linewidth(4)
    plt.gca().spines['right'].set_color(colors['border'])
    plt.gca().spines['right'].set_linewidth(4)

    # determine the size of the figure and save
    plt.gcf().set_size_inches((8, 8))
    plt.savefig('//transporter/PiReporting/toPi/airwave/usageByBuilding.png', dpi=200)
    plt.close()
    # plt.show()


def packetAction(bandwidth, colors):
    routeAction = {'allow': 0, 'deny': 0, 'reset-both': 0}
    # get only the last 60 seconds
    targetTime = max(bandwidth['Receive Time']) - pd.to_timedelta(60, unit='s')
    filteredBandwidth = bandwidth[bandwidth['Receive Time'] >= targetTime]
    filteredBandwidth = filteredBandwidth[['Receive Time', 'Action']]

    # total up the actions
    for packet in filteredBandwidth["Action"]:
        if packet not in routeAction:
            routeAction[packet] = 1
        else:
            routeAction[packet] += 1

    labels = list()
    for key, value in routeAction.items():  # adds the commas between after 3 nums
        labels.append(f"{key}: {'{:,}'.format(value)}")

    # used to get percentages and calculate it
    values = list(routeAction.values())
    total = sum(values)
    percentages = [routeAction['allow'] / total, routeAction['deny'] / total, routeAction['reset-both'] / total]

    internalColors = [colors['allowedPackets'], colors['deniedPackets'], colors['reset-both']]
    radius = 0.4

    # determine the size of the figure
    fig, ax = plt.subplots(figsize=(4, 4), dpi=200)

    # set the background color
    plt.gcf().set_facecolor(colors['background'])
    plt.gca().set_facecolor(colors['background'])

    # Set aspect ratio to 'equal' to ensure the circle is drawn as a circle
    ax.set_aspect('equal', adjustable='box')

    # determine the angles for the wedges
    angles = [2 * math.pi * value / total for value in values]
    angles_degrees = [math.degrees(value) for value in angles]
    start_angle = -126  # make it not so flat for flare

    # draw the wedges and put the percentage on them
    for angle, color, percentage in zip(angles_degrees, internalColors, percentages):
        ax.add_patch(patches.Wedge((.5, .5), radius, start_angle, start_angle + angle, color=color))
        text_angle = start_angle + angle / 2
        text_radius = radius * 0.7
        text_x = 0.5 + text_radius * math.cos(math.radians(text_angle))
        text_y = 0.5 + text_radius * math.sin(math.radians(text_angle))

        # Add text to the center of the wedge
        ax.text(text_x, text_y, f'{percentage * 100:.1f}%', ha='center', va='center', color=colors['font'],
                fontsize=10)

        start_angle += angle

    # turn the black border off
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    # Set aspect ratio to be equal to ensure the circle stays circular
    ax.set_aspect('equal', adjustable='box')
    ax.legend(bbox_to_anchor=(0.5, .9), loc='center left', labels=labels, fontsize=10)

    plt.title('Packet Action', color=colors['font'])
    plt.savefig("//transporter/PiReporting/toPi/firewall/PacketAction.png")
    # plt.show()
    plt.close()
