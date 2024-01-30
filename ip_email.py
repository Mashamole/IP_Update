
import re
import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def check_file_exists(filename):
    return os.path.isfile(filename)

def extract_recent_ips():
    ip_list = []
    if check_file_exists("test.txt") == True:
        command = "cat test.txt | tail -n 2"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        ip_text = output.decode()
        if error:
            print(f"Error: {error}")
            return "Error: NO IPS"
        else:
            print(f"ip_text:: {ip_text}")
            return ip_text.split("\n")
    else: 
        print("IP Log file does not exist")


def parse_ip_address():
  
    ipsRaw = extract_recent_ips()
    print(f"ips:: {ipsRaw}")
    ip_match = []
    # Regular expression pattern for an IP address
    pattern_ipv4 = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    pattern_ipv6 = r'\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b'
    for ip in ipsRaw: 
        # Search for the pattern in the line
        match_ipv4 = re.search(pattern_ipv4, ip)
        match_ipv6 = re.search(pattern_ipv6, ip)
        
        if match_ipv4:
            ip_match.append(match_ipv4.group())
        elif match_ipv6:
            ip_match.append(match_ipv6.group())
        else:
            ip_match.append("No IP address found in the line.")
    return ip_match

def check_ip_diff():
    ips = parse_ip_address()
    if ips[0] != ips[1]: 
        return 1,ips[1]
    else:
        return 0,ips[1]

## FOR TESTNG IP_LOG FILE 
# line = "01/21/24 - 00:00:05 --> 108.5.186.123"
# ip_address = parse_ip_address()


def send_email():
    # set up the SMTP server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()

    # Login Credentials for sending the mail
    server.login('ENTER EMAIL', 'ENTER APP CODE')

    # create a message
    msg = MIMEMultipart()

    # setup the parameters of the message
    msg['From'] = 'ENTER EMAIL'
    msg['To'] = 'ENTER EMAIL'
    msg['Subject'] = "IP Change Notification"

    ipStatusChange,ip = check_ip_diff()
    if ipStatusChange != 0: 
        print("Email notification")

        # add in the message body
        msg.attach(MIMEText(f'New Net IP address is ::\n\n {ip}', 'plain'))

        # send the message via the server
        server.send_message(msg)

        # Terminate the SMTP session and close the connection
        server.quit()

if __name__ == '__main__':
    send_email()
