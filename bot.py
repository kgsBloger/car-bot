import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

# List of items with specific tags/labels according to the photo and category
ITEMS = [
    {
        "title": "Luxury Car of the Day: Rolls-Royce Phantom Series II",
        "body": "The epitome of bespoke luxury and effortless power. The Rolls-Royce Phantom Series II offers a majestic presence, handcrafted interior, and a silent 'magic carpet' ride that redefines automotive elegance.",
        "image": "https://images.unsplash.com/photo-1563720223185-11003d516935?q=80&w=1920&auto=format&fit=crop",
        "tag": "LuxuryCars"
    },
    {
        "title": "Private Jet of the Day: Gulfstream G700",
        "body": "Redefining ultra-long-range private aviation, the Gulfstream G700 features the most spacious cabin in the industry, biophilic lighting, ultra-comfortable seating, and breathtaking cruising speeds.",
        "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?q=80&w=1920&auto=format&fit=crop",
        "tag": "PrivateJets"
    },
    {
        "title": "Luxury Watch of the Day: Rolex Cosmograph Daytona",
        "body": "A masterpiece of horological engineering. Designed for endurance racing drivers, the Rolex Daytona combines high-performance chronograph precision with timeless luxury and iconic design.",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1920&auto=format&fit=crop",
        "tag": "LuxuryWatches"
    },
    {
        "title": "Haute Couture Dress of the Day: Elegant Red Evening Gown",
        "body": "Crafted from finest silk chiffon with intricate hand-stitched detailing, this haute couture gown captures timeless grace, sophistication, and a dramatic silhouette for grand occasions.",
        "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?q=80&w=1920&auto=format&fit=crop",
        "tag": "Fashion"
    },
    {
        "title": "Luxury Train Journey: The Venice Simplon-Orient-Express",
        "body": "Step back into the golden age of travel. The Venice Simplon-Orient-Express offers legendary vintage cabins, exquisite fine dining, and breathtaking alpine views across Europe.",
        "image": "https://images.unsplash.com/photo-1515165562839-978bbcfc9282?q=80&w=1920&auto=format&fit=crop",
        "tag": "LuxuryTravel"
    },
    {
        "title": "Luxury Superyacht of the Day: Custom Ocean Master",
        "body": "The ultimate symbol of marine luxury. Featuring multi-deck infinity pools, helipads, lavish state rooms, and state-of-the-art navigation for unrivaled oceanic adventures.",
        "image": "https://images.unsplash.com/photo-1569263979104-865ab9cd8d5c?q=80&w=1920&auto=format&fit=crop",
        "tag": "Superyachts"
    }
]

def send_to_blogger():
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    blogger_email = "khageshwarbarik1111.myblogs@blogger.com"
    
    # Pick a random item for today
    item = random.choice(ITEMS)
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = blogger_email
    msg['Subject'] = f"{item['title']} #{item['tag']}"
    
    # HTML body with Full HD image and matching tag display
    html_content = f"""
    <div>
        <p style="font-size: 16px; line-height: 1.6;">{item['body']}</p>
        <br>
        <img src="{item['image']}" alt="{item['title']}" style="max-width:100%; height:auto; border-radius: 8px;" />
        <br><br>
        <p style="font-size: 14px; color: #666;"><b>Tags:</b> #{item['tag']} #LuxuryLifestyle</p>
    </div>
    """
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, blogger_email, msg.as_string())
        server.quit()
        print("Daily luxury post with photo and tag sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_to_blogger()
