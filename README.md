======================================================
        DJANGO ADMIN MANAGEMENT CHATBOT
======================================================

A lightweight, Natural Language Processing (NLP) chatbot built in Django that allows administrators to manage user records (add, update, delete) directly through a conversational interface. 

The bot uses Regular Expressions (Regex) to parse commands, meaning it runs entirely locally without needing third-party AI APIs.

--- FEATURES ---
* Natural Language Database Operations: Add, update, and remove users using plain English.
* Floating Chat UI: A persistent, toggleable chat interface fixed to the bottom right of the screen (Bootstrap 5).
* Admin-Only Access: The chat interface and backend API are strictly restricted to users with `is_admin=True`.
* Seamless Background Updates: Frontend data table updates instantly in the background without refreshing the page or clearing the chat history.

--- TECH STACK & PREREQUISITES ---
* Backend: Python 3.12.6, Django 4.2.23
* Frontend: HTML5, Bootstrap 5 (CSS & Icons), Vanilla JavaScript
* Database: SQLite (Default Django DB)

Note: To check your Django version in the terminal, use `django-admin --version` or `python -m django --version`. (Typing just `django --version` will return an error).

======================================================
               INSTALLATION & SETUP
======================================================

1. Create and activate a virtual environment:
   > python -m venv venv
   > .\venv\Scripts\activate      (For Windows)
   > source venv/bin/activate     (For Mac/Linux)

2. Install Django (Specific Version):
   > pip install django==4.2.23

3. Apply database migrations:
   > python manage.py makemigrations
   > python manage.py migrate

4. Run the development server:
   > python manage.py runserver

======================================================
        HOW TO CREATE YOUR FIRST ADMIN
======================================================

Before using the chatbot, you must create an Admin account through the Django dashboard:

1. Create a Django superuser (so you can access the admin panel):
   > python manage.py createsuperuser
   (Follow the prompts to set username and password)

2. Run the server and go to the Django Admin panel: 
   http://127.0.0.1:8000/admin

3. Log in, go to your 'Users' table, and click "Add User".
4. Fill in the email, password, phone number, and city.
5. CRUCIAL STEP: Make sure you check the box for `is_admin = True`. 
6. Save the record. You have successfully created an Admin user!

7. Now, CLOSE the Django Admin dashboard and visit your app's regular Login page (http://127.0.0.1:8000/login/).

--- VISIBILITY RULES ---
* If you log in with the ADMIN account you just created, the chatbot icon will appear in the bottom right corner.
* If a regular USER logs in (where `is_admin = False`), the chatbot remains completely hidden and inaccessible.

======================================================
           HOW TO USE THE CHATBOT
======================================================

Once logged in as an Admin, click the floating chat icon and try the following commands:

1. ADD A USER
   You must provide at least an email and phone number.
   Command: add user john@xyz.com phone +123456789 password mysecretpass city New York

2. REMOVE A USER
   Command: remove user john@xyz.com
   (Also accepts "delete user john@xyz.com")

3. UPDATE A USER
   You can update one or multiple fields at once using the '[field] to [value]' syntax.
   Command (Single Field): update user john@xyz.com city to London
   Command (Multiple Fields): update user john@xyz.com phone to +987654 password to newpass123 city to Paris