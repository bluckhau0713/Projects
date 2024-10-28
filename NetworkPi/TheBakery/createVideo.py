import matplotlib.patches as patches
import numpy as np
from collections import OrderedDict
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cv2
import matplotlib.pyplot as plt
import pandas as pd


def removeDate(dateTime):
    space = str(dateTime).index(" ")
    return str(dateTime)[space + 1:]


def mapSpeedToPercentage(speed):
    return speed * 180


def video(bandwidth, colors):
    # bandwidth["Receive Time"] = pd.to_datetime(bandwidth["Receive Time"])

    targetTimeStart = max(bandwidth['Receive Time']) - pd.to_timedelta(1, unit='s')

    bandwidthPerSecond = OrderedDict()
    for seconds in range(60, 0, -1):
        sessId = dict()
        targetTime = targetTimeStart - pd.to_timedelta(seconds, unit='s')
        filteredBandwidth = bandwidth[bandwidth['Receive Time'] == targetTime]
        filteredBandwidth = filteredBandwidth[['Receive Time', 'Bytes', 'Session ID']]

        for counter in range(len(filteredBandwidth["Session ID"])):
            if filteredBandwidth["Session ID"].iloc[counter] in sessId:
                sessId[filteredBandwidth["Session ID"].iloc[counter]] = max(filteredBandwidth["Bytes"].iloc[counter],
                                                                            sessId[filteredBandwidth["Session ID"].iloc[
                                                                                counter]])
            else:
                sessId[filteredBandwidth["Session ID"].iloc[counter]] = filteredBandwidth["Bytes"].iloc[counter]
        bandwidthPerSecond[targetTime] = (sum(sessId.values()) * 8)

    # print(sum(bandwidthPerSecond.values()) / len(bandwidthPerSecond))
    bandwidthList = list(bandwidthPerSecond.values())
    # print(bandwidthPerSecond)
    bandwidthList = [Mbps / 2000 for Mbps in bandwidthList]  # Mbps to Gbps / 1000 --> / 2 for bandwidth limit --> % now

    outerCounter = 0
    radius = .4
    for key in bandwidthPerSecond.keys():
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(4, 4), dpi=200)
        # fig, ax = plt.subplots()
        # Create a circle
        plt.title('Bandwidth Usage (Megabits per second)', color=colors['font'], fontsize=12)
        circle = patches.Circle((0.5, 0.5), radius=radius, edgecolor=colors['border'], facecolor='none', linewidth=3)

        # Add the circle to the axis
        ax.add_patch(circle)

        plt.gcf().set_facecolor(colors['background'])
        plt.gca().set_facecolor(colors['background'])

        # Set aspect ratio to 'equal' to ensure the circle is drawn as a circle
        ax.set_aspect('equal', adjustable='box')

        # Set axis limits if necessary
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        tick_spacing = 18
        tick_length = .05

        theta = np.arange(180, 360 + 180, tick_spacing)
        x_ticks = .5 + radius * np.cos(np.radians(theta))
        y_ticks = .5 + radius * np.sin(np.radians(theta))

        counter = 20
        for x, y, angle in zip(x_ticks, y_ticks, theta):
            x_start = x - 0.05 * np.cos(np.radians(angle))
            y_start = y - 0.05 * np.sin(np.radians(angle))
            x_end = x_start + tick_length * np.cos(np.radians(angle))
            y_end = y_start + tick_length * np.sin(np.radians(angle))
            ax.plot([x_start, x_end], [y_start, y_end], color=colors['border'])
            # ax.plot([x_start, x_end], [y_start, y_end], color='white')
            if counter == 20:
                mbps = str(0)
            else:
                mbps = str(int((counter * .1) * 2000))

            label_x = x_start + 0.1 * np.cos(np.radians(angle))  # Adjust the position of the label
            label_y = y_start + 0.1 * np.sin(np.radians(angle))  # Adjust the position of the label
            ax.text(label_x, label_y, f'{mbps}', color=colors['font'], ha='center', va='center', fontsize=10,
                    rotation=angle - 90)

            counter -= 1

        # draw the red gauge line
        gauge_angle = -mapSpeedToPercentage(
            bandwidthList[outerCounter]) - 180  # Angle for the gauge (180 degrees for 50%)
        gauge_x = 0.5 + radius * np.cos(np.radians(gauge_angle))
        gauge_y = 0.5 + radius * np.sin(np.radians(gauge_angle))
        ax.plot([0.5, gauge_x], [0.5, gauge_y], color=colors['gauge'], linestyle='solid')

        time_x = 0.5
        time_y = 0.4
        ax.text(time_x, time_y, removeDate(key), color=colors['font'], ha='center', va='center', fontsize=10)

        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        plt.savefig(f"C:/PythonScripts/NetworkPi/speedometerFrames/frame_{outerCounter}.png")
        # plt.show()
        plt.close()
        outerCounter += 1

    frame_files = [f"C:/PythonScripts/NetworkPi/speedometerFrames/frame_{i}.png" for i in range(len(bandwidthList))]
    frame = cv2.imread(frame_files[0])
    height, width, layers = frame.shape
    # print(width, height)
    vid = cv2.VideoWriter("//transporter/PiReporting/toPi/firewall/speedometer.webm", cv2.VideoWriter_fourcc(*"VP80"), 1, (width, height))

    for frame_file in frame_files:
        vid.write(cv2.imread(frame_file))

    cv2.destroyAllWindows()
    vid.release()


