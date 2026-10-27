import os
import random
import smtplib
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai

# ================= Configuration & Secrets =================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
BLOGGER_EMAIL = os.environ.get("BLOGGER_EMAIL", "khageshwarbarik1111.myblogs@blogger.com")

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


def clean_gemini_html(text: str) -> str:
    """Gemini ke response se extra markdown (```html ... ```) saaf karta hai"""
    text = text.strip()
    if text.startswith("```html"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def generate_ai_article(item_name: str) -> str:
    """Chota aur fast SEO optimized article generate karega"""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"Write a short, engaging luxury lifestyle blog post about '{item_name}' in about 150 to 200 words. "
            f"Make it sound professional, ultra-luxurious, and aspirational. "
            f"Use clean HTML tags like <h2> for headings and <p> for paragraphs. "
            f"Do NOT include markdown backticks (like ```html), <html>, or <body> tags. Return ONLY the raw inner HTML."
        )
        
        response = model.generate_content(prompt)
        return clean_gemini_html(response.text)
    except Exception as e:
        print(f"Error generating AI content: {e}")
        return None


def send_to_blogger():
    # Passwords aur Keys check
    if not all([GEMINI_API_KEY, SENDER_EMAIL, SENDER_PASSWORD]):
        print("Error: Missing environment variables! GEMINI_API_KEY, SENDER_EMAIL ya SENDER_PASSWORD missing hai.")
        return

    # Item choose karna
    item_name = random.choice(LUXURY_DATABASE)
    print(f"Generating article and Full HD image for: {item_name}...")
    
    # 1. Article generate karna
    article_body = generate_ai_article(item_name)
    if not article_body:
        print("Failed to generate article. Email nahi bheja gaya.")
        return

    # 2. Full HD (1920x1080) AI Image URL generation
    image_prompt = f"Ultra realistic, 8k resolution, professional luxury photography of {item_name}, high-end editorial style, cinematic lighting"
    encoded_prompt = urllib.parse.quote(image_prompt)
    random_seed = random.randint(1, 999999)  # Isse har baar bilkul nayi photo banegi
    
    # yahan width=1920 aur height=1080 (Full HD) set kiya gaya hai
    ai_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=true&seed={random_seed}"

    # 3. HTML Post structure
    html_content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #222;">
        {article_body}
        <br><br>
        <div style="text-align: center; margin-top: 25px;">
            <img src="{ai_image_url}" alt="{item_name}" style="max-width: 100%; height: auto; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
        </div>
    </div>
    """

    # 4. Email Setup
    msg = MIMEMultipart("alternative")
    msg['From'] = SENDER_EMAIL
    msg['To'] = BLOGGER_EMAIL
    msg['Subject'] = f"{item_name} - Exclusive Luxury Review"
    msg.attach(MIMEText(html_content, 'html'))

    # 5. Email send karna
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            
        print(f"Success! Full HD post successfully published for: {item_name}")
    except smtplib.SMTPAuthenticationError:
        print("SMTP Error: Gmail login fail! Gmail App Password sahi se check karein.")
    except Exception as e:
        print(f"Error sending email: {e}")


if __name__ == "__main__":
    send_to_blogger()
