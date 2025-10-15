from django.http import JsonResponse
import subprocess
import os
import getpass
import time

def open_rustdesk(request):
    try:
        # Get current user
        user = getpass.getuser()

        # Ensure we point to the correct X display
        display = os.environ.get("DISPLAY", ":0")
        xauth = os.path.expanduser(f"/home/{user}/.Xauthority")

        env = os.environ.copy()
        env["DISPLAY"] = display
        env["XAUTHORITY"] = xauth

        # Launch RustDesk in background
        subprocess.Popen(
            ["rustdesk"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Give it a moment to start
        time.sleep(2)

        # Check if RustDesk is running
        result = subprocess.run(["pgrep", "-x", "rustdesk"], capture_output=True, text=True)

        if result.returncode == 0:
            return JsonResponse({"status": "success", "message": "RustDesk launched successfully!"})
        else:
            return JsonResponse({"status": "error", "message": "RustDesk did not start. Check installation or DISPLAY settings."})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
