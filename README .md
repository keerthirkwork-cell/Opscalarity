# ◈ OpsClarity — Business Health for Indian SMEs

Find where your business is leaking money — in 30 seconds.

## 🚀 Quick Deploy

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo → `app.py`
4. Add secrets (optional, for AI advisor):
   - Settings → Secrets → paste: `ANTHROPIC_API_KEY = "sk-ant-..."`
5. Deploy ✅

## 📁 Files

```
app.py              ← Main app (everything in one file)
requirements.txt    ← Dependencies (fixes the openpyxl error)
.streamlit/
  secrets.toml.example  ← API key template
```

## 🔧 requirements.txt

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0       ← Fixes the Excel upload error
xlrd>=2.0.1
plotly>=5.18.0
anthropic>=0.25.0     ← For AI advisor tab
python-dotenv>=1.0.0
```

## ✨ What's New in v2

- ✅ **Fixed**: openpyxl error — Excel uploads now work
- 🏛️ **CA Portal**: Monitor all client health scores in one dashboard
- 🤖 **AI Advisor**: Ask plain-language questions about your data
- 💰 **3-tier pricing**: Free / Pro ₹499 / CA Plan ₹1,999
- 📊 **Better charts**: MoM trends with delta metrics
- 🎨 **Upgraded UI**: Playfair Display, cleaner layout

## 💡 AI Advisor Setup

The "Ask OpsClarity" tab calls Anthropic's API. To enable:

1. Get an API key at [console.anthropic.com](https://console.anthropic.com)
2. In Streamlit Cloud: **App settings → Secrets**
3. Add: `ANTHROPIC_API_KEY = "sk-ant-your-key-here"`

Without the key, the tab shows a graceful fallback message.

## 📞 Contact

WhatsApp: +91 63623 19163
Built in Bangalore 🇮🇳
