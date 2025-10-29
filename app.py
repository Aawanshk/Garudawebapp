import os
import sys
from flask import Flask, render_template_string, redirect, url_for
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import AlwaysOnSampler
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Application Insights Setup (CRITICAL) ---
# The connection string will be loaded from .env file for local development
# or from Azure App Service environment variables in production
CONNECTION_STRING = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

# 1. Initialize Flask App
app = Flask(__name__)

# Configure Flask app from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# 2. Configure OpenCensus Middleware for Flask
if CONNECTION_STRING:
    try:
        # This middleware automatically tracks requests, exceptions, dependencies, etc.
        middleware = FlaskMiddleware(
            app=app,
            exporter_mode='azure',
            connection_string=CONNECTION_STRING,
            sampler=AlwaysOnSampler() # Ensure all telemetry is sent
        )
        print("Application Insights Middleware initialized successfully.")
    except Exception as e:
        print(f"Error initializing Application Insights: {e}", file=sys.stderr)
        # Continue running the app even if telemetry fails
else:
    print("WARNING: APPLICATIONINSIGHTS_CONNECTION_STRING not found. Telemetry disabled.", file=sys.stderr)

# 3. Configure a Logger (Optional, for custom logging)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Attach the AzureLogHandler to the logger if connection string exists
if CONNECTION_STRING:
    logger.addHandler(AzureLogHandler(connection_string=CONNECTION_STRING))
    logger.info("Custom logger set up with Azure Application Insights.")


# --- Application Logic ---

def intentional_crash():
    """Function designed to raise an unhandled exception."""
    logger.critical("INTENTIONAL_CRASH_TRIGGERED: Preparing to raise a ValueError.")
    # This unhandled exception will result in a 500 Internal Server Error
    # and will be automatically tracked by Application Insights.
    raise ValueError("IntentionalCrash: The system received a direct instruction to fail.")

@app.route('/')
def index():
    """Main page with the crash button."""
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>The Crash App</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
            <style>
                body { font-family: 'Inter', sans-serif; }
            </style>
        </head>
        <body class="bg-gray-50 min-h-screen flex items-center justify-center p-4">
            <div class="bg-white p-8 md:p-10 rounded-xl shadow-2xl w-full max-w-lg text-center">
                <h1 class="text-4xl font-bold text-red-600 mb-6">Crash Test App</h1>
                <p class="text-gray-600 mb-8">
                    This application is configured to intentionally generate a Python unhandled exception
                    when the button below is pressed. This will trigger an Exception telemetry event
                    in Azure Application Insights, which in turn will fire an Azure Monitor alert.
                </p>

                <form method="POST" action="/crash">
                    <button type="submit" id="crashButton"
                        class="w-full px-6 py-3 text-lg font-semibold rounded-lg text-white transition duration-300
                               bg-red-500 hover:bg-red-600 focus:ring-4 focus:ring-red-300 focus:outline-none
                               shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98]">
                        Trigger Critical Crash
                    </button>
                </form>

                <p id="loadingMessage" class="mt-4 text-red-500 font-medium hidden">
                    Crash initiated... The system is intentionally failing. Check Application Insights!
                </p>
                
                <div class="mt-8 pt-6 border-t border-gray-100">
                    <p class="text-sm text-gray-400">
                        Monitoring Status: 
                        <span class="font-mono text-xs text-green-500 bg-green-50/50 rounded-md px-1 py-0.5">
                            Application Insights Enabled (via environment variable)
                        </span>
                    </p>
                </div>
            </div>
            <script>
                document.getElementById('crashButton').addEventListener('click', function(event) {
                    // Prevent multiple submissions
                    this.disabled = true;
                    this.classList.remove('hover:bg-red-600', 'hover:shadow-xl', 'hover:scale-[1.02]');
                    this.classList.add('bg-red-400', 'cursor-not-allowed');
                    this.textContent = 'Crashing...';
                    document.getElementById('loadingMessage').classList.remove('hidden');
                });
            </script>
        </body>
        </html>
    """)

@app.route('/crash', methods=['POST'])
def crash_endpoint():
    """Endpoint that causes the intentional crash."""
    # Call the function that raises the unhandled exception
    intentional_crash()
    # Note: This line will never be reached due to the unhandled exception above.
    return "Should never be seen", 500

if __name__ == '__main__':
    # When running locally, Flask runs in single-threaded debug mode,
    # which sometimes prevents Application Insights from immediately flushing telemetry.
    # In Azure App Service, Gunicorn handles the threading and graceful exit.
    print("Running Flask app locally. Remember to set APPLICATIONINSIGHTS_CONNECTION_STRING for telemetry.")
    app.run(host='0.0.0.0', port=5000)
