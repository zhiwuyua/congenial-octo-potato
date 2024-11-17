import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class ReuseItemsApp:
    def __init__(self, root):
        self.data_path = 'items_data.json'
        self.items = []
        self.load_data()

        self.root = root
        self.root.title("Reuse Items Application")

        self.label_title = tk.Label(root, text="Reuse Items Application", font=("Arial", 16))
        self.label_title.pack(pady=10)

        self.frame_controls = tk.Frame(root)
        self.frame_controls.pack(pady=10)

        self.btn_add = tk.Button(self.frame_controls, text="Add Item", command=self.add_item_gui)
        self.btn_add.pack(side=tk.LEFT, padx=5)

        self.btn_delete = tk.Button(self.frame_controls, text="Delete Item", command=self.delete_item_gui)
        self.btn_delete.pack(side=tk.LEFT, padx=5)

        self.btn_find = tk.Button(self.frame_controls, text="Find Item", command=self.find_item_gui)
        self.btn_find.pack(side=tk.LEFT, padx=5)

        self.btn_display = tk.Button(self.frame_controls, text="Display All Items", command=self.display_all_items_gui)
        self.btn_display.pack(side=tk.LEFT, padx=5)

        self.text_output = tk.Text(root, width=80, height=20)
        self.text_output.pack(pady=10)

        self.btn_exit = tk.Button(root, text="Exit", command=root.quit)
        self.btn_exit.pack(pady=5)

    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as file:
                self.items = json.load(file)
            for item in self.items:
                if 'contact_type' not in item:
                    item['contact_type'] = "unknown" 
        else:
            self.items = []

    def save_data(self):
        with open(self.data_path, 'w') as file:
            json.dump(self.items, file, indent=4)

    def add_item_gui(self):
        name = simpledialog.askstring("Add Item", "Enter item name:")
        if not name:
            messagebox.showerror("Input Error", "Item name cannot be empty!")
            return

        description = simpledialog.askstring("Add Item", "Enter item description:")
        if not description:
            messagebox.showerror("Input Error", "Item description cannot be empty!")
            return

        contact_type = self.select_contact_type_gui()
        if not contact_type:
            return

        information = simpledialog.askstring("Add Item", "Enter contact information:")
        if not information:
            messagebox.showerror("Input Error", "Contact information cannot be empty!")
            return

        if contact_type == 'Phone' and (not information.isdigit() or len(information) != 11):
            messagebox.showerror("Input Error", "Phone number must be 11 digits!")
            return

        item_id = len(self.items) + 1
        new_item = {
            'ID': item_id,
            'name': name,
            'description': description,
            'contact_type': contact_type,
            'information': information
        }
        self.items.append(new_item)
        self.save_data()
        messagebox.showinfo("Success", f"Item '{name}' added successfully with ID {item_id}.")
        self.display_all_items_gui()

    def select_contact_type_gui(self):
        contact_type_window = tk.Toplevel(self.root)
        contact_type_window.title("Select Contact Type")

        label = tk.Label(contact_type_window, text="Select contact type (Phone or WeChat):")
        label.pack(pady=10)

        contact_type = ttk.Combobox(contact_type_window, values=["Phone", "WeChat"], state="readonly")
        contact_type.pack(pady=10)

        def on_select():
            nonlocal selected_contact_type
            selected_contact_type = contact_type.get()
            if selected_contact_type:
                contact_type_window.destroy()

        contact_type_button = tk.Button(contact_type_window, text="OK", command=on_select)
        contact_type_button.pack(pady=10)

        selected_contact_type = None
        contact_type_window.grab_set()
        contact_type_window.wait_window()

        return selected_contact_type

    def delete_item_gui(self):
        item_id = simpledialog.askinteger("Delete Item", "Enter item ID to delete:")
        if not item_id:
            return

        for item in self.items:
            if item['ID'] == item_id:
                self.items.remove(item)
                self.save_data()
                messagebox.showinfo("Success", f"Item with ID {item_id} deleted successfully.")
                self.display_all_items_gui()
                return

        messagebox.showerror("Error", f"Item with ID {item_id} not found.")

    def find_item_gui(self):
        name = simpledialog.askstring("Find Item", "Enter item name to find:")
        if not name:
            return

        # 完全匹配
        exact_matches = [item for item in self.items if item['name'].lower() == name.lower()]

        # 部分匹配（排除完全匹配的物品）
        partial_matches = [item for item in self.items if all(char.lower() in item['name'].lower() for char in name.lower()) and item not in exact_matches]

        self.text_output.delete(1.0, tk.END)

        if exact_matches:
            self.text_output.insert(tk.END, "Exact items:\n")
            self.text_output.insert(tk.END, "-" * 30 + "\n")
            for item in exact_matches:
                self.display_item(item)

        if partial_matches:
            self.text_output.insert(tk.END, "Possible items:\n")
            self.text_output.insert(tk.END, "-" * 30 + "\n")
            for item in partial_matches:
                self.display_item(item)

        if not exact_matches and not partial_matches:
            self.text_output.insert(tk.END, f"No items found with name '{name}'.\n")


    def display_all_items_gui(self):
        self.text_output.delete(1.0, tk.END)
        if not self.items:
            self.text_output.insert(tk.END, "No items found.\n")
        else:
            for item in self.items:
                self.display_item(item)

    def display_item(self, item):
        self.text_output.insert(tk.END, f"ID: {item['ID']}\n")
        self.text_output.insert(tk.END, f"Name: {item['name']}\n")
        self.text_output.insert(tk.END, f"Description: {item['description']}\n")
        self.text_output.insert(tk.END, f"Contact Type: {item['contact_type']}\n")
        self.text_output.insert(tk.END, f"Contact Information: {item['information']}\n")
        self.text_output.insert(tk.END, "-" * 30 + "\n")

if __name__ == '__main__':
    root = tk.Tk()
    app = ReuseItemsApp(root)
    root.mainloop()
