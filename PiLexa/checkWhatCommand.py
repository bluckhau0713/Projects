import datetime


def seeIfMikeTeachingCommand(phrase):
    if 'mike' in phrase:
        return True
    return False


def seeIfRoomAvailabilityCommand(phrase, days, buildingMappings, buildings, ncMappings, rooms):
    try:
        day = extractDay(phrase, days)
        # print(f'Extracted {getLists.getClassDate(day)} for day')
    except Exception as e:
        print(e)
    try:
        buildingCode = extractBuilding(phrase, buildingMappings, buildings, ncMappings).upper()
        # print(f'Extracted {buildingCode} for building')
    except Exception as e:
        print(e)
    try:
        room = extractRoom(phrase, rooms)
        # print(f'Extracted {room} for room')
    except Exception as e:
        return False, None, None, None
    return True, buildingCode, day, room


def seeIfFischer(phrase):
    if 'julie' in phrase:
        return True
    return False


def seeIfFanCommand(phrase):
    if 'fan' in phrase:
        return True
    return False


def seeIfLunchCommand(phrase):
    lunchWords = ['lunch', 'menu']
    for word in lunchWords:
        if word in phrase:
            return True
    return False


def seeIfAzureSync(phrase):
    if 'azure' in phrase:
        return True
    return False


def seeIfWeather(phrase):
    if 'weather' in phrase:
        return True
    return False


def extractBuilding(phrase, buildingMappings, buildings, ncMappings):
    for building in buildings:
        if building in phrase:
            return building

    try:
        campusIndex = phrase.index('campus')
        return ncMappings[f"{phrase[campusIndex]} {phrase[campusIndex + 1]}"]
    except:
        print()
        # print('campus does not appear')

    for mapping in buildingMappings:
        if mapping in phrase:
            return buildingMappings[mapping]
    # print("Did not detect a building: assume frh")
    return "frh"


def extractDay(phrase, days):
    if 'tomorrow' in phrase:
        tomorrow = datetime.datetime.now() + datetime.timedelta(1)
        tomorrow = tomorrow.strftime('%A')
        # print("Returning tomorrow")
        return tomorrow
    for day in days:
        if day in phrase:
            # print("Returning", day)
            return day
    # if a day is never said, return today
    today = datetime.datetime.now()
    today = today.strftime('%A')
    # print("Returning", today)
    return today


def extractRoom(phrase, rooms):
    for room in rooms:
        if room in phrase:
            return room
    raise Exception("Could not extract room number")