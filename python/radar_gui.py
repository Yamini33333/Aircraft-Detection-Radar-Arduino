import tkinter as tk
from tkinter import ttk
import serial
from serial.tools import list_ports


class RadarGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Ultrasonic Radar System")
        self.master.geometry("800x600")
        self.master.configure(bg="black")

        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        # Radar display
        self.canvas = tk.Canvas(
            self.main_frame,
            width=600,
            height=400,
            bg="black"
        )
        self.canvas.pack(pady=20)

        self.create_radar_display()

        # Status
        self.status_label = tk.Label(
            self.main_frame,
            text="Status: Connecting...",
            fg="white",
            bg="black"
        )
        self.status_label.pack(pady=10)

        self.arduino = None

        self.connect_to_arduino()
        self.update_radar()

    def create_radar_display(self):

        # Radar circles
        for i in range(4):
            radius = (i + 1) * 80

            self.canvas.create_oval(
                300 - radius,
                200 - radius,
                300 + radius,
                200 + radius,
                outline="green"
            )

        # Range labels
        ranges = [500, 1000, 1500, 2000]

        for i, range_val in enumerate(ranges):

            y_pos = 200 - (i + 1) * 80 - 10

            self.canvas.create_text(
                300,
                y_pos,
                text=f"{range_val} cm",
                fill="green",
                anchor="s"
            )

        # Detection zones
        self.left_zone = self.canvas.create_arc(
            100, 0, 500, 400,
            start=150,
            extent=60,
            fill="darkgreen"
        )

        self.right_zone = self.canvas.create_arc(
            100, 0, 500, 400,
            start=330,
            extent=60,
            fill="darkgreen"
        )

        # Sensor indicators
        self.left_indicator = self.canvas.create_text(
            150,
            350,
            text="Sensor 1",
            fill="white"
        )

        self.right_indicator = self.canvas.create_text(
            450,
            350,
            text="Sensor 2",
            fill="white"
        )

    def connect_to_arduino(self):

        try:

            ports = list_ports.comports()

            # Automatically find Arduino
            for port in ports:

                if (
                    "Arduino" in port.description
                    or "CH340" in port.description
                ):

                    self.arduino = serial.Serial(
                        port.device,
                        9600,
                        timeout=1
                    )

                    self.status_label.config(
                        text=f"Connected to Arduino on {port.device}"
                    )

                    return

            # Try common ports
            common_ports = [
                "COM3",
                "COM4",
                "COM5",
                "COM6",
                "/dev/ttyUSB0",
                "/dev/ttyACM0"
            ]

            for port in common_ports:

                try:

                    self.arduino = serial.Serial(
                        port,
                        9600,
                        timeout=1
                    )

                    self.status_label.config(
                        text=f"Connected to Arduino on {port}"
                    )

                    return

                except:
                    continue

            self.status_label.config(
                text="Could not connect to Arduino"
            )

        except Exception as e:

            self.status_label.config(
                text=f"Connection error: {e}"
            )

    def update_radar(self):

        try:

            if (
                self.arduino is not None
                and self.arduino.is_open
                and self.arduino.in_waiting
            ):

                data = self.arduino.readline().decode().strip()

                distances = data.split(",")

                # Arduino sends:
                # distance1,distance2

                if len(distances) == 2:

                    dist1 = float(distances[0])
                    dist2 = float(distances[1])

                    self.update_zones(dist1, dist2)

                    self.canvas.itemconfig(
                        self.left_indicator,
                        text=f"Sensor 1: {dist1:.1f} cm"
                    )

                    self.canvas.itemconfig(
                        self.right_indicator,
                        text=f"Sensor 2: {dist2:.1f} cm"
                    )

                    # Object detection
                    if (
                        dist1 > 0
                        and dist2 > 0
                        and abs(dist1 - dist2) > 5
                    ):

                        self.canvas.itemconfig(
                            self.left_zone,
                            fill="red"
                        )

                        self.canvas.itemconfig(
                            self.right_zone,
                            fill="red"
                        )

                        self.status_label.config(
                            text="Object Detected!"
                        )

                    else:

                        self.canvas.itemconfig(
                            self.left_zone,
                            fill="darkgreen"
                        )

                        self.canvas.itemconfig(
                            self.right_zone,
                            fill="darkgreen"
                        )

                        self.status_label.config(
                            text="Monitoring..."
                        )

        except Exception as e:

            self.status_label.config(
                text=f"Error: {e}"
            )

        # Update every 100 ms
        self.master.after(
            100,
            self.update_radar
        )

    def update_zones(self, dist1, dist2):

        # Maximum display range
        max_range = 2000

        norm_dist1 = min(
            max(dist1 / max_range, 0),
            1.0
        )

        norm_dist2 = min(
            max(dist2 / max_range, 0),
            1.0
        )

        left_extent = 60 * norm_dist1
        right_extent = 60 * norm_dist2

        self.canvas.itemconfig(
            self.left_zone,
            extent=left_extent
        )

        self.canvas.itemconfig(
            self.right_zone,
            extent=right_extent
        )


if __name__ == "__main__":

    root = tk.Tk()

    app = RadarGUI(root)

    root.mainloop()
