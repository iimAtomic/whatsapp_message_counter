from flask import Flask, request, send_file, render_template, jsonify
import zipfile
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from uuid import uuid4

app = Flask(__name__)

visits_file_path = 'visit_count.txt'

def get_visit_count():
    try:
        with open(visits_file_path, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def update_visit_count():
    count = get_visit_count() + 1
    with open(visits_file_path, 'w') as file:
        file.write(str(count))
    return count

@app.route('/')
def index():
   visits = update_visit_count()
   return render_template('index.html', visits=visits)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    user_name = request.form['userName']
    friend_name = request.form['friendName']
    if file:
        zip_path = 'temp/zipfile.zip'
        file.save(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('temp')

        messages_path = None
        for filename in os.listdir('temp'):
            if filename.endswith('.txt'):
                messages_path = os.path.join('temp', filename)
                break

        if messages_path and os.path.exists(messages_path):
            try:
                with open(messages_path, 'r', encoding='utf-8') as f:
                    messages = f.readlines()
                message_count = len(messages)
            
                # Create a modern gradient background with rounded corners
                background = Image.new('RGBA', (800, 400), (255, 255, 255, 0))  # Transparent background
                draw = ImageDraw.Draw(background)
                
                # Gradient background
                for i in range(400):
                    draw.line([(0, i), (800, i)], fill=(153 - i//4, 204 - i//4, 102 + i//8))
                
                # Rounded rectangle with shadow
                rounded_rect = Image.new('RGBA', (750, 350), (255, 255, 255, 255))
                d = ImageDraw.Draw(rounded_rect)
                d.rounded_rectangle([(0, 0), (750, 350)], 30, fill=(255, 255, 255, 230))
                shadow = ImageOps.expand(rounded_rect, border=10, fill=(0, 0, 0, 128))
                background.paste(shadow, (25, 25), shadow)
                background.paste(rounded_rect, (25, 25), rounded_rect)

                # Define font paths and sizes
                font_path_bold = 'fonts/arialbd.ttf'  # Bold font
                font_path_regular = 'fonts/arial.ttf'  # Regular font
                font_large = ImageFont.truetype(font_path_bold, 80)
                font_medium = ImageFont.truetype(font_path_bold, 50)
                font_small = ImageFont.truetype(font_path_regular, 30)
                
                # Draw names
                draw.text((50, 50), f"{user_name}", fill=(51, 51, 51), font=font_medium)
                draw.text((600, 50), f"{friend_name}", fill=(51, 51, 51), font=font_medium)
                
                # Draw message count
                draw.text((300, 150), f"{message_count}", fill=(0, 102, 51), font=font_large, align='center')
                
                # Draw additional text
                draw.text((280, 240), "WhatsApp Messages", fill=(102, 102, 102), font=font_small)
                draw.text((320, 290), "Share this!", fill=(102, 102, 102), font=font_small)
                
                # Save and respond with the image path
                image_path = generate_unique_filename(user_name, friend_name)
                background.save(image_path)

                os.remove(messages_path)
                os.remove(zip_path)
                
                return jsonify({'image_url': image_path})
            except UnicodeDecodeError:
                return "Unicode decode error", 400
        else:
            os.remove(zip_path)
            return "No text file found in the ZIP.", 400
    else:
        return "No file provided!", 400

def generate_unique_filename(user_name, friend_name):
    unique_id = uuid4()
    return f"static/images/{user_name}_{friend_name}_{unique_id}.png"

if __name__ == '__main__':
    app.run(debug=True)
