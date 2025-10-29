# Garuda Web App

A Flask-based crash test application with Azure Application Insights integration for monitoring and alerting.

## Features

- 🔥 **Intentional Crash Testing**: Trigger controlled application failures
- 📊 **Azure Application Insights**: Real-time monitoring and telemetry
- 🚨 **Exception Tracking**: Automatic error logging and alerting
- 🎨 **Modern UI**: Clean, responsive interface with Tailwind CSS

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Aawanshk/Garudawebapp.git
cd Garudawebapp
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Azure Application Insights connection string:
   ```
   APPLICATIONINSIGHTS_CONNECTION_STRING=your-actual-connection-string-here
   ```

### 5. Get Azure Application Insights Connection String
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Application Insights resource
3. Go to **Overview** section
4. Copy the **Connection String**
5. Paste it in your `.env` file

### 6. Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Project Structure

```
garuda_web_app/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in git)
├── .env.example       # Environment template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | Azure Application Insights connection string | Yes |
| `FLASK_DEBUG` | Enable Flask debug mode | No (default: True) |
| `SECRET_KEY` | Flask secret key for sessions | No (auto-generated for dev) |

## Usage

1. **Access the application** at `http://localhost:5000`
2. **Click "Trigger Critical Crash"** to generate an intentional exception
3. **Check Application Insights** in Azure Portal to see the telemetry data
4. **Set up alerts** in Azure Monitor to get notified of crashes

## Deployment

### Azure App Service
1. Create an Azure App Service
2. Enable Application Insights integration
3. Deploy directly from GitHub or using Azure CLI

### Manual Deployment
1. Set environment variables in your hosting platform
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application with a production WSGI server

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## License

This project is licensed under the MIT License.