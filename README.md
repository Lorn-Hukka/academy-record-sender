# ACADEMY RECORD SENDER

## Instalation
1. Download and save script for example on Desktop.
2. Install Python (Minimum 3.9) with pip.
3. Open console withnin folder containing script.
4. Run:
    ```
    pip install -r requirements.txt
    ```
5. Copy `.settings.default` to `.settings`.
6. Enter the appropriate data into `.settings`
   ```
    _7ZIP = "D:\\7-Zip\\7z.exe" <- Path to 7zip exe
    RECORDS_PATH = "H:\\Nagrania" <- Path to your records folder
    EXTENSION = ".mkv" <- Extension your recorded files have.
    WEBHOOK = "INSERT WEBHOOK HERE" <- Webhook for discord channel
    NAME = "INSERT NAME HERE" <- Your name
   ```

# USAGE
1. Record your lecture.
2. Run `main.py` by double clicking or using command `python main.py` inside cmd.
3. Open `passwords` inside text editor
4. Copy password for share link. (You can found it after `LP: `)
5. Copy the share link and paste it after: `L: `
6. Run `main.py` again.

