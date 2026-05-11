import flet as ft
import calendar
import datetime
from backend.log_manager import get_status
from backend.stats_engine import get_month_range, get_range_status

class HistoryCalendar(ft.Container):
    def __init__(self, habit_id):
        super().__init__(expand = True, padding = 5)
        self.habit_id = habit_id

        self.today = datetime.datetime.now()
        self.state = {
            "year": self.today.year,
            "month": self.today.month,
        }

        # Container used to hold calendar pages
        self.calendar_content = ft.Column(
            spacing = 0, 
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            width = 560
        )

        # Create a row that supports horizontal scrolling to enclose the content.
        self.content = ft.Row(
            controls = [self.calendar_content],
            scroll = ft.ScrollMode.AUTO,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            expand = True
        )

        self.build_calendar()
        

    # Determine the date status and return the color
    def get_status_dot(self, date_str):
        check_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        today_date = datetime.datetime.strptime(self.today.strftime("%Y-%m-%d"), "%Y-%m-%d")
        # future dates: don't show dots
        if check_date > today_date:
            return None
        
        status = get_range_status(self.habit_id, date_str, date_str)
        
        if status[0] == True:
            return "#58CD67"  # completed -> green
        elif status[0] == False:
            return "#F92828"  # missed -> red
        else:
            return "#888888"  # not_started -> gray


    def build_calendar(self):
        self.calendar_content.controls.clear()
        
        year = self.state["year"]
        month = self.state["month"]

        # month data
        month_list = calendar.monthcalendar(year, month)

        # title and navigation buttons
        month_name = calendar.month_name[month]
        header_row = ft.Row(
            controls=[
                ft.Row([
                    ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click = lambda _: self.change_date(y = -1)),
                    ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click = lambda _: self.change_date(m = -1)),
                ], spacing = 0),
                ft.Text(f"{month_name} {year}", size = 30, color = ft.Colors.BLACK, weight = "bold", width = 250, text_align = "center", expand = True),
                ft.Row([
                    ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click = lambda _: self.change_date(m = 1)),
                    ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT, on_click = lambda _: self.change_date(y = 1)),
                ], spacing = 0),
            ],
            alignment = ft.MainAxisAlignment.CENTER,
        )
        self.calendar_content.controls.append(header_row)
        self.calendar_content.controls.append(ft.Container(height = 10)) # 間距

        # container for calendar grid
        grid_body = ft.Column(spacing = 0)

        # week header
        days_header = ["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]
        
        week_head = ft.Row(
            controls=[
                ft.Container(
                    content = ft.Text(day, size = 16, weight = "bold", color = ft.Colors.BLACK),
                    width = 80, height = 40, alignment = ft.Alignment.CENTER,
                    border = ft.border.only(
                        bottom = ft.BorderSide(0.5, ft.Colors.BLACK26),
                        right = ft.BorderSide(0.5, ft.Colors.BLACK26))
                ) for day in days_header
            ],
            spacing = 0, 
            alignment = ft.MainAxisAlignment.CENTER
        )
        grid_body.controls.append(week_head)

        # date cells
        for week in range(0, len(month_list)):
            week_row = ft.Row(spacing = 0, alignment = ft.MainAxisAlignment.CENTER)
            for day in range(0, len(month_list[week])):
                # basic cell with date number and status dot
                content_stack = ft.Column(
                    controls=[ft.Text(str(month_list[week][day]) if month_list[week][day] != 0 else "", size=16, color = ft.Colors.BLACK)],
                    alignment = ft.MainAxisAlignment.START,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    spacing = 8
                )
                # check whether to add a status dot (only if there's a date, i.e., not 0)
                if month_list[week][day] != 0:
                    date_str = f"{year}-{month:02d}-{month_list[week][day]:02d}"
                    dot_color = self.get_status_dot(date_str)
                    if dot_color:
                        content_stack.controls.append(
                            ft.Container(
                                width = 12,
                                height = 12,
                                bgcolor = dot_color,
                                border_radius = 6
                            )
                        )

                day_box = ft.Container(
                    content = content_stack,
                    width = 80, height = 70,
                    border = ft.border.only(
                        bottom = ft.BorderSide(1, "black12"),
                        right = ft.BorderSide(1, "black12")
                    ),
                    padding = 10,
                    alignment = ft.Alignment.TOP_LEFT
                )
                week_row.controls.append(day_box)
            grid_body.controls.append(week_row)

        # add borders to the entire grid by wrapping it in another container
        grid_container = ft.Container(
            content = grid_body,
            border = ft.border.only(
                left = ft.BorderSide(1, "black12"),
                top = ft.BorderSide(1, "black12")
            )
        )

        # put grid_container into main Column
        self.calendar_content.controls.append(grid_container)
        self.calendar_content.controls.append(ft.Container(height = 20))
        
        # legend
        legend_row = ft.Row(
            controls = [
                ft.Row([ft.Container(width = 14, height = 14, border_radius = 7, bgcolor = "#58CD67"),
                        ft.Text(" : completed", size = 18, color = ft.Colors.BLACK)], alignment = ft.Alignment.TOP_LEFT),
                ft.Row([ft.Container(width = 14, height = 14, border_radius = 7, bgcolor = "#F92828"),
                        ft.Text(" : missed", size = 18, color = ft.Colors.BLACK)], alignment = ft.Alignment.TOP_LEFT),
                ft.Row([ft.Container(width = 14, height = 14, border_radius = 7, bgcolor = "#888888"),
                        ft.Text(" : not started", size = 18, color = ft.Colors.BLACK)], alignment = ft.Alignment.TOP_LEFT)
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            spacing = 90,
        )
        self.calendar_content.controls.append(legend_row) 


    def change_date(self, y = 0, m = 0):
        self.state["year"] += y
        self.state["month"] += m
        if self.state["month"] > 12: 
            self.state["month"] = 1
            self.state["year"] += 1
        elif self.state["month"] < 1: 
            self.state["month"] = 12
            self.state["year"] -= 1

        self.build_calendar()
        self.update()