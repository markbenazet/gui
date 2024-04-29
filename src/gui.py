import tkinter as tk
from tkinter import simpledialog
import paramiko
import threading

class SSHClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.client.connect(self.host, username=self.username, password=self.password)
            return True
        except paramiko.AuthenticationException:
            print("Authentication failed, please check your credentials.")
            return False
        except paramiko.SSHException as e:
            print(f"Unable to establish SSH connection: {e}")
            return False

    def execute_command(self, command):
        print(f"Executing command: {command}")
        stdin, stdout, stderr = self.client.exec_command(f"/bin/bash -c '{command}'")
        stdout_str = stdout.read().decode()
        stderr_str = stderr.read().decode()
        print(f"Command output: {stdout_str}")
        print(f"Command error: {stderr_str}")
        return stdout_str, stderr_str

    def close(self):
        self.client.close()

def start_recording():
    global ssh_client
    threading.Thread(target=ssh_client.execute_command, args=('libcamera-vid -t 0 --framerate 30 --autofocus-mode continuous --width 2048 --height 1080 -o "/home/noctua_raspi/Videos/$(date +%Y%m%d_%H%M.h264)"',)).start()
    
def stop_recording():
    global ssh_client
    ssh_client.execute_command("killall -SIGINT libcamera-vid")

def run_file():
    global ssh_client
    result = ssh_client.execute_command("python3 /path/to/your/file.py")
    print(result)

def connect_ssh():
    global ssh_client
    selected_option = ssh_options.get()
    host = ""
    username = ""
    password = ""
    if selected_option == "RPi 4":
        host = "172.29.245.218"
        username = "noctua"
        password = "noctuaraspi"
    elif selected_option == "RPi 5":
        host = "172.29.24.48"
        username = "noctua_raspi"
        password = "raspi"
    
    # Disable all buttons during connection attempt
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.DISABLED)
    run_button.config(state=tk.DISABLED)
    close_button.config(state=tk.DISABLED)

    ssh_client = SSHClient(host, username, password)
    if ssh_client.connect():
        print("SSH connection established.")
        # Enable all buttons after successful connection
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.NORMAL)
        run_button.config(state=tk.NORMAL)
        close_button.config(state=tk.NORMAL)
    else:
        print("Failed to establish SSH connection.")

def close_ssh():
    global ssh_client
    if ssh_client:
        ssh_client.close()
        print("SSH connection closed.")

if __name__ == "__main__":
    ssh_client = None

    root = tk.Tk()
    root.title("RPi Control Panel")

    ssh_options = tk.StringVar(root)
    ssh_options.set("RPi 4")
    ssh_options_menu = tk.OptionMenu(root, ssh_options, "RPi 4", "RPi 5")
    ssh_options_menu.grid(row=2, column=0)

    connect_button = tk.Button(root, text="Connect SSH", command=connect_ssh)
    connect_button.grid(row=3, column=0)

    start_button = tk.Button(root, text="Start Recording", command=start_recording, state=tk.DISABLED)
    start_button.grid(row=4, column=0)

    stop_button = tk.Button(root, text="Stop Recording", command=stop_recording, state=tk.DISABLED)
    stop_button.grid(row=4, column=1)

    run_button = tk.Button(root, text="Run File", command=run_file, state=tk.DISABLED)
    run_button.grid(row=5, column=0)

    close_button = tk.Button(root, text="Close SSH", command=close_ssh, state=tk.DISABLED)
    close_button.grid(row=6, column=0)

    root.mainloop()
