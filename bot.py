import os
import random
import smtplib
import json
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai

# Environment Variables (Secrets se aayenge)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
BLOGGER_EMAIL = os.environ.get("BLOGGER_EMAIL", "khageshwarbarik1111.myblogss@blogger.com")


def generate_luxury_content():
    """Gemini se daily ek naya luxury product aur SEO content banwana"""
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = """
    Pick ONE unique, ultra-exclusive luxury product or lifestyle asset from around the world 
    (e.g., hypercars, rare tourbillon watches, superyachts, private islands, bespoke designer villas, exotic jewelry, private jets).
    
    Return your response strictly in valid JSON format with three keys:
    {
      "title": "SEO friendly catching title including the product name",
      "image_prompt": "Ultra-detailed visual prompt describing this luxury item in 8k cinematic lighting, ultra-realistic photography",
      "html_content": "Detailed, highly engaging SEO-optimized blog post (250-350 words). Include <h2> headings, <p> paragraphs, and a key features <ul> bullet list. Only pure HTML tags, no markdown backticks."
    }
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Content generation error: {e}")
        return None


def send_to_blogger():
    if not all([GEMINI_API_KEY, SENDER_EMAIL, SENDER_PASSWORD]):
        print("Error: Environment variables missing!")
        return

    print("Generating today's luxury post...")
    data = generate_luxury_content()
    if not data:
        print("Failed to generate content.")
        return

    title = data.get("title")
    image_prompt = data.get("image_prompt")
    article_html = data.get("html_content")

    # 1. Full HD (1920x1080) AI Image URL
    encoded_prompt = urllib.parse.quote(image_prompt)
    random_seed = random.randint(100000, 999999)
    ai_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=true&seed={random_seed}"

    # 2. Complete HTML Post formatting
    full_body = f"""
    <div style="font-family: Arial, sans-serif; font-size: 16px; line-height: 1.8; color: #222;">
        <div style="text-align: center; margin-bottom: 25px;">
            <img src="{ai_image_url}" alt="{title}" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);" />
        </div>
        <div>
            {article_html}
        </div>
    </div>
    """

    # 3. Email Setup
    msg = MIMEMultipart("alternative")
    msg['From'] = SENDER_EMAIL
    msg['To'] = BLOGGER_EMAIL
    msg['Subject'] = title
    msg.attach(MIMEText(full_body, 'html'))

    # 4. Blogger ko Email bhejna
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"Success! Post published: {title}")
    except Exception as e:
        print(f"Error publishing post: {e}")


if __name__ == "__main__":
    send_to_blogger()