def createVideoDf(bandwidth):
    uselessCountries = ['10.0.0.0-10.255.255.255', '172.16.0.0-172.31.255.255', '192.168.0.0-192.168.255.255',
                        '100.64.0.0-100.127.255.255', '169.254.0.0-169.254.255.255', '192.0.0.0-192.0.0.255',
                        '192.0.2.0-192.0.2.255']
    targetTimeStart = max(bandwidth['Receive Time']) - pd.to_timedelta(1, unit='s')
    sourcesPerSecond = OrderedDict()
    destinationsPerSecond = OrderedDict()
    for seconds in range(60, 0, -1):
        # print(seconds)
        targetTime = targetTimeStart - pd.to_timedelta(seconds, unit='s')
        filteredBandwidth = bandwidth[bandwidth['Receive Time'] == targetTime]
        filteredBandwidth = filteredBandwidth[['Receive Time', 'Source Country', 'Destination Country']]
        for counter in range(len(filteredBandwidth['Receive Time'])):
            if filteredBandwidth['Source Country'].iloc[counter] not in uselessCountries:
                if targetTime not in sourcesPerSecond:
                    sourcesPerSecond[targetTime] = {filteredBandwidth['Source Country'].iloc[counter]: 1}
                else:
                    if filteredBandwidth['Source Country'].iloc[counter] not in sourcesPerSecond[targetTime]:
                        sourcesPerSecond[targetTime][filteredBandwidth['Source Country'].iloc[counter]] = 1
                    else:
                        sourcesPerSecond[targetTime][filteredBandwidth['Source Country'].iloc[counter]] += 1
            # Now destinations
            if filteredBandwidth['Destination Country'].iloc[counter] not in uselessCountries:
                if targetTime not in destinationsPerSecond:
                    destinationsPerSecond[targetTime] = {filteredBandwidth['Destination Country'].iloc[counter]: 1}
                else:
                    if filteredBandwidth['Destination Country'].iloc[counter] not in destinationsPerSecond[targetTime]:
                        destinationsPerSecond[targetTime][filteredBandwidth['Destination Country'].iloc[counter]] = 1
                    else:
                        destinationsPerSecond[targetTime][filteredBandwidth['Destination Country'].iloc[counter]] += 1
        if targetTime not in sourcesPerSecond:  # if nothing happened in that second
            sourcesPerSecond[targetTime] = {'Unknown': 1}
        if targetTime not in destinationsPerSecond:     # if nothing happened in that second
            destinationsPerSecond[targetTime] = {'Unknown': 1}

    # for key, value in sourcesPerSecond.items():
    #     print(f'{key}: {value}')
    # for key, value in destinationsPerSecond.items():
    #     print(f'{key}: {value}')
    return sourcesPerSecond, destinationsPerSecond


