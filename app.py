from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import re

app = Flask(__name__)

# Load the Excel file
df = pd.read_excel('drug.xlsx')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    symptoms = request.form.get('symptoms')

    if symptoms:
        symptoms = symptoms.strip().lower().split(',')
        symptoms = [sym.strip() for sym in symptoms]

        results = []
        for _, row in df.iterrows():
            about_text = row['About'].lower()
            if all(sym in about_text for sym in symptoms):
                # Highlight matching words in red, bold, and uppercase
                highlighted_about = row['About']
                for sym in symptoms:
                    highlighted_about = re.sub(rf'\b({re.escape(sym)})\b', r'<span class="highlight">\1</span>', highlighted_about, flags=re.IGNORECASE)
                
                results.append({
                    'name': row['Name'],
                    'image': row['Image'],
                    'about': highlighted_about,  # Use the highlighted about text
                })

        # Redirect to the index page with results as a query parameter
        return render_template('index.html', results=results, symptoms=symptoms)

    return redirect(url_for('index'))  # Redirect to index if no symptoms are provided

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
