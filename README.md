# L-earnC

Software developed for tech field students learn, dynamically, how to code in C.

## Getting started

1. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Initialize the database:
   ```
   flask --app app init-db
   ```
3. Launch the development server:
   ```
   flask --app app run
   ```

Visit `http://127.0.0.1:5000` to access the login and registration experience.
