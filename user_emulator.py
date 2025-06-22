import time
import uiautomator2 as u2

class UserEmulator:
    def __init__(self, device_id="emulator-5554"):
        """Initialize the User Emulator with a specific emulator/device ID."""
        self.device = u2.connect(device_id)
        print(f"Connected to {device_id}")
    
    def execute_action(self, action):
        """Execute a single action from the action file."""
        parts = action.strip().split("(")
        command = parts[0]
        
        if len(parts) > 1:
            params = parts[1].rstrip(")").split(",")
        else:
            params = []

        if command == "AllApps":
            self.device.press("home")
            self.device.swipe(500, 1500, 500, 500, 0.3)  # Swipe up to open apps
            time.sleep(2)
        elif command == "Back":
            self.device.press("back")
            time.sleep(1)
        elif command == "Enter":
            self.device.press("enter")
            time.sleep(2)
            self.device.press("enter")
        elif command == "Dump":
            print(self.device.dump_hierarchy())
            time.sleep(2)
        elif command == "Home":
            self.device.press("home")
            time.sleep(2)
        elif command == "SetTxt":
            if len(params) == 1:  # If only text is provided
                text = params[0].strip()
                self.device(focused=True).set_text(text)  # Enter text in the currently focused field
            elif len(params) == 2:  # If widgetId and text are provided
                widget_id, text = params
                self.device(resourceId=widget_id.strip()).set_text(text.strip())
                time.sleep(1)
            else:
                print(f"Invalid SetTxt format: {action}")
        elif command == "SetTxtXY":
            if len(params) == 3:
                x, y, text = params
                self.device.click(int(x), int(y))
                time.sleep(0.5)
                self.device.set_text(text.strip())
            else:
                print(f"Invalid SetTxtXY format: {action}")
            time.sleep(2)
        elif command == "TapOn":
            widget_id = params[0].strip()
            if widget_id.startswith("com."):  # If resource ID is used
                self.device(resourceId=widget_id).click()
            else:  # If it's a text-based identifier (e.g., TapOn(notes))
                self.device(text=widget_id).click()
            time.sleep(2)
        elif command == "TapXY":
            if len(params) == 2:
                x, y = map(int, params)
                self.device.click(x, y)
            else:
                print(f"Invalid TapXY format: {action}")
        else:
            print(f"Unknown command: {command}")

    def execute_script(self, action_file_path):
        """Execute a sequence of actions from the action file."""
        with open(action_file_path, "r") as file:
            for line in file:
                if line.strip():
                    self.execute_action(line.strip())
                    time.sleep(1)  # Delay to simulate human interaction

if __name__ == "__main__":
    emulator = UserEmulator()
    emulator.execute_script("action2.txt")  # Provide the path to the actions file
