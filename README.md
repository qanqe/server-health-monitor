# server-health-monitor

Lightweight cross-platform health monitor written in Python. Checks CPU, memory, disk usage, and service status against thresholds you define. Logs everything and fires email alerts when something goes sideways.

## What it does

Gives you a terminal snapshot of your system's vital signs on demand (or on a schedule). Any metric that crosses a threshold gets flagged, logged, and optionally emailed to you. That's it — no agent running in the background, no dashboard to babysit.

Works on Linux (systemctl) and Windows (sc query) without changing anything.

## Features

- CPU, memory, and disk monitoring via `psutil`
- Service checks using `systemctl` on Linux and `sc query` on Windows
- Thresholds you control in `config.json` — nothing hardcoded
- Email alerts over SMTP/TLS when warnings fire
- All runs appended to `health.log` with timestamps
- Color-coded terminal output with a clean summary table

## Requirements

Python 3.7+ and `psutil`. That's the only dependency.

```bash
pip install psutil
```

## Installation

```bash
git clone https://github.com/your-username/server-health-monitor.git
cd server-health-monitor
pip install psutil
```

## Usage

```bash
python monitor.py
```

Output goes to the terminal and gets appended to `health.log` in the same directory.

## Configuration

Everything lives in `config.json`:

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
| `cpu_percent` | `80` | CPU warning level (%) |
| `memory_percent` | `85` | RAM warning level (%) |
| `disk_percent` | `90` | Disk warning level (%) |

### Services

Put service names in the `"services"` array. The monitor checks if each one is running:

- Windows uses `sc query <service>`
- Linux uses `systemctl is-active <service>`

Use the exact name the OS knows it by — `nginx`, `sshd`, `mysql`, etc.

### Email alerts

Flip `"enabled"` to `true` and fill in your SMTP credentials. For Gmail you'll need an [App Password](https://support.google.com/accounts/answer/185833) — don't use your main account password.

## Sample output

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

If email is enabled and warnings fired, the alert goes out right after the report prints.

## Log file

Each run appends entries to `health.log`:

```
2026-04-10 14:32:07,412 - INFO - CPU - 23.4% - OK
2026-04-10 14:32:07,413 - INFO - Memory - 61.2% - OK
2026-04-10 14:32:07,414 - INFO - Disk - 91.8% - WARNING
2026-04-10 14:32:07,415 - INFO - Service: nginx - running - OK
2026-04-10 14:32:07,416 - INFO - Service: mysql - not running - WARNING
2026-04-10 14:32:07,417 - INFO - Service: redis - running - OK
```

## Automating runs

Linux/macOS via cron, every 5 minutes:

```bash
*/5 * * * * /usr/bin/python3 /path/to/monitor.py
```

Windows via Task Scheduler, point it at:

```
python C:\path\to\monitor.py
```

## License

MIT
