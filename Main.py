import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


# =========================================================
# FILE SETTINGS
# =========================================================

DATA_FILE = "lost_found_data.json"


# =========================================================
# DATA FUNCTIONS
# =========================================================

def load_data():
    """Load records from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_data(records):
    """Save records to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)


records = load_data()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("College Lost & Found Manager")
root.geometry("950x650")
root.minsize(850, 600)


# =========================================================
# COLORS
# =========================================================

BG = "#F4F7FB"
NAVY = "#1F3A5F"
BLUE = "#2F6FED"
LIGHT_BLUE = "#EAF1FF"
GREEN = "#2E9D68"
LIGHT_GREEN = "#E8F7EF"
ORANGE = "#E8912D"
LIGHT_ORANGE = "#FFF2DF"
RED = "#D9534F"
WHITE = "#FFFFFF"
DARK = "#263238"
GRAY = "#667085"


root.configure(bg=BG)


# =========================================================
# STYLE
# =========================================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=DARK,
    rowheight=32,
    fieldbackground=WHITE,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=NAVY,
    foreground=WHITE,
    font=("Arial", 10, "bold")
)

style.map(
    "Treeview",
    background=[("selected", BLUE)],
    foreground=[("selected", WHITE)]
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def create_button(parent, text, command, color=BLUE, width=20):
    """Create a styled button."""
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        font=("Arial", 11, "bold"),
        width=width,
        height=2,
        relief="flat",
        cursor="hand2"
    )


def update_dashboard():
    """Update dashboard statistics."""
    total_lost = sum(1 for r in records if r["type"] == "Lost")
    total_found = sum(1 for r in records if r["type"] == "Found")
    returned = sum(1 for r in records if r["status"] == "Returned")

    lost_count_label.config(text=str(total_lost))
    found_count_label.config(text=str(total_found))
    returned_count_label.config(text=str(returned))


def clear_entries(entries):
    """Clear all form entries."""
    for entry in entries:
        entry.delete(0, tk.END)


# =========================================================
# REPORT LOST ITEM
# =========================================================

