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

# Luxury items ki list
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
    """100-200 words ka short aur fast SEO optimized article generate karega"""
    prompt = f"Write a short, engaging luxury lifestyle blog post about '{item_name}' strictly between 100 to 150 words. Make it professional and aspirational. Use clean HTML paragraphs (<p>...</p>) and subheadings (<h2>...</h2>)."
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

def send_to_blogger():
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    blogger_email = "khageshwarbarik1111.myblogs@blogger.com"
    
    item_name = random.choice(LUXURY_DATABASE)
    print(f"Generating quick AI article and unique image for: {item_name}...")
    
    article_body = generate_ai_article(item_name)
    
    image_prompt = f"Ultra realistic, 8k resolution, professional luxury photography of {item_name}, high-end editorial style"
    encoded_prompt = urllib.parse.quote(image_prompt)
    ai_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = blogger_email
    msg['Subject'] = f"{item_name} - Exclusive Luxury Review"
    
    html_content = f"""
    <div>
        {article_body}
        <br><br>
        <div style="text-align: center;">
            <img src="{ai_image_url}" alt="{item_name}" style="max-width:100%; height:auto; border-radius: 8px;" />
        </div>
    </div>
    """
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, blogger_email, msg.as_string())
        server.quit()
        print(f"Success! 100-200 words post sent for {item_name}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_to_blogger()
