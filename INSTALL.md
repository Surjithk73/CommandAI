# Installation Guide

Follow these steps to set up and run the AI-Powered Command Line Interface:

## Prerequisites

- Python 3.8 or later
- Pip (Python package installer)
- An OpenRouter API key with access to the Llama model or other LLM

## Setup Steps

1. **Clone or download the repository**

2. **Create a virtual environment**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```
   # On Windows
   venv\Scripts\activate
   ```

4. **Install the required dependencies**
   ```
   pip install -r requirements.txt
   ```

5. **Configure your API key**
   - Copy the `.env.example` file to a new file called `.env`
   - Replace `your_api_key_here` with your actual OpenRouter API key

## Running the Application

Run the application using one of the following methods:

**Using run.py:**
```
python run.py
```

**Directly from the source directory:**
```
python src/main.py
```

## Running Tests

To run the unit tests:
```
python -m unittest discover tests
```

## Troubleshooting

- If you encounter an error about missing modules, make sure you've activated the virtual environment and installed all dependencies.
- If you get an API error, check that your API key is correctly set in the `.env` file.
- For UI rendering issues, ensure you have the necessary Qt dependencies installed on your system. 