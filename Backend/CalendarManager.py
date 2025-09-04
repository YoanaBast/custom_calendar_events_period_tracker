import json
import calendar
import os
from datetime import datetime

class CalendarManager:
    def __init__(self):
        self.events_path = os.path.join("..", "DB", "events.json")


    def load_events(self):
        try:
            with open(self.events_path) as f:
                events = json.load(f)
        except FileNotFoundError:
            events = {}
        return events

    def save_events(self, events):
        import json
        with open(self.events_path, "w") as f:
            json.dump(events, f, indent=2)

    def add_event(self, user, event_name, event_type,  event_start_date, event_end_date=None, event_notes=None):
        events = self.load_events()
        if user not in events:
            events[user] = []

        new_event = {
            "title": event_name,
            "type": event_type,
            "start_date": event_start_date,
            "end_date": event_end_date,
            "notes": event_notes
        }

        if not any(e["title"] == event_name and e["start_date"] == event_start_date for e in events[user]):
            events[user].append(new_event)
            print(f"Event '{event_name}' added for {user}")
        else:
            print("Event already exists")

        self.save_events(events)


    def start_tracking_period(self, user):
        pass



    def set_period_arrived(self, user):
        pass


    def display_calendar_terminal(self, user):
        current_year  = datetime.now().year
        user_events = self.load_events()[user]
        events_by_month = {}
        for event in user_events:
            day_str, month_str = event['start_date'].split('/')
            day, month = int(day_str), int(month_str)
            events_by_month.setdefault(month, set()).add(day)
            print(events_by_month)

        c = calendar.Calendar()
        for month in range(1, 13):
            print(f"\n---- {calendar.month_name[month]} {current_year} ----")
            print("Mo Tu We Th Fr Sa Su")

            weeks_in_month = c.monthdayscalendar(current_year, month)
            for week_days in weeks_in_month:
                print(" ".join(
                    f"{day:2}*" if day in events_by_month.get(month, set()) else f"{day:2} "
                    for day in week_days
                ))

