Sure, here's a step-by-step guide on how we triggered the USB plug event and executed the script on Debian 11 using udev and Systemd:

1. **Write the Python Script:**
   - We started by writing the Python script (`yt.py`) that downloads videos and converts them to MP3 files, as per your requirements.

2. **Create a Virtual Environment (Optional):**
   - We created a virtual environment (venv) to isolate the Python dependencies for the script. This step ensures that the required packages (`pytube`, `moviepy`, etc.) are installed within the venv and do not interfere with the system-wide Python packages.

3. **Test the Python Script:**
   - Before integrating the script with udev, we tested the Python script manually to ensure that it works as expected. This step helps in identifying any issues or errors in the script.

4. **Identify USB Device Information:**
   - We plugged in the USB flash drive and ran `udevadm info -a /dev/sdb1` to gather information about the USB device. We needed this information to create the udev rule.

5. **Create the udev Rule:**
   - We created a udev rule file (e.g., `/etc/udev/rules.d/99-ibiza.rules`) with the following content:

     ```
     ACTION=="add", SUBSYSTEM=="usb", KERNEL=="sdb1", TAG+="systemd", ENV{SYSTEMD_WANTS}+="ibiza_script.service"
     ```

   - This rule tells udev to trigger the `ibiza_script.service` whenever a USB device with the kernel name `sdb1` (your USB flash drive) is added.

6. **Create the Systemd Service:**
   - We created a Systemd service file (e.g., `/etc/systemd/system/ibiza_script.service`) with the following content:

     ```
     [Unit]
     Description=Your Script Service
     After=media-skyflower-ibiza.mount

     [Service]
     Type=oneshot
     ExecStart=/home/skyflower/scripts/ytstart.sh

     [Install]
     WantedBy=media-skyflower-ibiza.mount
     ```

   - This Systemd service is responsible for executing the `ytstart.sh` script when triggered by the udev rule. It specifies that the service should be executed after the mount point (`media-skyflower-ibiza.mount`) is activated.

7. **Create the Shell Script (ytstart.sh):**
   - We created a shell script (`ytstart.sh`) that sets up the virtual environment, activates it, runs the Python script (`yt.py`), and deactivates the virtual environment.

8. **Make Shell Script Executable:**
   - We made the `ytstart.sh` shell script executable using the `chmod` command:

     ```
     chmod +x /home/skyflower/scripts/ytstart.sh
     ```

9. **Reload udev Rules:**
   - We reloaded the udev rules to apply the changes:

     ```
     udevadm control --reload-rules

     udevadm control --reload-rules
     sudo systemctl restart systemd-udevd
     ```

10. **Test the Setup:**
   - Finally, we tested the setup by plugging in the USB flash drive and checking the log files (`/tmp/yt_debug.log` and `/tmp/yt_python_version.log`) to ensure that the Python script was executed successfully.

With these steps, the Python script was triggered automatically when the USB flash drive was plugged in, and it successfully downloaded and converted videos to MP3 files on the USB drive.
