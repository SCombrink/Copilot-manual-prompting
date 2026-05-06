# Copilot-manual-prompting
This is a repository of manual copilot prompt, where you don't have access to api and need to open a browser to interact with copilot. 

How to set it up:

Place the files in the same folder as your existing copilot.py:

your-folder/   
├── copilot.py          ← your original script (renamed)   
├── app.py              ← new Flask backend   
├── requirements.txt   
└── static/       
    └── index.html      ← the UI

Install dependencies:

pip install flask playwright

Run it:

python app.py

Open your browser at http://localhost:5000