def worldVideo(bandwidth, colors):
    coordinates = {
        'QU': (39.9, -91.3),
        'Afghanistan': (33.9, 67.7),
        'Albania': (41.0, 20.0),
        'Algeria': (28.0, 1.6),
        'Andorra': (42.5, 1.5),
        'Angola': (-11.2, 17.87),
        'Antigua and Barbuda': (17.1, -61.8),
        'Argentina': (-37.4, -63.6),
        'Armenia': (40.0, 45.0),
        'Asia Pacific Region': (7.0, 165),
        'Australia': (-25.0, 135.0),
        'Austria': (47.6, 14.0),
        'Azerbaijan': (40.1, 47.5),
        'Bahamas': (25.0, -77.0),
        'Bahrain': (26.0, 50.5),
        'Bangladesh': (23.6, 90.3),
        'Barbados': (13.2, -59.5),
        'Belarus': (53.7, 27.9),
        'Belgium': (50.5, 4.4),
        'Belize': (17.2, -88.5),
        'Benin': (9.3, 2.3),
        'Bhutan': (27.5, 90.4),
        'Bolivia Plurinational State Of': (-17.0, -65.0),
        'Bosnia and Herzegovina': (44.0, 17.6),
        'Botswana': (-22.3, 24.7),
        'Brazil': (-10.0, -55.0),
        'Brunei': (4.5, 114.7),
        'Bulgaria': (42.7, 25.4),
        'Burkina Faso': (12.2, -1.5),
        'Burundi': (-3.3, 29.9),
        'Cabo Verde': (16.5, -23.0),
        'Cambodia': (12.5, 104.9),
        'Cameroon': (7.3, 11.9),
        'Canada': (60.0, -100.0),
        'Central African Republic': (6.6, 20.9),
        'Chad': (15.0, 19.0),
        'Chile': (-30.0, -71.0),
        'China': (35.0, 105.0),
        'Colombia': (4.0, -74.0),
        'Comoros': (-11.6, 43.3),
        'Congo': (-1.0, 21.0),
        'Costa Rica': (9.7, -83.7),
        # 'Cote d\'Ivoire': (8.0, -5.0),
        'Croatia': (45.1, 15.2),
        'Cuba': (21.5, -80.0),
        'Cyprus': (35.0, 33.0),
        'Czech Republic': (49.8, 15.4),
        'Denmark': (56.0, 9.5),
        'Djibouti': (11.8, 42.5),
        'Dominica': (15.4, -61.3),
        'Dominican Republic': (18.7, -70.1),
        'Ecuador': (-1.8, -78.1),
        'Egypt': (27.0, 30.0),
        'El Salvador': (13.7, -88.9),
        'Equatorial Guinea': (1.6, 10.2),
        'Eritrea': (15.1, 39.7),
        'Estonia': (58.5, 25.0),
        'Eswatini': (-26.5, 31.4),
        'Ethiopia': (9.0, 40.0),
        'European Union': (50.5, 4.2),
        'Fiji': (-17.7, 178.0),
        'Finland': (64.0, 26.0),
        'France': (46.4, 2.0),
        'Gabon': (-0.8, 11.6),
        'Gambia': (13.4, -15.3),
        'Georgia': (42.3, 43.3),
        'Germany': (51.0, 10.4),
        'Ghana': (7.9, -1.0),
        'Greece': (39.0, 21.8),
        'Grenada': (12.1, -61.6),
        'Guatemala': (15.7, -90.2),
        'Guinea': (9.9, -9.6),
        'Guinea-Bissau': (11.8, -15.1),
        'Guyana': (4.8, -58.9),
        'Haiti': (18.9, -72.2),
        'Honduras': (15.2, -86.2),
        'Hong Kong': (22.3, 114.1),
        'Hungary': (47.1, 19.5),
        'Iceland': (65.0, -18.0),
        'India': (21.0, 78.0),
        'Indonesia': (-0.7, 113.9),
        'Iran Islamic Republic Of': (32.4, 53.7),
        'Iraq': (33.0, 43.6),
        'Ireland': (53.0, -8.0),
        'Israel': (31.0, 34.8),
        'Italy': (41.8, 12.5),
        'Jamaica': (18.1, -77.2),
        'Japan': (36.0, 138.0),
        'Jordan': (30.5, 36.2),
        'Kazakhstan': (48.0, 68.0),
        'Kenya': (0.0, 37.9),
        'Kiribati': (1.8, -157.0),
        'Korea Republic Of': (40.0, 127.0),
        'Korea, South': (36.5, 128.0),
        'Kosovo': (42.6, 20.9),
        'Kuwait': (29.5, 47.4),
        'Kyrgyzstan': (41.2, 74.7),
        'Laos': (19.8, 102.0),
        'Latvia': (56.8, 24.6),
        'Lebanon': (33.8, 35.8),
        'Lesotho': (-29.6, 28.2),
        'Liberia': (6.4, -9.4),
        'Libya': (26.3, 17.0),
        'Liechtenstein': (47.1, 9.5),
        'Lithuania': (55.1, 23.8),
        'Luxembourg': (49.8, 6.1),
        'Madagascar': (-20.0, 46.8),
        'Malawi': (-13.2, 34.3),
        'Malaysia': (4.2, 101.9),
        'Maldives': (3.2, 73.2),
        'Mali': (17.0, -4.0),
        'Malta': (35.9, 14.4),
        # 'Marshall Islands': (7.0, 168.0),
        'Mauritania': (21.0, -10.9),
        'Mauritius': (-20.3, 57.5),
        'Mexico': (23.0, -102.0),
        # 'Micronesia': (6.0, 158.0),
        'Moldova Republic Of': (47.4, 28.3),
        'Monaco': (43.7, 7.4),
        'Mongolia': (46.0, 104.0),
        'Montenegro': (42.7, 19.3),
        'Morocco': (32.0, -5.0),
        'Mozambique': (-18.6, 34.0),
        'Myanmar': (21.9, 96.5),
        'Namibia': (-22.9, 18.4),
        'Nauru': (-0.5, 166.9),
        'Nepal': (28.3, 84.0),
        'Netherlands': (52.1, 5.2),
        'New Zealand': (-41.0, 174.0),
        'Nicaragua': (12.8, -85.0),
        'Niger': (16.0, 8.0),
        'Nigeria': (10.0, 8.0),
        'Macedonia The Former Yugoslav Republic Of': (41.6, 21.7),
        'Norway': (62.0, 10.0),
        'Oman': (21.4, 57.0),
        'Pakistan': (30.0, 70.0),
        # 'Palau': (7.5, 134.5),
        'Panama': (9.0, -80.0),
        'Papua New Guinea': (-6.0, 143.0),
        'Paraguay': (-23.0, -58.5),
        'Peru': (-9.1, -75.0),
        'Philippines': (12.8, 121.7),
        'Poland': (52.0, 20.0),
        'Portugal': (39.5, -8.0),
        'Qatar': (25.3, 51.1),
        'Romania': (45.9, 24.9),
        'Russian Federation': (60.0, 100.0),
        'Rwanda': (-1.9, 29.8),
        # 'Saint Kitts and Nevis': (17.3, -62.7),
        # 'Saint Lucia': (13.9, -60.9),
        # 'Saint Vincent and the Grenadines': (12.9, -61.2),
        'Samoa': (-13.7, -172.1),
        # 'San Marino': (43.9, 12.5),
        'Sao Tome and Principe': (0.1, 6.6),
        'Saudi Arabia': (25.0, 45.0),
        'Senegal': (14.4, -14.4),
        'Serbia': (44.0, 21.0),
        'Seychelles': (-4.6, 55.5),
        'Sierra Leone': (8.4, -11.7),
        'Singapore': (1.3, 103.8),
        'Slovakia': (48.6, 19.6),
        'Slovenia': (46.1, 14.9),
        'Solomon Islands': (-9.6, 160.1),
        'Somalia': (10.0, 49.0),
        'South Africa': (-29.0, 24.0),
        'South Sudan': (7.5, 30.0),
        'Spain': (40.0, -4.0),
        'Sri Lanka': (7.7, 80.0),
        'Sudan': (15.0, 30.0),
        'Suriname': (4.0, -56.0),
        'Sweden': (63.0, 16.0),
        'Switzerland': (47.0, 8.0),
        'Syria': (34.8, 38.9),
        'Taiwan': (24.0, 121.0),
        'Tajikistan': (38.8, 71.0),
        'Tanzania': (-6.3, 34.8),
        'Thailand': (16.2, 100.0),
        'Timor-Leste': (-8.8, 125.5),
        'Togo': (8.0, 1.0),
        # 'Tonga': (-20.0, -175.0),
        'Trinidad And Tobago': (10.6, -61.2),
        'Tunisia': (34.0, 9.0),
        'Turkey': (39.0, 35.0),
        'Turkmenistan': (38.9, 59.5),
        # 'Tuvalu': (-8.0, 178.0),
        'Uganda': (1.3, 32.0),
        'Ukraine': (49.0, 32.0),
        'United Arab Emirates': (24.0, 54.0),
        'United Kingdom': (53.0, -2),
        'United States': (39.8, -98.6),
        'Unknown': (0, 0),
        'Uruguay': (-33.0, -56.0),
        'Uzbekistan': (41.0, 64.0),
        # 'Vanuatu': (-16.0, 167.0),
        # 'Vatican City': (41.9, 12.5),
        'Venezuela Bolivarian Republic Of': (8.0, -66.0),
        'Viet Nam': (14.0, 108.0),
        'Virgin Islands British': (18.4, -64.6),
        'Yemen': (15.5, 48.0),
        'Zambia': (-15.0, 27.5),
        'Zimbabwe': (-19.0, 29.0),
    }
    sources, destinations = createVideoDf(bandwidth)

    # print(len(sources))
    # print(len(destinations))
    labels = ['Sources', 'Destinations', 'Both']
    source, dest, both = None, None, None
    outerCounter = 0
    for (sourceKey, sourceDict), (destinationsKey, destinationsDict) in zip(sources.items(), destinations.items()):
        # print(country, country[1], country[0])
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        ax.set_global()

        # Add Natural Earth features for context
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.LAND, color=colors['land'])
        ax.add_feature(cfeature.LAKES, edgecolor=colors['water'])
        ax.add_feature(cfeature.RIVERS)
        ax.set_facecolor(colors['water'])
        fig.set_facecolor(color=colors['background'])
        for sourceCountry, sourceAmount in sourceDict.items():

            if sourceCountry in destinationsDict.keys():
                bothLongitude = coordinates[sourceCountry][1]
                bothLatitude = coordinates[sourceCountry][0]

                ax.plot(bothLongitude, bothLatitude, 'ro', markersize=2, transform=ccrs.PlateCarree())
                ax.text(bothLongitude, bothLatitude, sourceAmount + destinationsDict[sourceCountry],
                        transform=ccrs.PlateCarree(), color=colors['font'])
                both, = ax.plot([coordinates['QU'][1], bothLongitude], [coordinates['QU'][0], bothLatitude],
                                transform=ccrs.PlateCarree(), color=colors['both'])
                del destinationsDict[sourceCountry]
            else:
                sourceLongitude = coordinates[sourceCountry][1]
                sourceLatitude = coordinates[sourceCountry][0]

                # ax.plot([x_start, x_end], [y_start, y_end], color='white')

                # Plot the point on the map
                ax.plot(sourceLongitude, sourceLatitude, 'ro', markersize=2, transform=ccrs.PlateCarree())
                ax.text(sourceLongitude, sourceLatitude, sourceAmount, transform=ccrs.PlateCarree(),
                        color=colors['font'])
                source, = ax.plot([coordinates['QU'][1], sourceLongitude], [coordinates['QU'][0], sourceLatitude],
                                  transform=ccrs.PlateCarree(), color=colors['source'])

        for destCountry, destAmount in destinationsDict.items():

            destLongitude = coordinates[destCountry][1]
            destLatitude = coordinates[destCountry][0]
            # ax.plot([x_start, x_end], [y_start, y_end], color='white')

            # Plot the point on the map
            ax.plot(destLongitude, destLatitude, 'ro', markersize=2, transform=ccrs.PlateCarree())
            ax.text(destLongitude, destLatitude, destAmount, transform=ccrs.PlateCarree(), color=colors['font'])
            dest, = ax.plot([coordinates['QU'][1], destLongitude], [coordinates['QU'][0], destLatitude],
                            transform=ccrs.PlateCarree(), color=colors['destination'])
            # print(f'Destinations: {destAmount}')
    # plt.tight_layout()
        ax.legend(handles=[source, dest, both], bbox_to_anchor=(0, .4), loc='center left', labels=labels, fontsize=10)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.title(f'Global Traffic Routes at {sourceKey}', color=colors['font'])
        # plt.show()

        plt.savefig(f'C:/PythonScripts/NetworkPi/worldFrames/frame_{outerCounter}.png', dpi=200)
        plt.close()
        outerCounter += 1

    frame_files = [f"C:/PythonScripts/NetworkPi/worldFrames/frame_{i}.png" for i in range(60)]
    frame = cv2.imread(frame_files[0])
    height, width, layers = frame.shape
    # print(width, height)
    vid = cv2.VideoWriter("//transporter/PiReporting/toPi/firewall/worldTraffic.webm", cv2.VideoWriter_fourcc(*"VP80"), 1, (width, height))

    for frame_file in frame_files:
        vid.write(cv2.imread(frame_file))

    cv2.destroyAllWindows()
    vid.release()
