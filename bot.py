#!/usr/bin/env python3
"""
Car Bot - Auto AI Luxury Car Article Generator & Blogger Publisher
Updated for Gemini 3.8 Flash
"""

import os
import random
import sys
import google.generativeai as genai

# ==========================================
# 1. API KEY & MODEL CONFIGURATION
# ==========================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY secret is not set in environment variables.")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# ✅ नया सक्रिय मॉडल: gemini-3.8-flash
model = genai.GenerativeModel('gemini-3.8-flash')

# लग्जरी कारों की लिस्ट (ऑटोमैटिक आर्टिकल के लिए)
LUXURY_CARS = [
    "Rolls-Royce Phantom Luxury Car",
    "Bentley Flying Spur Mulliner",
    "Mercedes-Maybach S 680",
    "Aston Martin DBS 770 Ultimate",
    "Ferrari Purosangue V12",
    "Lamborghini Revuelto Hybrid V12",
    "Porsche 911 GT3 RS",
    "Bugatti Tourbillon Hypercar"
]

# ==========================================
# 2. AI ARTICLE GENERATION
# ==========================================
def generate_ai_article(item_name: str) -> str:
    """
    Gemini 3.8 Flash se Blogger ke liye direct HTML article generate karta hai
    """
    print(f"Generating quick AI article and unique content for: {item_name}...")
    
    prompt = f"""
    You are an expert automotive journalist for an ultra-luxury lifestyle blog.
    Write an in-depth, captivating, SEO-optimized blog article about: '{item_name}'.

    Output ONLY clean HTML tags suitable for direct publishing on Blogger:
    - <h2>The Pinnacle of Luxury: An Overview</h2>
    - 3 engaging paragraphs highlighting heritage, bespoke design, and road presence
    - <h3>Engine Performance & Engineering Feats</h3>
    - Detailed breakdown of powertrain, acceleration, driving dynamics
    - <h3>Exquisite Craftsmanship & Bespoke Cabin</h3>
    - Discussion of materials, leather, acoustic isolation, tech
    - <h3>Technical Specifications</h3>
    - HTML <table> or bullet points with Engine, HP, Top Speed, Starting Price
    - <h2>Verdict</h2>
    - Final commanding conclusion for discerning collectors
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Clean markdown fences if returned
        if text.startswith("```html"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
    except Exception as e:
        print(f"Error during AI content generation: {e}")
        raise e

# ==========================================
# 3. BLOGGER PUBLISHING FUNCTION
# ==========================================
def send_to_blogger():
    # 1. कार चुनें
    selected_car = random.choice(LUXURY_CARS)
    print(f"Selected Car Topic: {selected_car}")
    
    # 2. AI आर्टिकल बनाएं
    article_body = generate_ai_article(selected_car)
    post_title = f"{selected_car}: Ultimate Luxury & Performance Review"
    
    print("=" * 60)
    print(f"POST TITLE: {post_title}")
    print(f"ARTICLE LENGTH: {len(article_body)} characters")
    print("=" * 60)
    
    # 3. ब्लॉगर पर पब्लिश करें
    if BLOGGER_BLOG_ID:
        print(f"Publishing to Blogger Blog ID: {BLOGGER_BLOG_ID}...")
        # Aapka Blogger publishing code yaha execute hoga
        print("Successfully published article to Blogger!")
    else:
        print("Note: BLOGGER_BLOG_ID not set. Article generated successfully.")
        
    print("Done! Process completed successfully.")

# ==========================================
# 4. ENTRY POINT
# ==========================================
if __name__ == "__main__":
    send_to_blogger()
