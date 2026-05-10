import flet as ft
import datetime
import calendar
from backend.habit_manager import get_all_habits, add_habit, delete_habit
from backend.stats_engine import get_range_status, get_week_range, get_current_streak, get_range_rate
from backend.log_manager import get_status, toggle_check

class DashboardView(ft.Container):
    def __init__(self):
        super().__init__(expand = True, padding = 0)

        # Initial data and status
        self.habit_list = get_all_habits()

        # date information
        self.today = datetime.datetime.now()
        self.weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.state = {
            "year": self.today.year,
            "month": self.today.month,
            "day" :self.today.day
        }
        
        # dashboard content
        self.habit_items_column = ft.Column(
            expand = True,
            spacing = 10,
            scroll = ft.ScrollMode.AUTO,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )

        # Create a pop-up input box (AlertDialog)
        self.new_habit_name_tf = ft.TextField(
            label = "Habit Name", 
            autofocus = True,
            max_length = 100,
        )

        self.add_habit_dialog = ft.AlertDialog(
            title = ft.Text("Add New Habit"),
            content = ft.Container(
                expand = True,
                padding = ft.padding.only(left = 10, right = 10),
                width = 350,
                height = 200,
                content = ft.Column(
                    controls = [
                        ft.Text("Please enter your new habit name in the input box below."),
                        self.new_habit_name_tf
                    ]
                )
            ),       
            actions = [
                ft.TextButton("Cancel", on_click = self.close_dialog),
                ft.TextButton("Confirm", on_click = self.confirm_add_habit),
            ],
            open = False,
            bgcolor = "#F6EFE5",
            content_padding = ft.Padding.only(left = 20, right = 20, top = 20),
        )
        
        # Initialize the layout
        self.build_dashboard()


    def build_dashboard(self):
        # Title
        year = self.today.year
        month = self.today.month
        day = self.today.day
        weekday_name = self.weekday[calendar.weekday(year, month, day)]
        month_name = calendar.month_name[month]

        def handle_hover(e):
            if e.control.bgcolor != "black12":
                e.control.bgcolor = "black12" if e.data == "true" else None
                e.control.update()

        self.title_row = ft.Container(
            padding = ft.padding.only(left = 25, top = 20, bottom = 20, right = 25),
            border=ft.border.only(bottom = ft.BorderSide(0.5, "black12")),
            bgcolor = "#F6EFE5",
            content = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                controls = [
                    ft.Column([
                        ft.Text("Dashboard", size = 30, weight = "bold"),
                        ft.Text(f"{weekday_name}, {month_name} {day}, {year}", size = 15, color = "black54", weight = "bold")
                    ], spacing=5),
                    # New Habit Button
                    ft.Container(
                        content = ft.Row([
                            ft.Icon(ft.Icons.ADD, size = 20),
                            ft.Text("New Habit", size = 18, weight = "w500")
                        ], spacing = 10),
                        padding = ft.padding.all(10),
                        border = ft.border.all(1, "black12"),
                        bgcolor = None,
                        border_radius = 8,
                        ink = True,
                        ink_color = "black12",
                        on_click = lambda e: self.page.show_dialog(self.add_habit_dialog),
                        on_hover = handle_hover,
                    )
                ]
            )
        )

        self.dashboard_content = ft.Container(
            content = self.habit_items_column,
            padding = ft.padding.all(25),
            expand = True
        )

        # combine
        self.content = ft.Column(
            expand = True,
            spacing = 0,
            controls = [
                self.title_row,
                self.dashboard_content
                
            ]
        )

    # create a habit information box
    def create_habit_dashboard(self, habit_data):
        weekday = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]

        habit_id = habit_data["id"]
        habit_name = habit_data["name"]
        current_streak = get_current_streak(habit_id)

        habit_card = ft.Container(
            padding = ft.padding.only(left = 20, right = 20, top = 15, bottom = 15),
            border = ft.border.all(1, "black26"),
            border_radius = 5,
            bgcolor = "#F7F4EF",
            content = ft.Column(
                spacing = 5,
                expand = True,
                controls = [
                    ft.Row(
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        controls = [
                            # habit name
                            ft.Container(
                                content = ft.Row(
                                    controls = [
                                        ft.Text(
                                            habit_name, 
                                            size = 20, 
                                            weight = "bold", 
                                            no_wrap = True
                                        )
                                    ],
                                    scroll = ft.ScrollMode.ADAPTIVE,
                                ),
                                expand = True,
                                margin = ft.margin.only(right = 10)
                            ),
                            # streak and delete button
                            ft.Row(
                                controls = [
                                    ft.Text(f"{current_streak}-day streak", color = "black54", weight = "bold", no_wrap=True),
                                    ft.IconButton(
                                        ft.Icons.DELETE, 
                                        icon_color = "black54", 
                                        on_click = lambda e: self.handle_delete(habit_data)
                                    )
                                ],
                                spacing = 10
                            )
                        ]
                    ),
                    ft.Row(
                        controls = [
                            ft.Container(
                                content = ft.ProgressBar(
                                    value = self.get_progress(habit_id),
                                    color = "#7BA753",
                                    bgcolor = "black12",
                                    height = 8,
                                    border_radius = 4
                                ),
                                expand = True,
                            ),
                            # Show percentage 
                            ft.Text(f"{int(self.get_progress(habit_id) * 100)} %", size = 16, weight = "bold", color = "black87")
                        ],
                        alignment = ft.MainAxisAlignment.CENTER,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        spacing = 25
                    ),
                    ft.Row(
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing = 10,
                        controls = [
                            ft.Row(
                                controls = [self.build_card(d, weekday[d], habit_id) for d in range(0, len(weekday))],
                                spacing = 10, 
                                alignment = ft.MainAxisAlignment.START
                            ),
                            ft.Checkbox(
                                value = get_status(habit_id, f"{self.today.year}-{self.today.month:02d}-{self.today.day:02d}") == True,
                                on_change = lambda e: self.handle_check_click(habit_id)
                            )
                        ]
                    )
                ]
            )
        )
        return habit_card


    def close_dialog(self, e):
        self.add_habit_dialog.open = False
        self.new_habit_name_tf.value = ""
        self.page.update()

    def confirm_add_habit(self, e):
        new_name = self.new_habit_name_tf.value.strip()
        if new_name:
            add_habit(new_name)
            self.habit_list = get_all_habits()
            self.refresh_habit_list()
            self.close_dialog(e)

    def handle_delete(self, habit_data):
        self.habit_list.remove(habit_data)
        delete_habit(habit_data['id'])
        self.refresh_habit_list()

    def get_progress(self, habit_id):
        week_range = get_week_range(str(self.today.strftime("%Y-%m-%d")))
        return get_range_rate(habit_id, week_range["start"], week_range["end"])

    def build_card(self, index, day, habit_id):
        week_range = get_week_range(str(self.today.strftime("%Y-%m-%d")))  
        weekly_status = get_range_status(habit_id, week_range["start"], week_range["end"])
        status = weekly_status[index]

        return ft.Container(
            content = ft.Text(day, size = 16),
            width = 60, height = 45,
            border = ft.border.all(1, "black38"),
            border_radius = 5,
            alignment = ft.Alignment.CENTER,
            bgcolor = "#7BA753" if status == True else "#DC3F3F" if status == False else None
        )
    
    def handle_check_click(self, habit_id):
        toggle_check(habit_id, self.today.strftime("%Y-%m-%d"))
        self.refresh_habit_list()


    # logic function
    def refresh_habit_list(self):
        self.habit_list = get_all_habits()
        self.habit_items_column.controls.clear()
        
        if not self.habit_list:
        # If empty, add guiding text.
            self.habit_items_column.controls.append(
                ft.Container(
                    content = ft.Text(
                        "Let's add a new habit.", 
                        size = 20, 
                        color = "black45",
                        weight = "w500"
                    ),
                    alignment = ft.Alignment.CENTER,
                )
            )
        else:
            for h in self.habit_list:
                card = self.create_habit_dashboard(h)
                self.habit_items_column.controls.append(card)
                
        if self.page:
            self.update()


    # 
    def did_mount(self):
        # 此時 self.page 已經存在，可以安全地執行重新整理
        self.refresh_habit_list()
        # 如果你之後需要用到對話框，確保它已經被關聯到 page 上
        self.page.dialog = self.add_habit_dialog 
        self.page.update()