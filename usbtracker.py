import os
import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import time
from threading import Thread
from datetime import datetime

# Ensure reports directory exists
if not os.path.exists('reports'):
    os.makedirs('reports')

class USBTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("USB Tracker")
        self.root.geometry("800x600")
        
        self.connected_devices = set()
        self.device_history = []
        self.running = True
        
        self.create_widgets()
        
        self.monitor_thread = Thread(target=self.monitor_usb_devices, daemon=True)
        self.monitor_thread.start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_device_list()
    
    def create_widgets(self):
        current_frame = ttk.LabelFrame(self.root, text="Connected USB Devices", padding=10)
        current_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.current_tree = ttk.Treeview(current_frame, columns=("Device", "Mount Point", "Size"), show="headings")
        self.current_tree.heading("Device", text="Device")
        self.current_tree.heading("Mount Point", text="Mount Point")
        self.current_tree.heading("Size", text="Size")
        self.current_tree.pack(fill=tk.BOTH, expand=True)
        
        history_frame = ttk.LabelFrame(self.root, text="Connection History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.history_tree = ttk.Treeview(history_frame, columns=("Time", "Event", "Device", "Mount Point"), show="headings")
        self.history_tree.heading("Time", text="Time")
        self.history_tree.heading("Event", text="Event")
        self.history_tree.heading("Device", text="Device")
        self.history_tree.heading("Mount Point", text="Mount Point")
        self.history_tree.pack(fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.refresh_btn = ttk.Button(button_frame, text="Refresh", command=self.update_device_list)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_history_btn = ttk.Button(button_frame, text="Clear History", command=self.clear_history)
        self.clear_history_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_btn = ttk.Button(button_frame, text="Export History", command=self.export_history)
        self.export_btn.pack(side=tk.RIGHT, padx=5)
    
    def monitor_usb_devices(self):
        while self.running:
            current_devices = self.get_usb_devices()
            
            new_devices = current_devices - self.connected_devices
            for device in new_devices:
                self.device_history.append((datetime.now(), "Connected", device[0], device[1]))
                self.update_history_tree()
            
            removed_devices = self.connected_devices - current_devices
            for device in removed_devices:
                self.device_history.append((datetime.now(), "Disconnected", device[0], device[1]))
                self.update_history_tree()
            
            self.connected_devices = current_devices
            time.sleep(1)
    
    def get_usb_devices(self):
        devices = set()
        for partition in psutil.disk_partitions():
            if 'removable' in partition.opts or 'fixed' in partition.opts:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    devices.add((partition.device, partition.mountpoint, self.format_size(usage.total)))
                except:
                    continue
        return devices
    
    def update_device_list(self):
        for item in self.current_tree.get_children():
            self.current_tree.delete(item)
        
        self.connected_devices = self.get_usb_devices()
        for device in self.connected_devices:
            self.current_tree.insert("", tk.END, values=device)
    
    def update_history_tree(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        for event in self.device_history[-100:]:
            time_str = event[0].strftime("%Y-%m-%d %H:%M:%S")
            self.history_tree.insert("", tk.END, values=(time_str, event[1], event[2], event[3]))
    
    def clear_history(self):
        self.device_history = []
        self.update_history_tree()
        messagebox.showinfo("Information", "History cleared successfully")
    
    def export_history(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join('reports', f'usb_history_{timestamp}.txt')
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write("Time\tEvent\tDevice\tMount Point\n")
                for event in self.device_history:
                    time_str = event[0].strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"{time_str}\t{event[1]}\t{event[2]}\t{event[3]}\n")
            
            messagebox.showinfo(
                "Export Successful", 
                f"USB history exported to:\n{os.path.abspath(filename)}"
            )
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export history:\n{str(e)}")
    
    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
    
    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = USBTrackerApp(root)
    root.mainloop()