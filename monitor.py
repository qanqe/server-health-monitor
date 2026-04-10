import psutil
import json
import subprocess
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText

# Load config
with open("config.json") as f:
    config = json.load(f)

# Setup logging - saves results to a file called health.log
logging.basicConfig(
    filename="health.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def check_cpu():
    usage = psutil.cpu_percent(interval=1)
    status = "WARNING" if usage > config["thresholds"]["cpu_percent"] else "OK"
    return {"metric": "CPU", "value": f"{usage}%", "status": status}

def check_memory():
    mem = psutil.virtual_memory()
    usage = mem.percent
    status = "WARNING" if usage > config["thresholds"]["memory_percent"] else "OK"
    return {"metric": "Memory", "value": f"{usage}%", "status": status}

def check_disk():
    disk = psutil.disk_usage("/")
    usage = disk.percent
    status = "WARNING" if usage > config["thresholds"]["disk_percent"] else "OK"
    return {"metric": "Disk", "value": f"{usage}%", "status": status}

def check_services():
    results = []
    for service in config["services"]:
        try:
            result = subprocess.run(
                ["sc", "query", service],
                capture_output=True, text=True
            )
            status = "OK" if "RUNNING" in result.stdout else "WARNING"
            value = "running" if status == "OK" else "not running"
        except Exception:
            status = "WARNING"
            value = "not found"
        results.append({"metric": f"Service: {service}", "value": value, "status": status})
    return results
    
def send_alert(warnings):
    if not config["email"]["enabled"]:
        return
    body = "Server Health Warnings:\n\n"
    for w in warnings:
        body += f"{w['metric']}: {w['value']} - {w['status']}\n"
    msg = MIMEText(body)
    msg["Subject"] = "Server Health Alert"
    msg["From"] = config["email"]["sender"]
    msg["To"] = config["email"]["receiver"]
    with smtplib.SMTP(config["email"]["smtp_server"], config["email"]["smtp_port"]) as server:
        server.starttls()
        server.login(config["email"]["sender"], config["email"]["password"])
        server.send_message(msg)

def run():
    print(f"\n{'='*50}")
    print(f"  SERVER HEALTH REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    results = [check_cpu(), check_memory(), check_disk()] + check_services()
    warnings = []

    for r in results:
        icon = "✅" if r["status"] == "OK" else "⚠️"
        print(f"{icon}  {r['metric']:<25} {r['value']:<15} {r['status']}")
        logging.info(f"{r['metric']} - {r['value']} - {r['status']}")
        if r["status"] == "WARNING":
            warnings.append(r)

    print(f"{'='*50}")
    print(f"  Warnings: {len(warnings)} | Checked: {len(results)} metrics")
    print(f"{'='*50}\n")

    if warnings:
        send_alert(warnings)

if __name__ == "__main__":
    run()