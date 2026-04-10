# Server Health Monitor

A lightweight, cross-platform server health monitoring tool written in Python. Tracks CPU, memory, and disk usage alongside service availability, logs results to a file, and sends email alerts when configurable thresholds are exceeded.

---

## Overview

Server Health Monitor gives you a quick snapshot of your system's vital signs from the terminal. It checks resource usage against thresholds you define, flags anything out of range, and can fire off an email alert so you know about problems before they become outages.

---

## Features

- **CPU, memory, and disk monitoring** via `psutil` — works on Linux, macOS, and Windows
- **Service status checks** — uses `sc query` on Windows and `systemctl` on Linux
- **Configurable thresholds** — set your own warning levels in `config.json`
- **Email alerts** — sends a summary of all warnings over SMTP with TLS
- **Persistent logging** — all results are written to `health.log` with timestamps
- **Clean terminal output** — color-coded status icons and an at-a-glance summary table

---

## Requirements

- Python 3.7+
- [`psutil`](https://pypi.org/project/psutil/)

Install the dependency:

```bash
pip install psutil
```

---

## Installation

```bash
git clone https://github.com/your-username/server-health-monitor.git
cd server-health-monitor
pip install psutil
```

---

## Usage

```bash
python monitor.py
```

Results are printed to the terminal and appended to `health.log` in the same directory.

---

## Configuration

All settings live in `config.json`:

```json
{
  "thresholds": {
    "cpu_percent": 80,
    "memory_percent": 85,
    "disk_percent": 90
  },
  "services": ["nginx", "mysql", "redis"],
  "email": {
    "enabled": false,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender": "your@email.com",
    "receiver": "your@email.com",
    "password": "your_app_password"
  }
}
```

### Thresholds

| Key | Default | Description |
|---|---|---|
| `cpu_percent` | `80` | Warning threshold for CPU usage (%) |
| `memory_percent` | `85` | Warning threshold for RAM usage (%) |
| `disk_percent` | `90` | Warning threshold for disk usage (%) |

### Services

List service names to check under `"services"`. The monitor checks whether each service is running:

- **Windows** — uses `sc query <service>`
- **Linux** — uses `systemctl is-active <service>`

Use the exact service name as registered with the OS (e.g. `nginx`, `mysql`, `sshd`).

### Email Alerts

Set `"enabled": true` and fill in your SMTP credentials to receive email alerts whenever a warning is triggered. For Gmail, generate an [App Password](https://support.google.com/accounts/answer/185833) instead of using your account password.

---

## Sample Output

```
==================================================
  SERVER HEALTH REPORT - 2026-04-10 14:32:07
==================================================
✅  CPU                       23.4%           OK
✅  Memory                    61.2%           OK
⚠️  Disk                      91.8%           WARNING
✅  Service: nginx             running         OK
⚠️  Service: mysql             not running     WARNING
✅  Service: redis             running         OK
==================================================
  Warnings: 2 | Checked: 6 metrics
==================================================
```

When warnings are present and email alerts are enabled, a notification is sent immediately after the report is printed.

---

## Log File

Every run appends timestamped entries to `health.log`:

```
2026-04-10 14:32:07,412 - INFO - CPU - 23.4% - OK
2026-04-10 14:32:07,413 - INFO - Memory - 61.2% - OK
2026-04-10 14:32:07,414 - INFO - Disk - 91.8% - WARNING
2026-04-10 14:32:07,415 - INFO - Service: nginx - running - OK
2026-04-10 14:32:07,416 - INFO - Service: mysql - not running - WARNING
2026-04-10 14:32:07,417 - INFO - Service: redis - running - OK
```

---

## Automating Runs

**Linux / macOS (cron)** — check every 5 minutes:

```bash
*/5 * * * * /usr/bin/python3 /path/to/monitor.py
```

**Windows (Task Scheduler)** — create a Basic Task that runs:

```
python C:\path\to\monitor.py
```

---

## License

MIT
