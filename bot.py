import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

# List of sample cars for the daily blog
CARS = [
    {
        "title": "Car of the Day: 2026 Tesla Model 3 Performance",
        "body": "The 2026 Tesla Model 3 Performance brings blistering acceleration, a revamped interior, and razor-sharp handling. A true electric icon for speed enthusiasts."
    },
    {
        "title": "Car of the Day: Hyundai Ioniq 5 N",
        "body": "The Hyundai Ioniq 5 N redefines what an EV can do with simulated gear shifts, incredible track capability, and aggressive styling."
    },
    {
        "title": "Car of the Day: Ford Mustang Dark Horse",
        "body": "Powered by a ferocious V8 engine, the Ford Mustang Dark Horse delivers raw American muscle power paired with advanced track tech."
    },
    {
        "title": "Car of the Day: Toyota GR Supra",
        "body": "A blend of precision engineering and sports car heritage, the Toyota GR Supra offers unmatched driving thrills on every twisty road."
    }
]

def send_to_blogger():
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    blogger_email = "khageshwarbarik1111.myblogs@blogger.com"
    
    # Pick a random car for today
    car = random.choice(CARS)
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = blogger_email
    msg['Subject'] = car['title']
    
    msg.attach(MIMEText(car['body'], 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, blogger_email, msg.as_string())
        server.quit()
        print("Blog post sent successfully via email!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_to_blogger()
