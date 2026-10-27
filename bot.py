import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import urllib.parse
import google.generativeai as genai

# Configure Gemini AI (GitHub Secrets se API key uthayega)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Luxury items ki list (AI inke liye har baar nayi photo aur article banayega)
LUXURY_DATABASE = [
    "Rolls-Royce Phantom Luxury Car",
    "Gulfstream G700 Private Jet",
    "Rolex Cosmograph Daytona Gold Watch",
    "Haute Couture Luxury Evening Gown",
    "Venice Simplon-Orient-Express Luxury Train",
    "Custom Designer Superyacht",
    "Penthouse Suite with Ocean View",
    "Diamond Encrusted Luxury Smartphone"
]

def generate_ai_article(item_name):
    """Gemini AI se 300-500 words ka SEO optimized article likhwata hai"""
    prompt = f"""
    Write a high-quality, engaging, and SEO-optimized luxury lifestyle blog article about '{item_name}'. 
    The article must be around 300 to 500 words long. 
    Make it sound professional, aspirational, and appealing to wealthy lifestyle readers. 
    Do not include any markdown code blocks in your output, just provide clean HTML paragraphs (<p>...</p>) and subheadings (<h2>...</h2>) so it can be directly posted to a blog.
    """
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

def send_to_blogger():
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    blogger_email = "khageshwarbarik1111.myblogs@blogger.com"
    
    # Roz ek random luxury item select hoga
    item_name = random.choice(LUXURY_DATABASE)
    
    print(f"Generating AI article and unique AI image for: {item_name}...")
    
    # 1. AI se lamba article generate karwayenge
    article_body = generate_ai_article(item_name)
    
    # 2. AI Image Generator URL (Item ke naam ke hisab se har baar ekdum nayi HD photo banayega)
    image_prompt = f"Ultra realistic, 8k resolution, professional luxury photography of {item_name}, high-end editorial style, stunning lighting"
    encoded_prompt = urllib.parse.quote(image_prompt)
    ai_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true"
    
    # Email message setup
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = blogger_email
    msg['Subject'] = f"{item_name} - Exclusive Luxury Review"
    
    # Final HTML template with AI generated image and AI article
    html_content = f"""
    <div>
        {article_body}
        <br><br>
        <div style="text-align: center;">
            <img src="{ai_image_url}" alt="{item_name}" style="max-width:100%; height:auto; border-radius: 8px;" />
        </div>
        <br><br>
        <p style="font-size: 14px; color: #666;"><b>Tags:</b> #LuxuryAI #HighEndLiving #ExclusiveDesign</p>
    </div>
    """
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, blogger_email, msg.as_string())
        server.quit()
        print(f"Success! Unique AI image and article posted for {item_name}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_to_blogger()
    
