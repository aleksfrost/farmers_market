import csv
from datetime import datetime
import re


def run_parcer():
    #Open and read .csv file
    with open(r'Export.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  #read headers
        #create lists and write files for payments and merch
        payments = list(enumerate(headers[23:28]))
        with open(r'tables_from_export\payments.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(payments)
        merchandise = list(enumerate(headers[28:58]))
        with open(r'tables_from_export\merch.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(merchandise)
        #create lists for tables
        markets = []
        markets_payments = []
        markets_merch = []
        websites = []
        facebooks = []
        tweetters = []
        youtubes = []
        othermedias = []
        streets = []
        zips = []
        coords = []
        cities = []
        states = []
        countries = []
        seasons = []
        market_season = []
        locations = []
        market_locations = []
        upd_dates = []
        market_updates = []

        #start reading the data
        for row in csv_reader:
            market_id = row[0]
            market_name = row[1]
            market_website = row[2]
            market_facebook = row[3]
            market_twitter = row[4]
            market_youtube = row[5]
            market_othermedia = row[6]
            market_street = row[7]
            market_city = row[8]
            market_country = row[9]
            market_state = row[10]
            market_zip = row[11]
            s1_date = row[12]   #dates
            s1_time = row[13]   #times + day
            s2_date = row[14]   #dates
            s2_time = row[15]   #times + day
            s3_date = row[16]   #dates
            s3_time = row[17]   #times + day
            s4_date = row[18]   #dates
            s4_time = row[19]   #times + day
            coord = row[20:22]    #x, y
            location = row[22]
            upd_time = row[58]

            #fill paymets/markets list
            for i in range(len(payments)):
                if row[23:28][i] == "Y":
                    markets_payments.append([i, market_id])

            #fill merch/markets list
            for i in range(len(merchandise)):
                if row[28:58][i] == "Y":
                    markets_merch.append([i, market_id])

            #fill medias
            if market_website:
                websites.append([market_id, market_website])
            if market_facebook:
                facebooks.append([market_id, market_facebook])
            if market_twitter:
                tweetters.append([market_id, market_twitter])
            if market_youtube:
                youtubes.append([market_id, market_youtube])
            if market_othermedia:
                othermedias.append([market_id, market_othermedia])

            #fill streets
            if market_street in streets:
                street_id = streets.index(market_street)
            else:
                streets.append(market_street)
                street_id = streets.index(market_street)

            #fill zips
            if market_zip in zips:
                zip_id = zips.index(market_zip)
            else:
                zips.append(market_zip)
                zip_id = zips.index(market_zip)

            #fill coords
            if coord in coords:
                coord_id = coords.index(coord)
            else:
                coords.append(coord)
                coord_id = coords.index(coord)


            #fill markets list
            markets.append([market_id, market_name, street_id, zip_id, coord_id])

            #fill cities, states, countries
            #fill relation city - zip
            city_zip = [zip_id, market_city]
            if city_zip not in cities:
                cities.append(city_zip)

            #fill relation state - zip
            state_zip = [zip_id, market_state]
            if city_zip not in states:
                states.append(state_zip)

            #fill relation country - zip
            countrie_zip = [zip_id, market_country]
            if countrie_zip not in countries:
                countries.append(countrie_zip)

            #fill date adn time when market is open
            for data, dtime in (zip((s1_date, s2_date, s3_date, s4_date), (s1_time, s2_time, s3_time, s4_time))):
                if data:
                    temp = [clr_data.strip() for clr_data in data.split("to")]
                    if len(temp) == 2:
                        date_start = temp[0]
                        try:
                            new_date_start = datetime.strptime(date_start, '%m/%d/%Y').strftime('%Y-%m-%d')
                        except ValueError:
                            print(f'Incorrect value date_start {date_start} on market_id {market_id}. Write null')
                            new_date_start = None
                        if temp[1] == '':
                            new_date_end = None
                        else:
                            date_end = temp[1]
                            try:
                                new_date_end = datetime.strptime(date_end, '%m/%d/%Y').strftime('%Y-%m-%d')
                            except ValueError:
                                print(f'Incorrect value date_end {date_end} on market_id {market_id}. Write null')
                                new_date_end = None
                    t_start = None
                    t_end = None
                    for dt in dtime[:-1].split(';'):
                        pattern_start = r'\d+:\d+\s\w+(?=-)'
                        pattern_end = r'(?<=-)\d+:\d+\s\w+'
                        t_start = re.findall(pattern_start, dt)
                        if len(t_start) == 1:
                            t_start = t_start[0]
                        else:
                            t_start = None
                        t_end = re.findall(pattern_end, dt)
                        if len(t_end) == 1:
                            t_end = t_end[0]
                        else:
                            t_end = None
                        the_day = re.findall(r'\b[A-Za-z]{3}', dt)
                        if the_day:
                            the_day = the_day[0]
                        else:
                            t_end = None
                        open_time = [new_date_start, new_date_end, the_day, t_start, t_end]
                        if open_time in seasons:
                            season_id = seasons.index(open_time)
                        else:
                            seasons.append(open_time)
                            season_id = seasons.index(open_time)
                        market_season.append([season_id, market_id])


            # fill locations
            if location in locations:
                location_id = locations.index(location)
            else:
                locations.append(location)
                location_id = locations.index(location)

            market_locations.append([location_id, market_id])


            #Format and fill UPD timestamp

            if "AM" in upd_time or "PM" in upd_time:
                converted_time = datetime.strptime(upd_time, "%m/%d/%Y %I:%M:%S %p").strftime("%Y-%m-%d %H:%M:%S")
            else:
                converted_time = datetime.strptime(upd_time, "%d.%m.%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")

            if converted_time in upd_dates:
                upd_id = upd_dates.index(upd_time)
            else:
                upd_dates.append(converted_time)
                upd_id = upd_dates.index(converted_time)

            market_updates.append([upd_id, market_id])

        #write files mentioned
        with open(r'tables_from_export\markets_merch.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(markets_merch)

        with open(r'tables_from_export\markets_payments.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(markets_payments)

        with open(r'tables_from_export\streets.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(list(enumerate(streets)))

        with open(r'tables_from_export\zips.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(list(enumerate(zips)))

        coordinates = []
        for i in range(len(coords)):
            temp = coords[i]
            temp.insert(0, i)
            coordinates.append(temp)
        with open(r'tables_from_export\coords.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(coordinates)

        cities_with_ids = []
        for i in range(len(cities)):
            temp = cities[i]
            temp.insert(0, i)
            cities_with_ids.append(temp)
        with open(r'tables_from_export\cities.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(cities_with_ids)

        countries_with_ids = []
        for i in range(len(countries)):
            temp = countries[i]
            temp.insert(0, i)
            countries_with_ids.append(temp)
        with open(r'tables_from_export\countries.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(countries_with_ids)

        states_with_ids = []
        for i in range(len(states)):
            temp = states[i]
            temp.insert(0, i)
            states_with_ids.append(temp)
        with open(r'tables_from_export\states.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(states_with_ids)


        with open(r'tables_from_export\fmarkets.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(markets)


        with open(r'tables_from_export\market_seasons.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(market_season)


        seasons_with_ids = []
        for i in range(len(seasons)):
            temp = seasons[i]
            temp.insert(0, i)
            seasons_with_ids.append(temp)
        with open(r'tables_from_export\seasons.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(seasons_with_ids)


        with open(r'tables_from_export\locations.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(list(enumerate(locations)))

        with open(r'tables_from_export\updates.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(list(enumerate(upd_dates)))

        with open(r'tables_from_export\market_locations.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(market_locations)

        with open(r'tables_from_export\market_upds.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(market_updates)

        with open(r'tables_from_export\websites.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(websites)

        with open(r'tables_from_export\fbs.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(facebooks)

        with open(r'tables_from_export\tweets.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(tweetters)

        with open(r'tables_from_export\youtubes.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(youtubes)

        with open(r'tables_from_export\othermedias.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv.writer(out_file).writerows(othermedias)


run_parcer()

"""
As it is there is two records that has wrong date format
One is "November 21 - April 17" instead of DD/MM/YYYY format
The other is september 31st which is impossible (30 max)


Result:
Incorrect value date_start November 21 on market_id 1020001. Write null
Incorrect value date_end April 17 on market_id 1020001. Write null
Incorrect value date_end 09/31/2012 on market_id 1005358. Write null
"""