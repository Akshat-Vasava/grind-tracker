import flet as ft
import time
import threading

def main(page: ft.Page):
    page.title = "Grind Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window_width = 400
    page.window_height = 700

    # --- DATA & STATE MANAGEMENT ---
    # 1. Try to load saved data from the phone's memory
    saved_tasks = page.client_storage.get("task_states")
    if saved_tasks is None:
        saved_tasks = {} # If no data, start fresh

    # 2. Lists of tasks
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

    # --- UI ELEMENTS ---
    status_text = ft.Text(value="Select your day type:", size=20, weight="bold")
    task_list = ft.Column()
    progress_bar = ft.ProgressBar(width=400, color="amber", bgcolor="#222222", value=0)
    
    # --- LOGIC FUNCTIONS ---
    
    def save_data():
        """Saves current checkboxes to phone memory"""
        page.client_storage.set("task_states", saved_tasks)
        update_progress()

    def update_progress():
        """Calculates % completion"""
        if not task_list.controls:
            progress_bar.value = 0
            return
            
        total = len(task_list.controls)
        checked = 0
        for control in task_list.controls:
            if isinstance(control, ft.Checkbox) and control.value:
                checked += 1
        
        progress = checked / total if total > 0 else 0
        progress_bar.value = progress
        page.update()

    def checkbox_changed(e):
        """When a box is clicked, save it immediately"""
        saved_tasks[e.control.label] = e.control.value
        save_data()

    def set_mode(e, mode):
        # Clear old list
        task_list.controls.clear()
        
        # Decide which list to load
        if mode == "Short":
            current_tasks = tasks_short_day
            status_text.value = "Mode: Home by 3:00 PM"
        elif mode == "Long":
            current_tasks = tasks_long_day
            status_text.value = "Mode: Home by 5:30 PM"
        else:
            current_tasks = tasks_holiday
            status_text.value = "Mode: Holiday / Home"

        # Build checkboxes
        for task in current_tasks:
            # Check if we have a saved state for this task
            is_checked = saved_tasks.get(task, False)
            
            task_list.controls.append(
                ft.Checkbox(
                    label=task, 
                    value=is_checked, 
                    on_change=checkbox_changed
                )
            )
        
        # Save the mode so app remembers next time
        page.client_storage.set("last_mode", mode)
        update_progress()
        page.update()

    def run_timer(seconds, message):
        """Mobile friendly timer with SnackBar"""
        status_text.value = f"⏳ Timer: {int(seconds/60)} mins"
        page.update()
        
        time.sleep(seconds)
        
        # Play generic system sound (if browser allows) and show popup
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"⏰ {message}", size=20),
            bgcolor=ft.Colors.GREEN_700,
            open=True
        )
        status_text.value = "✅ Timer Finished!"
        page.update()

    def start_coding_timer(e):
        # 25 mins = 1500 seconds
        t = threading.Thread(target=run_timer, args=(1500, "Coding Session Done!"))
        t.start()

    # --- BUTTONS ---
    btn_short = ft.ElevatedButton(
        content=ft.Text("Short Day", color=ft.Colors.WHITE),
        on_click=lambda e: set_mode(e, "Short"),
        bgcolor=ft.Colors.GREEN_400
    )
    
    btn_long = ft.ElevatedButton(
        content=ft.Text("Long Day", color=ft.Colors.WHITE),
        on_click=lambda e: set_mode(e, "Long"),
        bgcolor=ft.Colors.RED_400
    )
    
    btn_holiday = ft.ElevatedButton(
        content=ft.Text("Holiday", color=ft.Colors.WHITE),
        on_click=lambda e: set_mode(e, "Holiday"),
        bgcolor=ft.Colors.BLUE_400
    )

    # --- BUILD PAGE ---
    page.add(
        ft.Column(
            [
                status_text,
                progress_bar, # Added progress bar
                ft.Row([btn_short, btn_long, btn_holiday], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Divider(),
                ft.ElevatedButton(
                    content=ft.Text("Start 25m Focus Timer", size=16),
                    icon="timer",
                    on_click=start_coding_timer,
                    bgcolor=ft.Colors.ORANGE_700,
                    color=ft.Colors.WHITE
                ),

                ft.Divider(),
                ft.Text("Your Mission:", size=16),
                task_list
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # --- AUTO-LOAD LAST SESSION ---
    # When app opens, check if we remember the last mode
    last_mode = page.client_storage.get("last_mode")
    if last_mode:
        set_mode(None, last_mode)

ft.app(target=main)
