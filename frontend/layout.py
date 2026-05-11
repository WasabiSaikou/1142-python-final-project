import flet as ft
from frontend.statistics import StatisticView
from frontend.history import HistoryView
from frontend.dashboard import DashboardView

class AppLayout(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__(expand = True, spacing = 0)

        # save all visited Container
        self.nav_items_list = []

        # right content area, initially set to DashboardView
        self.content_area = ft.Container(
            alignment = ft.Alignment.TOP_LEFT,
            expand = True,
            padding = ft.padding.only(bottom = 5),
            bgcolor = "#F5F1EB",
            content = DashboardView()
        )

        # left menu area
        # create guide objects
        dashboard_item = self.nav_item(ft.Icon(ft.Icons.DASHBOARD, color = ft.Colors.BLACK), "Dashboard")
        statistics_item = self.nav_item(ft.Icon(ft.Icons.INSERT_CHART, color = ft.Colors.BLACK), "Statistics")
        history_item = self.nav_item(ft.Icon(ft.Icons.HISTORY, color = ft.Colors.BLACK), "History")

        self.sidebar = ft.Container(
            width = 250,
            bgcolor = "#F5EBDB",
            border = ft.border.only(right = ft.BorderSide(1, "#B0ABAB")),
            
            content = ft.Column(
                spacing = 0,
                controls = [
                    ft.Container(   # Title : MENU
                        content = ft.Text("MENU", size = 40, weight = "bold", color = ft.Colors.BLACK),
                        padding = ft.padding.only(top = 30, bottom = 30, left = 40)
                    ),
                    ft.Container(   # Intermediate function list
                        width = 250,
                        expand = True,
                        padding = ft.padding.all(10),
                        content = ft.Column(
                            scroll=ft.ScrollMode.AUTO,
                            expand = True,
                            spacing = 5,
                            controls = [dashboard_item, statistics_item, history_item]
                        )
                    )
                ]
            )
        )

        self.set_initial_nav("Dashboard")
        # put sidebar and content in a Row
        self.controls = [self.sidebar, self.content_area]

    # initial item
    def set_initial_nav(self, label):
        for item in self.nav_items_list:
            if item.data == label:
                item.bgcolor = "black12"
            else:
                item.bgcolor = None

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
                title = ft.Text(label, size = 20, weight = "w500", color = ft.Colors.BLACK),
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
            self.content_area.content = DashboardView()
        elif clicked_label == "Statistics":
            self.content_area.content = StatisticView()
        elif clicked_label == "History":
            self.content_area.content = HistoryView()

        # update content
        self.content_area.update()