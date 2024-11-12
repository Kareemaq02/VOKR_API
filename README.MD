# VOKR API

VOKR API is a Django-based chatbot API designed to handle user interactions with advanced AI models. This project integrates semantic search and AI model responses to assist customers with various tasks.

## Project Setup

To get started with this project, follow the steps below.

### 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/Kareemaq02/VOKR_API.git
cd VOKR_API
```

### 2. Install WSL (Windows Subsystem for Linux)

To run the project on Windows, you need to install WSL (Windows Subsystem for Linux). This will allow you to use Ubuntu or other Linux distributions within Windows.

Run the following command to install WSL:

```powershell
wsl --install
```

After installation, restart your machine and set up your WSL environment by following the prompts.

### 3. Create a Virtual Environment

Once inside the project directory, create a virtual environment to manage the dependencies:

```bash
python -m venv myenv
```

Activate the virtual environment:

```bash
# On Windows
myenv\Scripts\activate

# On Linux/macOS
source myenv/bin/activate
```

### 4. Install Project Dependencies

Install all necessary dependencies by running:

```bash
pip install -r requirements.txt
```

### 5. Set Up the `.env` File

Create a `.env` file in the project root directory to configure sensitive information such as your database settings and secret keys.

Here’s a sample `.env` file to get started:

```ini
# .env

# Database configuration
DB_NAME=VOKR
DB_USER=root
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=3306

# Other sensitive information
SECRET_KEY=your_secret_key_here
DEBUG=True
```

**Important:** Replace `your_password_here` and `your_secret_key_here` with your actual database password and secret key.

### 6. Install and Set Up Llama3.1

This project uses the Llama3.1 model for AI interactions. You will need to install and set up `ollama` to run this model.

First, open your WSL terminal (Ubuntu or your preferred distribution). Then, install `ollama` within WSL:

```bash
# Inside WSL
curl -sSL https://ollama.com/install.sh | bash
```

Once installed, pull the model:

```bash
# Inside WSL
ollama pull llama3.1
```

# Run the database creation command

To Initialize the database, run the following command:

```bash
python manage.py create_database
```

### 7. Run Migrations

Before running the project, you need to apply database migrations to set up the necessary tables. Run the following command:

```bash
python manage.py migrate
```

### 8. Start the Development Server

You can now start the Django development server to run the project locally:

```bash
python manage.py runserver
```

The API will be accessible at `http://127.0.0.1:8000/`.

## Project Description

VOKR API is a chatbot application built with Django and various AI models to provide efficient and effective customer support. The API includes features like handling user messages, fetching session data, and generating AI responses using a semantic search and the Llama3.1 model.

The goal of this project is to create a robust system that can assist customers with a wide range of questions, including product details, shipping, returns, and more. The integration with machine learning models ensures that responses are accurate and tailored to each user's query.

## Troubleshooting

- If you encounter issues related to the `.env` file, make sure the file is correctly formatted and placed in the root directory.
- If you face errors with `ollama`, ensure that the model is running properly and the required dependencies are installed.
- For database-related issues, double-check your `.env` file and confirm that your MySQL server is running.
