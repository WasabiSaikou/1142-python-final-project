import flet as ft
from backend.habit_manager import get_all_habits
from frontend.calender import HistoryCalendar

class HistoryView(ft.Container):
    def __init__(self):
        super().__init__(expand = True, padding = 0)
        
        # save all visited Container
        self.hist_items_list = []        
        self.habit_list = get_all_habits()
        
        # right side : detail of history
        self.hist_detail = ft.Container(
            padding = 15,
            expand = True,
            content = ft.Text("Select a habit to see details", size = 20, color = "grey"),
            alignment = ft.Alignment.TOP_CENTER
        )       
        
        # A prompt when there is no custom data
        if not self.habit_list:
            self.hist_detail.content = ft.Text("No habits were established.", size = 20, color = "grey")
        else:
            # Build sidebar projects
            sidebar_controls = [self.hist_nav_item(habit) for habit in self.habit_list]
            # Initialization the calendar
            first_habit = self.habit_list[0]
            self.hist_detail.content = self.create_detail_content(first_habit["id"])
            sidebar_controls[0].bgcolor = "black12" # Set the first one as the selected state    

        # left side : sidebar of hostory
        self.hist_sidebar = ft.Container(
            width = 250,
            alignment = ft.Alignment.TOP_LEFT,
            padding = 0,
            bgcolor = "#F5EFE6",
            border = ft.border.only(right = ft.BorderSide(0.5, "black12")),
            content = ft.Column(
                spacing = 0,
                controls = [
                    # SELECT HABIT
                    ft.Container(                        
                        content = ft.Text("SELECT HABIT", size = 13, weight = "bold", color = "#807E7C"),
                        padding = ft.padding.only(top = 20, bottom = 10, left = 10)
                    ),
                    ft.Container(
                        expand = True,
                        padding = ft.padding.only(left = 5, right = 5),
                        content = ft.Column(
                            # controls = [self.hist_nav_item(name) for name in habit_info],
                            controls = sidebar_controls,
                            scroll = ft.ScrollMode.AUTO,
                            spacing = 5
                        )
                    ) 
                ]
            )
        )

        # all contents of History
        self.content = ft.Column(
            expand = True,
            spacing = 0,
            controls=[
                # Title : History
                ft.Container(
                    width = 1400,
                    bgcolor = "#F6EFE5",
                    padding = ft.padding.only(left = 25, top = 20, bottom = 20),
                    border = ft.border.only(bottom = ft.BorderSide(0.5, "black12")),
                    content = ft.Column([
                        ft.Text("History", size = 30, weight = "bold"),
                        ft.Text("Review your daily progress.", size = 15),
                    ], spacing = 5)
                ),

                # Content (left -> sidebar ; right -> history of the chosen habit)
                ft.Row(
                    expand = True,
                    spacing = 0,
                    vertical_alignment = ft.CrossAxisAlignment.START,
                    controls = [
                        self.hist_sidebar,
                        self.hist_detail
                    ]
                )
            ]
        )


    def create_detail_content(self, habit_id):
        # send ID to build calendar elements
        return ft.Column(
            controls = [HistoryCalendar(habit_id = habit_id)], 
            scroll = ft.ScrollMode.AUTO, 
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )


    def hist_nav_item(self, habit_dict):
        # Generate member entries
        def handle_hover(e):
            if e.control.bgcolor != "black12":
                e.control.bgcolor = "black12" if e.data == "true" else None
                e.control.update()

        nav_item = ft.Container(
            on_click = self.hist_on_nav_change,
            on_hover = handle_hover,
            data = habit_dict,
            padding = ft.padding.symmetric(horizontal = 10, vertical = 12),
            border_radius = 5,
            ink = True,
            ink_color = "black12",

            content = ft.Row(
                vertical_alignment = ft.CrossAxisAlignment.START,
                controls = [
                    ft.Icon(ft.Icons.EVENT, size = 20, color = "#807E7C"),
                    ft.Text(
                        value = habit_dict["name"],
                        size = 16,
                        color = "black87",
                        overflow = ft.TextOverflow.VISIBLE, # Ensure that line breaks are not truncated
                        no_wrap = False,
                        expand = True
                    )    
                ]
            )
        )
        # Store the items in a list for later iteration and updates
        self.hist_items_list.append(nav_item)
        return nav_item


    def hist_on_nav_change(self, e):
        # Get click habit dictionary
        habit_info = e.control.data
        clicked_id = habit_info["id"]

        # Update sidebar background color
        for item in self.hist_items_list:
            item.bgcolor = "black12" if item.data["id"] == clicked_id else None
            item.update()

        # Update the calendar on the right
        self.hist_detail.content = self.create_detail_content(clicked_id)
        self.hist_detail.update()