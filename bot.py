import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import google.generativeai as genai

# Configure Gemini AI (Yeh GitHub Secrets se API key uthayega)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Categories aur unke Full HD high-quality images ki list
LUXURY_DATABASE = [
    {
        "category": "LuxuryCars",
        "name": "Rolls-Royce Phantom Series II",
        "image": "https://images.unsplash.com/photo-1563720223185-11003d516935?q=80&w=1920&auto=format&fit=crop"
    },
    {
        "category": "PrivateJets",
        "name": "Gulfstream G700 Private Jet",
        "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?q=80&w=1920&auto=format&fit=crop"
    },
    {
        "category": "LuxuryWatches",
        "name": "Rolex Cosmograph Daytona",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1920&auto=format&fit=crop"
    },
    {
        "category": "Fashion",
        "name": "Haute Couture Red Evening Gown",
        "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?q=80&w=1920&auto=format&fit=crop"
    },
    {
        "category": "LuxuryTravel",
        "name": "Venice Simplon-Orient-Express Train",
        "image": "https://images.unsplash.com/photo-1515165562839-978bbcfc9282?q=80&w=1920&auto=format&fit=crop"
    },
    {
        "category": "Superyachts",
        "name": "Custom Luxury Superyacht",
        "image": "https://images.unsplash.com/photo-1569263979104-865ab9cd8d5c?q=80&w=1920&auto=format&fit=crop"
    }
]

def generate_ai_article(item_name, category):
    """Gemini AI se 300-500 words ka SEO optimized article likhwata hai"""
    prompt = f"""
    Write a high-quality, engaging, and SEO-optimized luxury lifestyle blog article about '{item_name}' in the '{category}' category. 
    The article must be around 300 to 500 words long. 
    Make it sound professional, aspirational, and appealing to wealthy lifestyle readers. 
    Do not include any markdown code blocks in your output, just provide clean HTML paragraphs (<p>...</p>) and subheadings (<h2>...</h2>) so it can be directly posted to a blog.
    """
    
    # Using Gemini 1.5 Flash for fast and smart generation
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def send_to_blogger():
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    blogger_email = "khageshwarbarik1111.myblogs@blogger.com"
    
    # Roz ek random item select hoga
    selected_item = random.choice(LUXURY_DATABASE)
    item_name = selected_item["name"]
    category = selected_item["category"]
    image_url = selected_item["image"]
    
    print(f"Generating article for: {item_name}...")
    
    # AI se lamba article generate karwayenge
    article_body = generate_ai_article(item_name, category)
    
    # Email message setup
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = blogger_email
    msg['Subject'] = f"{item_name} - Luxury Lifestyle Review #{category}"
    
    # Final HTML template with Full HD image and AI article
    html_content = f"""
    <div>
        {article_body}
        <br><br>
        <div style="text-align: center;">
            <img src="{image_url}" alt="{item_name}" style="max-width:100%; height:auto; border-radius: 8px;" />
        </div>
        <br><br>
        <p style="font-size: 14px; color: #666;"><b>Tags:</b> #{category} #LuxuryLifestyle #HighEndLiving</p>
    </div>
    """
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, blogger_email, msg.as_string())
        server.quit()
        print(f"Success! AI article and HD photo posted for {item_name}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_to_blogger()
    
