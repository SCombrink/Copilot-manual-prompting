Copilot Manual Prompting

This repository provides a workaround for interacting with Copilot manually via a browser when API access is not available.


📁 Project Structure

Place the files in the same directory as your existing script:

    your-folder/
    ├── copilot.py        ← Your original script (renamed)
    ├── app.py            ← Flask backend
    ├── requirements.txt
    └── static/
        └── index.html    ← Web UI

 ⚙️ Setup Instructions

1. Install Dependencies

Install the required packages:
pip install flask playwright

2. Run the Application

Start the Flask server:
python app.py

3. Open the Interface

Navigate to the following URL in your browser:

    http://localhost:5000

 📝 Notes

*   This setup enables manual Copilot interaction through a browser-based UI.
*   Useful in environments where API access is restricted or unavailable.
*   Ensure all files are correctly placed as per the project structure.

Use client.py as your template to start writing your code. 