def report_lost_item():

    window = tk.Toplevel(root)
    window.title("Report Lost Item")
    window.geometry("550x620")
    window.configure(bg=BG)
    window.resizable(False, False)

    title = tk.Label(
        window,
        text="📦  REPORT LOST ITEM",
        font=("Arial", 21, "bold"),
        bg=BG,
        fg=NAVY
    )
    title.pack(pady=(25, 5))

    subtitle = tk.Label(
        window,
        text="Enter details of the lost item",
        font=("Arial", 11),
        bg=BG,
        fg=GRAY
    )
    subtitle.pack(pady=(0, 20))

    form = tk.Frame(window, bg=WHITE, padx=30, pady=25)
    form.pack(padx=30, fill="both", expand=True)

    # Item Name
    tk.Label(
        form,
        text="Item Name",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    item_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=45,
        relief="solid",
        bd=1
    )
    item_entry.pack(pady=(5, 15))

    # Category
    tk.Label(
        form,
        text="Category",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    category_combo = ttk.Combobox(
        form,
        values=[
            "Electronics",
            "Documents",
            "Accessories",
            "Books",
            "Stationery",
            "Clothing",
            "Other"
        ],
        state="readonly",
        width=42
    )
    category_combo.pack(pady=(5, 15))
    category_combo.set("Select Category")

    # Location
    tk.Label(
        form,
        text="Lost Location",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    location_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=45,
        relief="solid",
        bd=1
    )
    location_entry.pack(pady=(5, 15))

    # Description
    tk.Label(
        form,
        text="Description",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    description_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=45,
        relief="solid",
        bd=1
    )
    description_entry.pack(pady=(5, 15))

    def save_lost_item():

        item_name = item_entry.get().strip()
        category = category_combo.get()
        location = location_entry.get().strip()
        description = description_entry.get().strip()

        if not item_name or category == "Select Category" or not location:
            messagebox.showwarning(
                "Missing Information",
                "Please enter Item Name, Category and Location."
            )
            return

        new_item = {
            "id": len(records) + 1,
            "item_name": item_name,
            "category": category,
            "location": location,
            "description": description,
            "type": "Lost",
            "status": "Pending",
            "date": datetime.now().strftime("%d-%m-%Y")
        }

        records.append(new_item)
        save_data(records)
        update_dashboard()

        messagebox.showinfo(
            "Success",
            "Lost item has been saved successfully!"
        )

        window.destroy()

    create_button(
        form,
        "💾  SAVE LOST ITEM",
        save_lost_item,
        BLUE,
        22
    ).pack(pady=10)


# =========================================================
# REPORT FOUND ITEM
# =========================================================

def report_found_item():

    window = tk.Toplevel(root)
    window.title("Report Found Item")
    window.geometry("550x620")
    window.configure(bg=BG)
    window.resizable(False, False)

    title = tk.Label(
        window,
        text="🔎  REPORT FOUND ITEM",
        font=("Arial", 21, "bold"),
        bg=BG,
        fg=NAVY
    )
    title.pack(pady=(25, 5))

    subtitle = tk.Label(
        window,
        text="Enter details of the found item",
        font=("Arial", 11),
        bg=BG,
        fg=GRAY
    )
    subtitle.pack(pady=(0, 20))

    form = tk.Frame(window, bg=WHITE, padx=30, pady=25)
    form.pack(padx=30, fill="both", expand=True)

    # Item Name
    tk.Label(
        form,
        text="Item Name",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    item_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=45,
        relief="solid",
        bd=1
    )
    item_entry.pack(pady=(5, 15))

    # Category
    tk.Label(
        form,
        text="Category",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    category_combo = ttk.Combobox(
        form,
        values=[
            "Electronics",
            "Documents",
            "Accessories",
            "Books",
            "Stationery",
            "Clothing",
            "Other"
        ],
        state="readonly",
        width=42
    )
    category_combo.pack(pady=(5, 15))
    category_combo.set("Select Category")

    # Location
    tk.Label(
        form,
        text="Found Location",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    location_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=45,
        relief="solid",
        bd=1
    )
    location_entry.pack(pady=(5, 15))

    # Description
    tk.Label(
        form,
        text="Description",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    description_entry = tk.Entry(
        form,
        font=("Arial", 11),
        width=45,
        relief="solid",
        bd=1
    )
    description_entry.pack(pady=(5, 15))

    def save_found_item():

        item_name = item_entry.get().strip()
        category = category_combo.get()
        location = location_entry.get().strip()
        description = description_entry.get().strip()

        if not item_name or category == "Select Category" or not location:
            messagebox.showwarning(
                "Missing Information",
                "Please enter Item Name, Category and Location."
            )
            return

        new_item = {
            "id": len(records) + 1,
            "item_name": item_name,
            "category": category,
            "location": location,
            "description": description,
            "type": "Found",
            "status": "Pending",
            "date": datetime.now().strftime("%d-%m-%Y")
        }

        records.append(new_item)
        save_data(records)
        update_dashboard()

        messagebox.showinfo(
            "Success",
            "Found item has been saved successfully!"
        )

        window.destroy()

    create_button(
          form,
          "💾  SAVE FOUND ITEM",
          save_found_item,
          GREEN,
          22
    ).pack(pady=10)


# =========================================================
# SEARCH ITEM
# =========================================================

def search_item():

    window = tk.Toplevel(root)
    window.title("Search Item")
    window.geometry("850x600")
    window.configure(bg=BG)

    title = tk.Label(
        window,
        text="🔍  SEARCH ITEMS",
        font=("Arial", 21, "bold"),
        bg=BG,
        fg=NAVY
    )
    title.pack(pady=(25, 5))

    search_frame = tk.Frame(window, bg=BG)
    search_frame.pack(pady=15)

    search_entry = tk.Entry(
        search_frame,
        width=40,
        font=("Arial", 12)
    )
    search_entry.grid(row=0, column=0, padx=10)

    result_count = tk.Label(
        window,
        text="",
        font=("Arial", 10, "bold"),
        bg=BG,
        fg=GRAY
    )
    result_count.pack()

    columns = (
        "ID",
        "Item",
        "Category",
        "Location",
        "Type",
        "Status"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=15
    )

    for column in columns:
        tree.heading(column, text=column)

    tree.column("ID", width=50)
    tree.column("Item", width=170)
    tree.column("Category", width=120)
    tree.column("Location", width=150)
    tree.column("Type", width=80)
    tree.column("Status", width=100)

    tree.pack(padx=25, pady=15, fill="both", expand=True)

    def perform_search():

        for row in tree.get_children():
            tree.delete(row)

        keyword = search_entry.get().strip().lower()

        found = []

        for record in records:

            searchable_text = (
                record["item_name"] + " " +
                record["category"] + " " +
                record["location"] + " " +
                record["description"]
            ).lower()

            if keyword in searchable_text:
                found.append(record)

        for record in found:

            tree.insert(
                "",
                "end",
                values=(
                    record["id"],
                    record["item_name"],
                    record["category"],
                    record["location"],
                    record["type"],
                    record["status"]
                )
            )

        result_count.config(
            text=f"{len(found)} record(s) found"
        )

    create_button(
        search_frame,
        "🔍 SEARCH",
        perform_search,
        BLUE,
        12
    ).grid(row=0, column=1)


# =========================================================
# VIEW ALL RECORDS
# =========================================================

def view_all_records():

    window = tk.Toplevel(root)
    window.title("All Records")
    window.geometry("950x600")
    window.configure(bg=BG)

    title = tk.Label(
        window,
        text="📋  ALL LOST & FOUND RECORDS",
        font=("Arial", 21, "bold"),
        bg=BG,
        fg=NAVY
    )
    title.pack(pady=25)

    columns = (
        "ID",
        "Item",
        "Category",
        "Location",
        "Type",
        "Status",
        "Date"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=17
    )

    for column in columns:
        tree.heading(column, text=column)

    tree.column("ID", width=50)
    tree.column("Item", width=150)
    tree.column("Category", width=110)
    tree.column("Location", width=130)
    tree.column("Type", width=80)
    tree.column("Status", width=100)
    tree.column("Date", width=100)

    tree.pack(
        padx=20,
        pady=10,
        fill="both",
        expand=True
    )

    for record in records:

        tree.insert(
            "",
            "end",
            values=(
                record["id"],
                record["item_name"],
                record["category"],
                record["location"],
                record["type"],
                record["status"],
                record["date"]
            )
        )

    def mark_returned():

        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select Record",
                "Please select a record first."
            )
            return

        values = tree.item(selected[0], "values")
        record_id = int(values[0])

        for record in records:

            if record["id"] == record_id:
                record["status"] = "Returned"
                break

        save_data(records)
        update_dashboard()

        messagebox.showinfo(
            "Success",
            "Item marked as returned."
        )

        window.destroy()

    create_button(
        window,
        "✓  MARK SELECTED AS RETURNED",
        mark_returned,
        GREEN,
        25
    ).pack(pady=15)


# =========================================================
# SMART MATCHING
# =========================================================

def find_matches():

    matches = []

    lost_items = [
        r for r in records
        if r["type"] == "Lost" and r["status"] != "Returned"
    ]

    found_items = [
        r for r in records
        if r["type"] == "Found" and r["status"] != "Returned"
    ]

    for lost in lost_items:

        for found in found_items:

            score = 0

            lost_name = lost["item_name"].lower()
            found_name = found["item_name"].lower()

            lost_category = lost["category"].lower()
            found_category = found["category"].lower()

            lost_location = lost["location"].lower()
            found_location = found["location"].lower()

            # Item name match
            if lost_name == found_name:
                score += 50
            elif lost_name in found_name or found_name in lost_name:
                score += 30

            # Category match
            if lost_category == found_category:
                score += 25

            # Location match
            if lost_location == found_location:
                score += 25

            if score >= 60:
                matches.append(
                    (lost, found, score)
                )

    show_matches(matches)


def show_matches(matches):

    window = tk.Toplevel(root)
    window.title("Smart Matches")
    window.geometry("850x600")
    window.configure(bg=BG)

    title = tk.Label(
        window,
        text="🤖  SMART POSSIBLE MATCHES",
        font=("Arial", 21, "bold"),
        bg=BG,
        fg=NAVY
    )
    title.pack(pady=(25, 5))

    subtitle = tk.Label(
        window,
        text="Lost and found records with similar details",
        font=("Arial", 11),
        bg=BG,
        fg=GRAY
    )
    subtitle.pack(pady=(0, 20))

    if not matches:

        tk.Label(
            window,
            text="No possible matches found.",
            font=("Arial", 15, "bold"),
            bg=BG,
            fg=GRAY
        ).pack(pady=80)

        return

    canvas = tk.Canvas(
        window,
        bg=BG,
        highlightthickness=0
    )
    canvas.pack(
        fill="both",
        expand=True,
        padx=25
    )

    for lost, found, score in matches:

        card = tk.Frame(
            canvas,
            bg=WHITE,
            padx=20,
            pady=15,
            bd=1,
            relief="solid"
        )
        card.pack(fill="x", pady=10)

        tk.Label(
            card,
            text=f"🔔 MATCH SCORE: {score}%",
            font=("Arial", 13, "bold"),
            bg=WHITE,
            fg=GREEN
        ).pack(anchor="w")

        tk.Label(
            card,
            text=f"📦 Lost: {lost['item_name']} | {lost['location']}",
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(anchor="w", pady=5)

        tk.Label(
            card,
            text=f"🔎 Found: {found['item_name']} | {found['location']}",
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(anchor="w", pady=5)

        def return_item(lost_id=lost["id"], found_id=found["id"]):

            for record in records:

                if record["id"] in (lost_id, found_id):
                    record["status"] = "Returned"

            save_data(records)
            update_dashboard()

            messagebox.showinfo(
                "Success",
                "Matching items marked as returned."
            )

            window.destroy()

        create_button(
            card,
            "✓  MARK AS RETURNED",
            return_item,
            GREEN,
            20
        ).pack(anchor="e", pady=5)


# =========================================================
# STATISTICS
# =========================================================

def show_statistics():

    window = tk.Toplevel(root)
    window.title("Statistics")
    window.geometry("600x500")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="📊  PROJECT STATISTICS",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=NAVY
    ).pack(pady=30)

    total_lost = sum(
        1 for r in records if r["type"] == "Lost"
    )

    total_found = sum(
        1 for r in records if r["type"] == "Found"
    )

    returned = sum(
        1 for r in records if r["status"] == "Returned"
    )

    pending = sum(
        1 for r in records if r["status"] == "Pending"
    )

    stats_frame = tk.Frame(
        window,
        bg=BG
    )
    stats_frame.pack(pady=10)

    statistics = [
        ("📦", "Total Lost", total_lost, BLUE),
        ("🔎", "Total Found", total_found, GREEN),
        ("✓", "Returned", returned, ORANGE),
        ("⏳", "Pending", pending, RED)
    ]

    for icon, name, value, color in statistics:

        card = tk.Frame(
            stats_frame,
            bg=WHITE,
            width=400,
            height=65
        )
        card.pack(pady=7)
        card.pack_propagate(False)

        tk.Label(
            card,
            text=f"{icon}  {name}",
            font=("Arial", 12, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(side="left", padx=20)

        tk.Label(
            card,
            text=str(value),
            font=("Arial", 16, "bold"),
            bg=WHITE,
            fg=color
        ).pack(side="right", padx=20)
header = tk.Frame(
root,
bg=NAVY,
height=120
)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="🎓  COLLEGE LOST & FOUND MANAGER",
    font=("Arial", 25, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(pady=(22, 3))

tk.Label(
    header,
    text="Smart Item Recovery System",
    font=("Arial", 12),
    bg=NAVY,
    fg="#D9E7FF"
).pack()
stats_frame = tk.Frame(
    root,
    bg=BG
)
stats_frame.pack(pady=25)

# Lost card
lost_card = tk.Frame(
    stats_frame,
    bg=WHITE,
    width=200,
    height=90
)
lost_card.grid(row=0, column=0, padx=10)
lost_card.pack_propagate(False)

tk.Label(
    lost_card,
    text="📦  LOST ITEMS",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=GRAY
).pack(pady=(15, 2))

lost_count_label = tk.Label(
    lost_card,
    text="0",
    font=("Arial", 22, "bold"),
    bg=WHITE,
    fg=BLUE
)
lost_count_label.pack()
found_card = tk.Frame(
    stats_frame,
    bg=WHITE,
    width=200,
    height=90
)
found_card.grid(row=0, column=1, padx=10)
found_card.pack_propagate(False)

tk.Label(
    found_card,
    text="🔎  FOUND ITEMS",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=GRAY
).pack(pady=(15, 2))
found_count_label = tk.Label(
    found_card,
    text="0",
    font=("Arial", 22, "bold"),
    bg=WHITE,
    fg=GREEN
)
found_count_label.pack()


# Returned card
returned_card = tk.Frame(
    stats_frame,
    bg=WHITE,
    width=200,
    height=90
)
returned_card.pack_propagate(False)

tk.Label(
    returned_card,
    text="✓  RETURNED",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=GRAY
).pack(pady=(15, 2))

returned_count_label = tk.Label(
    returned_card,
    text="0",
    font=("Arial", 22, "bold"),
    bg=WHITE,
    fg=ORANGE
)
returned_count_label.pack()
button_frame = tk.Frame(
    root,
    bg=BG
)
button_frame.pack(pady=10)

create_button(
    button_frame,
    "📦  REPORT LOST ITEM",
    report_lost_item,
    BLUE,
    25
).grid(row=0, column=0, padx=10, pady=8)

create_button(
    button_frame,
    "🔎  REPORT FOUND ITEM",
    report_found_item,
    GREEN,
    25
).grid(row=0, column=1, padx=10, pady=8)
create_button(
    button_frame,
    "🔍  SEARCH ITEM",
    search_item,
    ORANGE,
    25
).grid(row=1, column=0, padx=10, pady=8)

create_button(
    button_frame,
    "📋  VIEW ALL RECORDS",
    view_all_records,
    NAVY,
    25
).grid(row=1, column=1, padx=10, pady=8)

create_button(
    button_frame,
    "🤖  FIND POSSIBLE MATCH",
    find_matches,
    "#7B61A8",
    25
).grid(row=2, column=0, padx=10, pady=8)
create_button(
    button_frame,
    "📊  VIEW STATISTICS",
    show_statistics,
    "#5B7C99",
    25
).grid(row=2, column=1, padx=10, pady=8)


# =========================================================
# START APPLICATION
# =========================================================

update_dashboard()

root.mainloop()