# OpsClarity — SME Ops Intelligence

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy free on Streamlit Cloud
1. Push this repo to GitHub
2. Go to share.streamlit.io
3. Connect your repo → Deploy

## Add Razorpay payments
Replace the paywall button with:
```python
import razorpay
client = razorpay.Client(auth=("YOUR_KEY", "YOUR_SECRET"))
order = client.order.create({"amount": 299900, "currency": "INR"})
```

## Apollo.io outreach template
Target: "Founder OR Owner OR Director" + "restaurant OR retail OR clinic" + "Bengaluru"
Subject: "Your Tally data can show you exactly where you're losing money"
