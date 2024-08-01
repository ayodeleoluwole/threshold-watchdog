# Python Backup Manager

A Python based backup automation tool that monitors disk utilization and triggers 
file/directory backups when a set threshold is exceeded. It is runnable via command line 
or a Tkinter GUI.

---

## What It Does

- **Disk Monitoring** : checks disk usage against a defined threshold and 
  triggers a backup automatically when exceeded
- **File & Directory Backup** : copies files and directories to a timestamped 
  destination path
- **Compression** : archives backed-up data into a `.tar.gz` compressed file
- **Logging** : writes all activity to a structured log file with timestamps
- **Dual Interface** : runs as a desktop GUI (Tkinter) or via command line arguments

---

## Usage

### Command Line
```bash
python3 backup_manager.py <disc> <threshold> <runner> <log_file_path> <log_file_name>
```

| Argument | Description |
|---|---|
| `disc` | Disk/mount path to monitor (e.g. `/home`) |
| `threshold` | Usage percentage that triggers the backup (e.g. `80`) |
| `runner` | Identifier for the backup run |
| `log_file_path` | Directory to store the log file |
| `log_file_name` | Name of the log file |

### GUI Mode
```bash
python3 backup_manager.py gui
```
Launches a Tkinter form where you can fill in all parameters and submit.

---

## How It Works

1. Checks the current disk usage of the specified mount point
2. Compares usage against the defined threshold
3. If exceeded, triggers the on-premise backup function
4. Copies each source to a timestamped destination directory
5. Compresses all backed-up paths into a `.tar.gz` archive
6. Logs all activity to a structured log file

---

## Built With

- Python 3
- `shutil` : file and directory operations
- `tarfile` : backup compression
- `logging` : structured log output
- `tkinter` : desktop GUI interface
- `subprocess` / `os` : disk monitoring and system commands

---

## Logs

All activity is logged to a file under `<log_file_path>/<runner>/`, 
covering disk checks, backup start/end times, compression status, and errors.