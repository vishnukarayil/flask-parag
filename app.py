# app.py
import openai
from flask import Flask, request, render_template
import os

# Set up Flask app
app = Flask(__name__)

# Set the page title and icon
favicon_path = os.path.join(os.path.dirname(__file__), 'cropped-PathonotesLogowithin.png')
app.config['PAGE_TITLE'] = "PARAG - Pathology AI Research Assistant"
app.config['PAGE_ICON'] = favicon_path

# Authenticate OpenAI API Key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define the search_in_gpt3 function
def search_in_gpt3(query):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f'respond like an AI assistant for pathology research. We need it to generate factually correct answers for queries submitted by the user. User is a student in pathology and his questions are all related to pathology. The api will be used in a web app that is accessed in the pathology library pc in our medical college. There is no room for error. A single instance of a grossly wrong fact will ruin our reputation. So first, the api should cross check whether the question is correct. If the user ask about a made uo word which is not a recognizable disease,you should ask the user to rephrase the question. Use markdown syntax for styling. Use headings wherever necessary. \n\nQuery: {query}\n\nResponse:',
        max_tokens=1024,
        top_p=1,
        n=1,
        frequency_penalty=0,
        presence_penalty=0,
        temperature=0.7,
    )
    return response.choices[0].text

# Define the routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        response = search_in_gpt3(query)
        return render_template('index.html', response=response)
    else:
        return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
