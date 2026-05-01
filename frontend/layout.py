import flet as ft
from frontend.statistics import StatisticView
from frontend.history import HistoryView
from frontend.dashboard import DashboardView


class AppLayout(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__(expand = True, spacing = 0)

        # save all visited Container
        self.nav_items_list = []

        # right content area
        self.content_area = ft.Container(
            alignment = ft.Alignment.TOP_LEFT,
            expand = True,
            padding = ft.padding.only(bottom = 5),
            bgcolor = "#F5F1EB",
            content = ft.Column(
                controls = [
                    ft.Text("Dashboard", size = 30, weight = "bold"),
                    ft.Text("date", size = 15)
                ]
            )
        )

        # left menu area
        # create guide objects
        dashboard_item = self.nav_item(ft.Icon(ft.Icons.DASHBOARD), "Dashboard")
        statistics_item = self.nav_item(ft.Icon(ft.Icons.INSERT_CHART), "Statistics")
        history_item = self.nav_item(ft.Icon(ft.Icons.HISTORY), "History")
        setting_item = self.nav_item(ft.Icon(ft.Icons.SETTINGS), "Setting")

        self.sidebar = ft.Container(
            width = 210,
            bgcolor = "#F5EBDB",
            border = ft.border.only(right = ft.BorderSide(1, "#B0ABAB")),
            
            content = ft.Column(
                spacing = 0,
                controls = [
                    ft.Container(   # Title : MENU
                        content = ft.Text("MENU", size = 35, weight = "bold"),
                        padding = ft.padding.only(top = 30, bottom = 30, left = 20)
                    ),
                    ft.Container(   # Intermediate function list
                        width = 210,
                        expand = True,
                        padding = ft.padding.all(10),
                        content = ft.Column(
                            scroll=ft.ScrollMode.AUTO,
                            expand = True,
                            spacing = 5,
                            controls = [dashboard_item, statistics_item, history_item]
                        )
                    ),
                    ft.Container(   # Setting button
                        content = setting_item,
                        padding = ft.padding.only(bottom = 20, top = 15, left = 10, right = 10),
                    ),
                ]
            )
        )

        # put sidebar and content in a Row
        self.controls = [self.sidebar, self.content_area]


    # layout item definition
    def nav_item(self, icon_name, label):
        # Change bgcolor when hovering
        def on_hover_container(e):
            if e.control.bgcolor != "black12":
                e.control.bgcolor = "black12" if e.data == "true" else None
                e.control.update()
        
        nav_container =  ft.Container(
            border_radius = 5,
            data = label,
            on_hover = on_hover_container,
            margin = ft.margin.symmetric(horizontal = 10, vertical = 2),
            content=ft.ListTile(
                leading = icon_name,
                title = ft.Text(label, size = 14, weight = "w500"),
                on_click = self.on_nav_change,
                data = label,
            )
        )
        self.nav_items_list.append(nav_container)
        return nav_container
    

    def on_nav_change(self, e):
        # retrieve the clicked data from ListTile
        clicked_label = e.control.data

        # iterate through the list and update the bgcolor of all buttons
        for item in self.nav_items_list:
            if item.data == clicked_label:
                item.bgcolor = "black12"
            else:
                item.bgcolor = None
            item.update()

        # update content based on the clicked item
        if clicked_label == "Dashboard":
            self.content_area.content = ft.Text("Dashboard Content", size=30)
        elif clicked_label == "Statistics":
            self.content_area.content = StatisticView()
        elif clicked_label == "History":
            self.content_area.content = HistoryView()
        elif clicked_label == "Setting":
            self.content_area.content = ft.Text("Settings", size=30)

        # update content
        self.content_area.update()