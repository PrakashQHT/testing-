import os
import psutil
from datetime import datetime
from email.message import EmailMessage
import ssl
import smtplib


email_sender = 'gokulrajargr681@gmail.com'
email_password = "ykki bioq tzyv xyks"  
email_receiver = 'prakash@quehive.com'
hostname = os.uname()[1]

subject = "Daily System Resource Usage Report"

def send_email(body):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def check_system():
    disk_usage = psutil.disk_usage('/')
    disk_percent = disk_usage.percent


    memory = psutil.virtual_memory()
    memory_percent = memory.percent
 
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())


    load_avg = os.getloadavg()


    processes = sorted(psutil.process_iter(attrs=['pid', 'name', 'memory_percent']), key=lambda p: p.info['memory_percent'], reverse=True)
    top_process = processes[0].info


    disk_threshold = 60.0  
    memory_threshold = 60.0  
    load_avg_threshold = 2.0  


    body = f"""
    System Resource Usage Report: {hostname}

    Disk Usages: {disk_percent}%
    Memory Usages: {memory_percent}%
    Uptime: {uptime}
    Load Average : {load_avg}
    
    Top Process:
    PID: {top_process['pid']}
    Name: {top_process['name']}
    Memory Usage: {top_process['memory_percent']:.2f}%
    """

    if disk_percent > disk_threshold:
        body += f"\nWARNING: Disk usage is above {disk_threshold}%!"
    if memory_percent > memory_threshold:
        body += f"\nWARNING: Memory usage is above {memory_threshold}%!"
    if load_avg[0] > load_avg_threshold:
        body += f"\nWARNING: Load average is above {load_avg_threshold}!"
    if disk_percent > disk_threshold or memory_percent > memory_threshold or load_avg[0] > load_avg_threshold:
        send_email(body)
    else:
        print("System usage is within normal limits. No email sent.")

check_system()
