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


    def start_tracking_period(self, user, first_day_last_per, cycle_len=28, per_len=5):
        current_year_int  = datetime.now().year
        current_month_int = datetime.now().month
        last_month_lst = calendar.monthcalendar(current_year_int, current_month_int - 1)
        curr_month_lst = calendar.monthcalendar(current_year_int, current_month_int)
        next_month_lst = calendar.monthcalendar(current_year_int, current_month_int + 1)

        last_curr_next_moth_flat_list = [f"{day}/{current_month_int -1}"  for week in last_month_lst for day in week]
        last_curr_next_moth_flat_list.extend([f"{day}/{current_month_int}" for week in curr_month_lst for day in week])
        last_curr_next_moth_flat_list.extend([f"{day}/{current_month_int + 1}"  for week in next_month_lst for day in week])
        last_curr_next_moth_flat_list = [x for x in last_curr_next_moth_flat_list if int(x.split('/')[0]) != 0]

        index_of_last_day = last_curr_next_moth_flat_list.index(f"{first_day_last_per}/{current_month_int -1}")
        index_of_next_start_day = index_of_last_day + cycle_len

        last_dates = [last_curr_next_moth_flat_list[index_of_last_day + i] for i in range(per_len)]
        curr_dates = [last_curr_next_moth_flat_list[index_of_next_start_day + i] for i in range(per_len)]

        #add last month
        self.add_event(user, f'Period - {calendar.month_name[current_month_int - 1]}', 'Period', last_curr_next_moth_flat_list[index_of_last_day], last_curr_next_moth_flat_list[index_of_last_day + per_len], last_dates)
        #add curr month
        self.add_event(user, f'Period - {calendar.month_name[current_month_int]}', 'Period', last_curr_next_moth_flat_list[index_of_next_start_day], last_curr_next_moth_flat_list[index_of_next_start_day + per_len], curr_dates)


    def set_period_arrived(self, user):
        pass


    def get_events_mothly_dict(self, user):
        user_events = self.load_events()[user]
        events_by_month = {}

        for event in user_events:
            period_dates_this_month = []
            period_dates_next_month = []

            if event['end_date']:
                _, start_month = event['start_date'].split('/')
                for item in event['notes']:
                    d, m = item.split('/')

                    if m == start_month:
                        period_dates_this_month.append(int(d))

                    elif int(m) == int(start_month) + 1:
                        period_dates_next_month.append(int(d))

                    else:
                        print('error here, not getting current or next month')

                keyword = 'Period' if event['type'] == 'Period' else event['title']
                events_by_month.setdefault(int(start_month), {}).setdefault(keyword, []).extend(period_dates_this_month)
                events_by_month.setdefault(int(start_month) + 1, {}).setdefault(keyword, []).extend(period_dates_next_month)

            else:
                keyword = event['title']
                day, month = event['start_date'].split('/')
                events_by_month.setdefault(int(month), {}).setdefault(keyword, [int(day)])


        return events_by_month

    def display_calendar_on_terminal(self, user) -> str:
        current_year = datetime.now().year
        c = calendar.Calendar()
        events_by_month_dict = self.get_events_mothly_dict(user)

        #dynamic syms
        symbols = ["*", "#", "@", "$", "%", "&", "+", "~"]
        event_symbol_map = {}  # event_name -> symbol

        for month_events in events_by_month_dict.values():
            for event_name in month_events.keys():
                if event_name not in event_symbol_map:
                    symbol = symbols[len(event_symbol_map) % len(symbols)]
                    event_symbol_map[event_name] = symbol

        output = ""

        for month in range(1, 13):
            output += f"\n---- {calendar.month_name[month]} {current_year} ----\n"
            output += "Mo Tu We Th Fr Sa Su\n"

            weeks_in_month = c.monthdayscalendar(current_year, month)
            month_events = events_by_month_dict.get(month, {})

            #map days to sym
            day_symbol_map = {}
            for event_name, days in month_events.items():
                for day in days:
                    day_symbol_map.setdefault(day, []).append(event_symbol_map[event_name])

            symbols_used_this_month = set()

            for week_days in weeks_in_month:
                week_display = []
                for day in week_days:
                    if day == 0:
                        week_display.append("    ")  #blank for empty days
                    elif day in day_symbol_map:
                        symbols_str = "".join(day_symbol_map[day])
                        symbols_used_this_month.update(day_symbol_map[day])
                        week_display.append(f"{day:2}{symbols_str}")
                    else:
                        week_display.append(f"{day:2}  ")  #two spaces if no event
                output += " ".join(week_display) + "\n"

            #legend for this month
            if symbols_used_this_month:
                output += "Legend:\n"
                for event_name, symbol in event_symbol_map.items():
                    if symbol in symbols_used_this_month:
                        output += f"{symbol}: {event_name}\n"

        return output
