import customtkinter as tk
import asyncio
import threading

tk.set_appearance_mode("System")

# Light/dark theme mappings
mappings = []
# format:
# [
#   {'object': object, 'light': [], 'dark': []}
# ]

# Create the main Tkinter window
root = tk.CTk()
root.title("Zen Explorer")
root.geometry("900x600")
root.minsize(600, 400)
root.configure(fg_color="white")
mappings.append({'object': root, 'light': {'fg_color': 'white'}, 'dark': {'fg_color': 'black'}})

# Sidebar
sidebar = tk.CTkFrame(root, width=200)
sidebar.configure(fg_color="#dddddd", corner_radius=0)
sidebar.pack_propagate(False)
sidebar.pack(side="left", fill="y")
mappings.append({'object': sidebar, 'light': {'fg_color': '#dddddd'}, 'dark': {'fg_color': '#222222'}})

# Main content
main_content = tk.CTkFrame(root)
main_content.configure(fg_color="white")
main_content.pack(side="right", fill="both", expand=True)
mappings.append({'object': main_content, 'light': {'fg_color': 'white'}, 'dark': {'fg_color': 'black'}})

# Label to display async messages
status_label = tk.CTkLabel(main_content, text="Status: Ready")
status_label.configure(text_color="black")
status_label.pack(pady=20)
mappings.append({'object': status_label, 'light': {'text_color': 'black'}, 'dark': {'text_color': 'white'}})

# Create a new asyncio event loop in a separate thread
loop = asyncio.new_event_loop()
asyncio_thread = threading.Thread(target=loop.run_forever, daemon=True)
asyncio_thread.start()

# Update
async def fetch_data():
    status_label.config(text="Fetching data...")
    await asyncio.sleep(2)  # Simulate async API call
    root.after(0, lambda: status_label.config(text="Data loaded!"))  # Update UI safely from the main thread

# Function to start async task
def run_async_task(task):
    asyncio.run_coroutine_threadsafe(task, loop)  # Schedule async function

# Sidebar button
def create_sidebar_button(parent, text, command):
    return tk.CTkButton(
        parent, text=text, command=command
    )

def update_theme_color():
    mode = tk.get_appearance_mode()
    is_dark = mode.lower() == "dark"

    for mapping in mappings:
        obj = mapping['object']
        obj.configure(**mapping['dark' if is_dark else 'light'])

    root.update()

    root.after(100, lambda: update_theme_color())

# Add button to trigger async task
btn = create_sidebar_button(sidebar, "Load Data", run_async_task)
btn.pack(fill="x", pady=5, padx=10, ipady=5)

update_theme_color()

# Start the Tkinter event loop
root.mainloop()

# Cleanup (stop the asyncio loop when Tkinter closes)
loop.stop()
