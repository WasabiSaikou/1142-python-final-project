import flet as ft
import datetime
import re
import flet_charts as fch
from backend.stats_engine import get_current_streak, get_longest_streak, get_range_rate, get_range_status, get_week_range, get_month_range, get_create_date, get_cumulative_rate

class StatisticalChart(ft.Container):
    def __init__(self, habit_id, habit_name):
        super().__init__(padding = 10, alignment = ft.Alignment.TOP_CENTER)
        self.habit_id = habit_id
        self.habit_name = habit_name
        self.cur_streak = get_current_streak(self.habit_id)
        self.today = datetime.datetime.now()
        self.longest_streak = get_longest_streak(self.habit_id, get_create_date(self.habit_id), self.today.strftime("%Y-%m-%d"))

        # Build a container to put all contents in
        self.main_layout = ft.Column(scroll = ft.ScrollMode.ADAPTIVE,spacing = 20)
        self.content = self.main_layout
        self.stats_row_area = ft.Row(spacing = 10, alignment = ft.MainAxisAlignment.CENTER)

        # Line Chart Area
        self.chart_container = ft.Container(
            content = ft.Column(
                controls = [
                    ft.Text("Input a range to view progress chart", size = 16, weight = "bold", color = "black45"),
                    ft.Text("The scope is limited to 2020 to today.", size = 13, color = "black45")
                ],
                alignment = ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 5
            ),
            height = 300,
            padding = None,
            border = ft.border.all(1, ft.Colors.GREY_300),
            border_radius = 10,
            alignment = ft.Alignment.CENTER
        )

        # Create a custom date input row (not displayed by default).
        self.build_custom_date_row()
        self.build_ui_structure()


    def initial_load(self):
        # initialize interface
        date_range = get_week_range(self.today.strftime("%Y-%m-%d"))
        rate = get_range_rate(self.habit_id, date_range["start"], date_range["end"])
        statuses = get_range_status(self.habit_id, date_range["start"], date_range["end"])
        
        completed = sum(1 for s in statuses if s is True)
        total = sum(1 for s in statuses if s is not None)

        self.stats_row_area.controls = self.create_stat_card_controls(rate, completed, total, self.cur_streak)
        
        cumulative_rates = get_cumulative_rate(self.habit_id, date_range["start"], date_range["end"])
        self.update_line_chart(cumulative_rates, date_range["start"], date_range["end"])

        self.render_stats(date_range["start"], date_range["end"])


    def validate_dates(self):
        # Verify date format and validity
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        MIN_DATE = datetime.datetime(2020, 1, 1)  # Assuming the app starts in 2020
        MAX_DATE = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        
        def get_date_obj(date_str):
            if not re.match(date_pattern, date_str):
                return None
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                return None

        from_date_obj = get_date_obj(self.from_input.value)
        to_date_obj = get_date_obj(self.to_input.value)

        is_valid = False

        if from_date_obj and to_date_obj:
            if from_date_obj <= to_date_obj:
                if (from_date_obj <= MAX_DATE) and (from_date_obj >= MIN_DATE):
                    if (to_date_obj <= MAX_DATE) and (to_date_obj >= MIN_DATE):
                        is_valid = True
        
        self.apply_btn.disabled = not is_valid
        
        if self.page:
            self.update()


    def build_custom_date_row(self):
        # start date input
        self.from_input = ft.TextField(
                label = "Started date", 
                value = (self.today - datetime.timedelta(days = 7)).strftime("%Y-%m-%d"),
                dense = True, hint_text = "YYYY-MM-DD", expand = True,
                on_change = lambda _: self.validate_dates()
            )
        self.from_input_column = ft.Column(
            controls = [
                ft.Text("From", size = 12, weight = "bold", color = ft.Colors.BLACK),
                self.from_input
            ],
            spacing = 2, expand = True
        )
        
        # end date input
        self.to_input = ft.TextField(
            label = "End date", 
            value = self.today.strftime("%Y-%m-%d"),
            dense = True, hint_text = "YYYY-MM-DD", expand = True,
            on_change = lambda _: self.validate_dates()
        )
        self.to_input_column = ft.Column(
            controls = [
                ft.Text("To", size = 12, weight = "bold", color = ft.Colors.BLACK),
                self.to_input
            ],
            spacing = 2, expand = True
        )

        self.apply_btn = ft.ElevatedButton(
            "Apply", 
            on_click = self.handle_apply_click,
            expand = True,
            style = ft.ButtonStyle(
                shape = ft.RoundedRectangleBorder(radius = 5),
                # Background color setting
                color = {
                    ft.ControlState.DEFAULT: ft.Colors.RED_700,
                    ft.ControlState.DISABLED: ft.Colors.GREY_400,
                },
                bgcolor = {
                    ft.ControlState.DEFAULT: ft.Colors.RED_100,
                    ft.ControlState.DISABLED: ft.Colors.GREY_200,
                }
            )            
        )
        
        # Package date information into a row
        self.custom_date_area = ft.Row(
            controls = [
                ft.Container(content = self.from_input_column, padding = ft.padding.only(left = 10, right = 10),expand = 1, alignment = ft.Alignment.CENTER),
                ft.Container(content = self.to_input_column, padding = ft.padding.only(left = 10, right = 10), expand = 1, alignment = ft.Alignment.CENTER),
                ft.Container(content = self.apply_btn, padding = ft.padding.only(top = 18, left = 10, right = 10), expand = 1, height = 55),
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            visible = False # Initial hiding
        )
        

    # Interface structure
    def build_ui_structure(self):
        # Header
        header_row = ft.Row(
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            controls = [
                # habit name
                ft.Container(
                    content = ft.Row(
                        controls = [
                            ft.Text(
                                self.habit_name, 
                                size = 20, 
                                weight = "bold",
                                no_wrap = True,
                                color = ft.Colors.BLACK
                            )
                        ],
                        scroll = ft.ScrollMode.ADAPTIVE, 
                    ),
                    expand = True,
                    margin = ft.margin.only(right = 15) 
                ),
                # streak
                ft.Text(
                    f"{self.cur_streak}-day streak", 
                    size = 16, 
                    color = ft.Colors.GREY_700,
                    no_wrap = True
                )
            ]
        )
        header_container = ft.Container(
            content = header_row, 
            border = ft.border.only(bottom = ft.BorderSide(0.5, "black12")), 
            padding = ft.padding.only(bottom = 10, left = 10, right = 10) 
        )

        # Segmented Buttons
        self.mode_buttons = ft.SegmentedButton(
            selected = ["this week"],
            on_change = self.handle_mode_change,
            allow_empty_selection = False,
            allow_multiple_selection = False,
            show_selected_icon = False,
            expand = True,
            style = ft.ButtonStyle(
                shape = ft.RoundedRectangleBorder(radius = 5),
            ),
            segments = [
                ft.Segment(value = "this week", label = ft.Text("this week", color = ft.Colors.BLACK, text_align = ft.TextAlign.CENTER)),
                ft.Segment(value = "this month", label = ft.Text("this month", color = ft.Colors.BLACK, text_align = ft.TextAlign.CENTER)),
                ft.Segment(value = "Custom", label = ft.Text("Custom", color = ft.Colors.BLACK, text_align = ft.TextAlign.CENTER)),
            ],
        )
        buttons_row = ft.Row([self.mode_buttons])

        # put all elements into main_layout
        self.main_layout.controls.extend([
            header_container,
            buttons_row,
            self.custom_date_area,
            self.stats_row_area,
            ft.Text("Rate Over Time (Daily Completion Rate)", color = ft.Colors.BLACK, size = 16, weight = "bold"),
            self.chart_container
        ])


    def update_line_chart(self, rates_list, start_date_str, end_date_str):
        if not rates_list:
            self.chart_container.content = ft.Text("No data found for the selected range.", color = "black45")
            self.chart_container.border = ft.border.all(1, ft.Colors.GREY_300)
            self.chart_container.update()
            return

        # Date logic processing
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
        total_days = (end_date - start_date).days + 1
        
        # Calculate the X-axis label spacing -> Logic: dynamically adjust steps based on total number of days.
        if total_days <= 20:
            step = 1  # Show every day
        elif total_days <= 60:
            step = 5  # Show every 5 days
        elif total_days <= 120:
            step = 10 # Show every 10 days
        elif total_days <= 180:
            step = 15 # Show every 15 days
        else:
            step = 30 # Show every 30 days
            
        data_points = []
        x_axis_labels = []
            
        for i, val in enumerate(rates_list):
            # Create data point
            data_points.append(fch.LineChartDataPoint(x = i, y = round(val * 100, 1)))
            
            # Create X-axis labels
            if i % step == 0 or i == len(rates_list) - 1:
                current_date = start_date + datetime.timedelta(days = i)
                year_label = current_date.strftime("%Y")
                date_label = current_date.strftime("%m/%d")
                x_axis_labels.append(
                    fch.ChartAxisLabel(
                        value = i,
                        label = ft.Container(
                            content = ft.Column(
                                controls = [
                                    ft.Text(year_label, size = 9, color = "black38", weight = "bold"),
                                    ft.Text(date_label, size = 10, color = "black54", weight = "bold"),
                                ],
                                spacing = 2,
                                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                            ),
                            padding = ft.padding.only(top = 10) 
                        )
                    )
                )

        # Build chart
        chart = fch.LineChart(
            data_series = [
                fch.LineChartData(
                    points = data_points,
                    stroke_width = 3,
                    color = ft.Colors.RED_400,
                    below_line_bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.RED_400),
                    selected_below_line = True,
                    rounded_stroke_cap = True
                )
            ],
            border = ft.border.all(1, ft.Colors.BLACK12),
            # y-axis setting
            left_axis = fch.ChartAxis(
                label_spacing = 25,
                labels = [
                    fch.ChartAxisLabel(value = 0, label = ft.Text("0.0%", size = 11, color = ft.Colors.BLACK)),
                    fch.ChartAxisLabel(value = 25, label = ft.Text("25.0%", size = 11, color = ft.Colors.BLACK)),
                    fch.ChartAxisLabel(value = 50, label = ft.Text("50.0%", size = 11, color = ft.Colors.BLACK)),
                    fch.ChartAxisLabel(value = 75, label = ft.Text("75.0%", size = 11, color = ft.Colors.BLACK)),
                    fch.ChartAxisLabel(value = 100, label = ft.Text("100.0%", size = 11, color = ft.Colors.BLACK)),
                ],
                label_size = 45,
            ),
            # x-axis setting (dynamic label)
            bottom_axis = fch.ChartAxis(
                labels = x_axis_labels,
                label_size = 20,
            ),
            horizontal_grid_lines = fch.ChartGridLines(interval = 25, color = ft.Colors.GREY_300, width = 1),
            min_y = 0,
            max_y = 100,
            expand = True
        )

        self.chart_container.padding = ft.padding.only(left = 0, right = 20, top = 50, bottom = 20)
        self.chart_container.border = None
        self.chart_container.content = chart
        
        if self.page:
            self.chart_container.update()


    def create_stat_card_controls(self, rate, completed, total, longest_streak):
        def build_single_card(title, value):
            return ft.Container(
                content = ft.Column([
                    ft.Text(title, size = 14, color = ft.Colors.GREY_700),
                    ft.Text(value, size = 24, weight = "bold", color = ft.Colors.BLACK),
                ], alignment = "center", horizontal_alignment = "center"),
                border = ft.border.all(1, ft.Colors.GREY_400),
                border_radius = 5,
                padding = ft.padding.only(top = 10, bottom = 10),
                expand = 1
            )
        
        return [
            build_single_card("Overall Rate", f"{rate:.1%}"),
            build_single_card("Completed Days", f"{completed} / {total}"),
            build_single_card("Longest Streak", f"{longest_streak} days"),
        ]


    def handle_mode_change(self, e):
        mode = e.data if isinstance(e.data, str) else list(e.data)[0]
        
        # Control the display/hide of the date input box
        self.custom_date_area.visible = (mode == "Custom")

        if mode != "Custom":
            self.load_stats_by_mode(mode)
        else:
            self.from_input.value = ""
            self.to_input.value = ""
            self.apply_btn.disabled = True

            self.render_custom_initial_stats()

            self.chart_container.content = ft.Column(
                controls = [
                    ft.Text("Input a range to view progress chart", color = "black45", size = 16, weight = "bold"),
                    ft.Text("The scope is limited to 2020 to today.", color = "black38", size = 13),
                ],
                alignment = ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 5
            )
            self.chart_container.border = ft.border.all(1, ft.Colors.GREY_300)
            self.chart_container.alignment = ft.Alignment.CENTER
            self.chart_container.padding = None

            if self.page:
                self.update()


    def handle_apply_click(self, e):
        start_date = self.from_input.value
        end_date = self.to_input.value
        self.render_stats(start_date, end_date)


    def load_stats_by_mode(self, mode):
        if mode == "this week":
            date_range = get_week_range(self.today.strftime("%Y-%m-%d"))
        else:     # this month
            date_range = get_month_range(self.today.strftime("%Y-%m-%d"))

        self.render_stats(date_range["start"], date_range["end"])


    def render_stats(self, start_date, end_date):
        rate = get_range_rate(self.habit_id, start_date, end_date)
        statuses = get_range_status(self.habit_id, start_date, end_date)
        
        completed = sum(1 for s in statuses if s is True)
        total = sum(1 for s in statuses if s is not None)

        longest_streak = get_longest_streak(self.habit_id, start_date, end_date)

        # Update card content
        new_cards = self.create_stat_card_controls(rate, completed, total, longest_streak)
        self.stats_row_area.controls = new_cards
        
        # Get cumulative data and render a chart
        cumulative_rates = get_cumulative_rate(self.habit_id, start_date, end_date)
        # calculate the x-axis interval
        self.update_line_chart(cumulative_rates, start_date, end_date)
        
        if self.page:
            self.update()


    # initial render    
    def render_custom_initial_stats(self):
        def build_single(title, value):
            return ft.Container(
                content = ft.Column([
                    ft.Text(title, size = 14, color = ft.Colors.GREY_700),
                    ft.Text(value, size = 24, weight = "bold", color = ft.Colors.BLACK),
                ], alignment="center", horizontal_alignment = "center"),
                border = ft.border.all(1, ft.Colors.GREY_400),
                border_radius = 5,
                expand = 1,
                padding = ft.padding.only(top = 10, bottom = 10)
            )
            
        initial_cards = [
            build_single("Overall Rate", "0.0%"),
            build_single("Completed Days", "0 / 0"),
            build_single("Longest Streak", "0 days"),
        ]
        
        self.stats_row_area.controls = initial_cards

    
    def did_mount(self):
        self.initial_load()