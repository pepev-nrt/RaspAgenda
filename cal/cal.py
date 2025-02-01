#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
# TODO: Comment this
"""

import caldav
from datetime import date, datetime, timedelta
import pytz
import vobject


class CalendarHelper:

    def __init__(self, caldavURL: str, caldavUser: str, caldavPassword: str, timezone="Europe/Madrid", caldavBlacklist=[""]):
        self.caldavURL = caldavURL
        self.caldavUser = caldavUser
        self.caldavPassword = caldavPassword
        self.caldavBlacklist = caldavBlacklist
        self.timezone = timezone


    def fetch_cals(self):

        with caldav.DAVClient(
            url=self.caldavURL,
            username=self.caldavUser,
            password=self.caldavPassword
        ) as client:
        
            principal = client.principal()

            # Get user's calendars
            calendars = principal.calendars()

            # Upcoming events on all calendars
            tz = pytz.timezone(self.timezone)
            now = datetime.now(tz=tz)
            end = now + timedelta(days=30)
            all_events = []
            for calendar in calendars:
                #print(str(calendar))
                if str(calendar) not in self.caldavBlacklist:
                    events = calendar.search(start=now, end=end, expand=True)
                    all_events.extend(events)
            

            # Parse events into parsed_vents list
            parsed_events = []
            for event in all_events:
                parsed_events.append(self.parse_event(event.data))

            for event in parsed_events:
                # If datetime.datetime, do nothing, if datetime.time, convert it to datetime.datetime
                if not isinstance(event["DTSTART"], datetime):
                    event["DTSTART"] = date.strftime(event["DTSTART"], '%Y-%m-%d, %H:%M:%S')
                    event["DTSTART"] = datetime.strptime(event["DTSTART"], '%Y-%m-%d, %H:%M:%S')

                else:
                    event["DTSTART"] = datetime.strftime(event["DTSTART"], '%Y-%m-%d, %H:%M:%S')
                    event["DTSTART"] = datetime.strptime(event["DTSTART"], '%Y-%m-%d, %H:%M:%S')


                    #event["DTSTART"] = datetime.combine(event["DTSTART"], datetime.min.time())
            
            #print(parsed_events)
            # Sort the list of dictionaries by DTSTART
            sorted_events = sorted(parsed_events, key=lambda x: x['DTSTART'])

            #return sorted_events

            # Print the sorted list of events
            #for event in sorted_events:
                #print(f'{event["DTSTART"]} --- {event["SUMMARY"]}')
            
        return sorted_events


    def parse_event(self, event_str: str):
        calendar = vobject.readOne(event_str)
        event = calendar.vevent

        event_dict = {}
        for component in event.getChildren():
            try:
                event_dict[component.name] = component.value
            except:
                continue

        return(event_dict)