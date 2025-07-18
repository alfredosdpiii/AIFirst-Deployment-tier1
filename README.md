# Tier 1: Streamlit Deployment Guide

This guide walks through deploying the ShopSage Streamlit app locally and to Streamlit Community Cloud.

## 🎯 Overview

Streamlit provides the fastest way to create and share data apps. Perfect for:
- Quick prototypes and demos
- Teaching and workshops
- Internal tools
- MVP testing

## 📋 Prerequisites

- Python 3.11 or higher
- Tavily API key
- OpenAI API key
- GitHub account (for cloud deployment)

## 🚀 Local Development

### 1. Setup Environment

```bash
# Navigate to Streamlit directory
cd shopsage/tier1-streamlit

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies using uv
uv sync
```

### 2. Configure API Keys

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
# Use your preferred editor (nano, vim, code, etc.)
nano .env
```

Add your API keys:
```env
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
```

### 3. Run Locally

```bash
# Start Streamlit app with uv
uv run streamlit run streamlit_app.py

# Or with specific port
uv run streamlit run streamlit_app.py --server.port 8501

# With browser auto-open disabled
uv run streamlit run streamlit_app.py --server.headless true
```

Your app will be available at: http://localhost:8501

## ☁️ Deploy to Streamlit Community Cloud

### 1. Prepare GitHub Repository

```bash
# Initialize git (if not already)
git init

# Create .gitignore
echo -e "venv/\n.env\n__pycache__/\n*.pyc\n.DS_Store" > .gitignore

# Add files
git add .
git commit -m "Initial ShopSage Streamlit app"

# Create GitHub repo and push
# Use GitHub CLI or create manually on github.com
gh repo create shopsage-streamlit --public
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub account
4. Select repository: `your-username/shopsage-streamlit`
5. Set branch: `main`
6. Set main file path: `tier1-streamlit/streamlit_app.py`

### 3. Configure Secrets

In Streamlit Cloud dashboard:

1. Click "Settings" → "Secrets"
2. Add your secrets in TOML format:

```toml
TAVILY_API_KEY = "tvly-xxxxxxxxxxxxxxxxxxxxx"
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxx"
OPENAI_MODEL = "gpt-4o-mini"
```

3. Click "Save"

### 4. Advanced Settings (Optional)

```toml
# In Streamlit Cloud settings
[server]
maxUploadSize = 200

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
```

## 🛠️ Development Tips

### Hot Reload
Streamlit automatically reloads when you save changes:
```bash
# Enable always rerun
uv run streamlit run streamlit_app.py --server.runOnSave true
```

### Debug Mode
```bash
# Run with debug logging
uv run streamlit run streamlit_app.py --logger.level debug
```

### Custom Configuration
Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
headless = true
runOnSave = true

[browser]
gatherUsageStats = false
serverAddress = "localhost"
```

## 📊 Usage Examples

### Basic Search
1. Enter query: "best wireless earbuds under $200"
2. Click "Get recommendation"
3. View results with ranking and reasons

### Product Comparison
1. Enter: "iPad Pro vs Surface Pro"
2. Select LLM provider in sidebar
3. Get detailed comparison

### Export Results
- Click "Download JSON" for raw data
- Click "Download Report" for formatted text

## 🔍 Troubleshooting

### Common Issues

1. **Module not found error**
   ```bash
   # Ensure you're in the right directory
   cd shopsage/tier1-streamlit
   # Reinstall dependencies
   uv sync
   ```

2. **API key errors**
   ```bash
   # Check .env file exists and has correct keys
   cat .env
   # Ensure no quotes around API keys in .env
   ```

3. **Port already in use**
   ```bash
   # Use different port
   uv run streamlit run streamlit_app.py --server.port 8502
   ```

4. **Import errors for shopsage_core**
   ```bash
   # Ensure parent directory has shopsage_core.py
   ls ../shopsage_core.py
   # Try running with uv
   uv run streamlit run streamlit_app.py
   ```

### Performance Optimization

1. **Enable caching**
   ```python
   @st.cache_data
   def search_products(query):
       return scout.search(query)
   ```

2. **Limit search results**
   ```python
   results = scout.search(query, max_results=5)
   ```

3. **Use session state**
   ```python
   if 'results' not in st.session_state:
       st.session_state.results = []
   ```

## 📈 Monitoring

### View Logs
```bash
# Streamlit logs
uv run streamlit run streamlit_app.py 2>&1 | tee app.log

# On Streamlit Cloud
# View logs in dashboard under "Manage app" → "Logs"
```

## 🔗 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cloud Guide](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit Components](https://streamlit.io/components)
- [Community Forum](https://discuss.streamlit.io)