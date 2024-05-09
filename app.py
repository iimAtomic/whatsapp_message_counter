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
            
                # Create a green rounded rectangle background
                background = Image.new('RGBA', (800, 300), (255, 255, 255, 0))  # Transparent background
                d = ImageDraw.Draw(background)
                d.rounded_rectangle([(0, 0), (800, 300)], 30, fill=(153, 204, 102))

                # Define font
                font_path = 'fonts/arial.ttf'
                font_large = ImageFont.truetype(font_path, 80)
                font_small = ImageFont.truetype(font_path, 32)

                # Position and draw text
                d.text((100, 30), f"{user_name}", fill=(0, 0, 0), font=font_small)
                d.text((600, 30), f"{friend_name}", fill=(0, 0, 0), font=font_small)
                d.text((300, 110), f"{message_count}", fill=(0, 0, 0), font=font_large ,align=('center'),)
                d.text((300, 210), "Messages WhatsApp", fill=(0, 0, 0), font=font_small)
                d.text((300, 250), "Partagez", fill=(0, 0, 0), font=font_small)

                # Save and respond
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
        return "No file provided !", 400

def generate_unique_filename(user_name, friend_name):
    unique_id = uuid4()
    return f"static/images/{user_name}_{friend_name}_{unique_id}.png"

if __name__ == '__main__':
    app.run(debug=True)
