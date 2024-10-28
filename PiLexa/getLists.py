import datetime


def getRoomCodes(cursor):
    query = f"""
    SELECT DISTINCT

    schedules.ROOM_CDE

    FROM

    TmsEPrd.dbo.SECTION_SCHEDULES as schedules

    WHERE
    schedules.YR_CDE LIKE {getYear()} -- "Dynamic" will always be current year
    AND
    schedules.TRM_CDE LIKE '{getTerm()}' -- "Dynamic" will assume the current term
    AND
    schedules.LOC_CDE NOT LIKE 'WEB'
    AND
    schedules.LOC_CDE NOT LIKE 'OFF'
    AND
    schedules.ROOM_CDE NOT LIKE 'NULL'

    ORDER BY schedules.ROOM_CDE
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    counter = 0
    for row in rows:
        rows[counter] = row[0].lower().strip()
        counter += 1

    # print(rows)
    # print(type(rows))
    return rows


def getBuildingCodes(cursor):
    query = f"""
    SELECT DISTINCT

    schedules.BLDG_CDE

    FROM

    TmsEPrd.dbo.SECTION_SCHEDULES as schedules

    WHERE
    schedules.YR_CDE LIKE {getYear()} -- "Dynamic" will always be current year
    AND
    schedules.TRM_CDE LIKE '{getTerm()}' -- "Dynamic" will assume the current term
    AND
    schedules.LOC_CDE NOT LIKE 'WEB'
    AND
    schedules.LOC_CDE NOT LIKE 'OFF'
    AND
    schedules.BLDG_CDE NOT LIKE 'NULL'

    ORDER BY schedules.BLDG_CDE
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    counter = 0
    for row in rows:
        rows[counter] = row[0].lower().strip()
        counter += 1

    # print(rows)
    # print(type(rows))
    return rows


def getYear():
    year = datetime.datetime.now()
    year = year.strftime('%Y')
    return year


def getDays():
    return ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']


def getFanModes():
    return ['low', 'high', 'off', 'l', 'h', 'o']


def getActivateWords():
    return ["pi", "pie", "python", "py"]


def getBuildingMappings():
    return {
        'francis': 'frh',
        'friars': 'fri',
        'fitness': 'hfc',
        'success': 'ssc',
        'frances': 'frh'
    }


def getNorthCampusMappings():
    return {
        'campus a': 'nca',
        'campus b': 'ncb',
        'campus d': 'ncd'
    }


def getClassDate(daySaid):
    daySaid = daySaid.upper() + "_CDE"
    return f"schedules.{daySaid} NOT LIKE ''"


def getCycle():
    now = datetime.datetime.now()
    startDate = datetime.datetime.strptime('08/26/2024', '%m/%d/%Y')
    return ((now - startDate).days // 7) % 4 + 1


def getTerm():
    # Will add dynamic term at some point
    return 'FA'
