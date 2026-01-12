import threading
import time
import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Grind Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    # A dictionary to store the state of every task
    task_states = {}

    # Mobile-friendly timer
    def run_timer(seconds, message):
        # Update text
        status_text.value = f"⏳ Timer started: {int(seconds/60)} mins"
        page.update()
        
        # Wait
        time.sleep(seconds)
        
        # 1. Play a sound (Optional - adds a nice "Ding")
        # We add an invisible audio player to the page
        audio1 = ft.Audio(src="https://luna-1.divorce-online.co.uk/audio/alert.mp3", autoplay=True)
        page.overlay.append(audio1)
        
        # 2. Show a SnackBar (Mobile friendly notification)
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"⏰ {message}", size=20),
            bgcolor=ft.Colors.RED_700,
            open=True  # This forces it to pop up
        )
        
        # Reset text
        status_text.value = "✅ Timer Finished!"
        page.update()

    # Button click handler
    def start_coding_timer(e):
        # 25 minutes = 1500 seconds (Pomodoro style)
        # We run this in a thread so the app doesn't freeze
        t = threading.Thread(target=run_timer, args=(1500, "Coding Session Done! Take a break."))
        t.start()

    # Tasks for each mode
    tasks_short_day = [
        "Power Workout (3:30 PM)",
        "Deep Coding Session (4:30 PM)",
        "Review Japanese (Night)",
        "Esports Scrims (9:00 PM)"
    ]

    tasks_long_day = [
        "Recharge & Snack (5:30 PM)",
        "Quick Study / Review (6:30 PM)",
        "Light Stretch (7:30 PM)",
        "Esports Scrims (9:00 PM)"
    ]

    tasks_holiday = [
        "Heavy Workout (8:00 AM)",
        "Deep Coding (10:00 AM - 12:00 PM)",
        "Japanese Writing (12:00 PM)",
        "Afternoon Gaming (2:00 PM)",
        "Farm Help / Review (4:00 PM)",
        "Esports Scrims (8:30 PM)"
    ]

    # Function to change the list based on button click
    def set_mode(e, mode):
        # SAVE STATE: Before clearing, save current checkboxes to the dictionary
        for control in task_list.controls:
            if isinstance(control, ft.Checkbox):
                task_states[control.label] = control.value

        # Clear the old list
        task_list.controls.clear()
        
        # Select the new list of tasks
        if mode == "Short":
            current_tasks = tasks_short_day
        elif mode == "Long":
            current_tasks = tasks_long_day
        else:
            current_tasks = tasks_holiday

        # RESTORE STATE: Create new checkboxes, checking memory for saved values
        for task in current_tasks:
            # .get(task, False) means: "Get the saved value, or default to False if new"
            is_checked = task_states.get(task, False) 
            task_list.controls.append(ft.Checkbox(label=task, value=is_checked))
        
        status_text.value = f"Mode set to: {mode}"
        page.update()

    # UI Elements
    status_text = ft.Text(value="Select your day type:", size=20, weight="bold")
    
    btn_short = ft.ElevatedButton(
        content=ft.Text("Home by 3:00 PM", color=ft.Colors.WHITE),
        on_click=lambda e: set_mode(e, "Short"),
        bgcolor=ft.Colors.GREEN_400
    )
    
    btn_long = ft.ElevatedButton(
        content=ft.Text("Home by 5:30 PM", color=ft.Colors.WHITE),
        on_click=lambda e: set_mode(e, "Long"),
        bgcolor=ft.Colors.RED_400
    )

    btn_holiday = ft.ElevatedButton(
        content=ft.Text("Holiday / Home", color=ft.Colors.WHITE),
        on_click=lambda e: set_mode(e, "Holiday"),
        bgcolor=ft.Colors.BLUE_400
    )

    task_list = ft.Column()

    # Layout
    # Layout
    page.add(
        ft.Column(
            [
                status_text,
                ft.Row([btn_short, btn_long, btn_holiday], alignment=ft.MainAxisAlignment.CENTER),
                
                # --- NEW TIMER BUTTON ---
                # --- NEW TIMER BUTTON ---
                ft.Divider(),
                ft.ElevatedButton(
                    content=ft.Text("Start 25m Coding Timer", size=16),
                    icon="timer",  # We used the string "timer" instead of ft.icons.TIMER
                    on_click=start_coding_timer,
                    bgcolor=ft.Colors.ORANGE_700,
                    color=ft.Colors.WHITE
                ),
                # ------------------------

                ft.Divider(),
                ft.Text("Your Mission:", size=16),
                task_list
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)