from flask import Flask, render_template, request
import pandas as pd
import os
import random
import openai

app = Flask(__name__)

# Define the static folder
STATIC_FOLDER = "/Users/ayushthapaliya/Desktop/AI/static"
app.config['STATIC_FOLDER'] = STATIC_FOLDER
api_key = "yourkey"
openai.api_key = api_key

def read_caption():
    caption_path = "/Users/ayushthapaliya/Desktop/AI/archive/captions.txt"
    captions_df = pd.read_csv(caption_path, sep=',')
    return captions_df

def elaborate_caption(initial_caption):
    prompt = f"Generate a more detailed description based on the following caption:\n\"{initial_caption}\""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Update the predict_captions function
def predict_captions(image_name):
    captions_df = read_caption()
    matching_captions = captions_df[captions_df['image'] == image_name]['caption'].tolist()
    if matching_captions:
        initial_caption = random.choice(matching_captions)
        detailed_caption = elaborate_caption(initial_caption)
        return detailed_caption
    else:
        return "No caption found for this image."

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/index')
def index():
    captions_df = read_caption()
    return render_template('index.html', captions=captions_df)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Handle image upload and prediction
        uploaded_file = request.files['my_image']
        if uploaded_file.filename != '':
            image_name = uploaded_file.filename
            image_path = os.path.join(app.config['STATIC_FOLDER'], image_name)
            uploaded_file.save(image_path)
            prediction = predict_captions(image_name)
            img_path = image_name  # Set the img_path variable without the leading 'static'
            return render_template('index.html', prediction=prediction, img_path=img_path)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
