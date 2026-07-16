# BazarStore Price Tracking System

Track product prices over time with monthly updates.

---

## 📈 Latest Results (Jan–Jul 2026)

Tracked 50 grocery items across 4 snapshots (Jan 10, Feb 10, Mar 10, Jul 10, 2026):

- **Basket index rose +8.2%** on average across 48 items with complete price history
- **Biggest increase:** Local red apples — **+152%** (0.79 → 1.99 AZN)
- **Biggest drop:** Muço tomatoes — **-54%** (spiked to 6.99 AZN in spring, then crashed)
- **10 of 50 products** had zero price change (e.g. Coca-Cola, Kinder Country)
- Fresh produce was the most volatile category; packaged/branded goods stayed stable

📊 [Interactive dashboard for analyzing prices.](price_scraper_bazarstore/bazar_price_dashboard.html)

---

## 📁 Files

1. **[collect_urls.py](price_scraper_bazarstore/collect_urls.py)** - Run ONCE to collect product URLs
2. **[monthly_price_tracker.py](price_scraper_bazarstore/monthly_price_tracker.py)** - Run MONTHLY to update prices
3. **[product_urls.txt](price_scraper_bazarstore/product_urls.txt)** - Stores product URLs (created by collect_urls.py)
4. **[price_history.csv](price_scraper_bazarstore/price_history.csv)** - Your price tracking data (created/updated by monthly_price_tracker.py)
---

## 🛠️ Tools & Technologies Used

* **Python 3.8+** - Programming language
* **Requests** - HTTP library for web requests
* **BeautifulSoup4** - HTML parsing and web scraping
* **Pandas** - Data processing and CSV handling
* **Chart.js** - Interactive dashboard charts
* **Git/GitHub** - Version control and repository hosting

### 📋 Requirements & Dependencies

To run the scripts, make sure you have the following Python packages installed:

```text
requests == 2.31.0
beautifulsoup4 == 4.12.2
pandas == 2.1.1
```
---

## 🚀 How to Use

### **Step 1: Collect URLs (Run Once - January 2026)**

```bash
python collect_urls.py
```

**What it does:**
- Scrapes BazarStore bestsellers page
- Collects up to 50 product URLs
- Saves them to `product_urls.txt`

**Output:**
```
product_urls.txt
├── https://bazarstore.az/products/banan-kq
├── https://bazarstore.az/products/alma
├── https://bazarstore.az/products/armud
└── ...
```

---

### **Step 2: Track Prices (Run Monthly)**

**First run (January 2026):**
```bash
python monthly_price_tracker.py
```

**Creates CSV:**
```csv
product_name,price_2026-01-10,url
BANAN KQ,3.19,https://bazarstore.az/products/banan-kq
ALMA,2.50,https://bazarstore.az/products/alma
ARMUD,4.20,https://bazarstore.az/products/armud
```

---

**Second run (February 2026):**
```bash
python monthly_price_tracker.py
```

**Updates CSV (adds new column):**
```csv
product_name,price_2026-01-10,price_2026-02-10,url
BANAN KQ,3.19,3.49,https://bazarstore.az/products/banan-kq
ALMA,2.50,2.30,https://bazarstore.az/products/alma
ARMUD,4.20,4.50,https://bazarstore.az/products/armud
```

---

**Third run (March 2026):**
```bash
python monthly_price_tracker.py
```

**Updates CSV (adds another column):**
```csv
product_name,price_2026-01-10,price_2026-02-10,price_2026-03-10,url
BANAN KQ,3.19,3.49,3.29,https://bazarstore.az/products/banan-kq
ALMA,2.50,2.30,2.45,https://bazarstore.az/products/alma
ARMUD,4.20,4.50,4.35,https://bazarstore.az/products/armud
```

---

**Fourth run (July 2026):**
```bash
python monthly_price_tracker.py
```

**Updates CSV (adds another column):**
```csv
product_name,price_2026-01-10,price_2026-02-10,price_2026-03-10,url
BANAN KQ,3.19,3.49,3.29,https://bazarstore.az/products/banan-kq
ALMA,2.50,2.30,2.45,https://bazarstore.az/products/alma
ARMUD,4.20,4.50,4.35,https://bazarstore.az/products/armud
```
---


## 📅 Monthly Schedule

Set a reminder to run this **every month**:

```bash
python monthly_price_tracker.py
```

**Recommended:** 1st or 15th of each month

---

## 🔧 Configuration

### Change number of products to track:

Edit `collect_urls.py`:
```python
collector = URLCollector(
    max_products=100,  # Change from 50 to 100
    delay=3
)
```

### Change delay between requests:

Edit `monthly_price_tracker.py`:
```python
tracker = MonthlyPriceTracker(delay=5)  # Change from 3 to 5 seconds
```

### Change file names:

```python
tracker.run(
    urls_file="my_products.txt",      # Default: product_urls.txt
    csv_file="my_price_history.csv"   # Default: price_history.csv
)
```

---

## 📊 Analyzing Price History

After collecting several months of data, you can:

### View in Excel/Google Sheets
- Open `price_history.csv`
- Create charts to visualize price trends
- Use formulas to calculate average prices

### Example: Find price changes
```python
import pandas as pd

df = pd.read_csv('price_history.csv')

# Calculate price change from Jan to Feb
df['change'] = df['price_2026-02-10'] - df['price_2026-01-10']
df['change_percent'] = (df['change'] / df['price_2026-01-10']) * 100

print(df[['product_name', 'change', 'change_percent']])
```

---

## ⚠️ Troubleshooting

### Problem: "No URLs found"
**Solution:** Website structure may have changed. Run `bazarstore_inspector.py` to check.

### Problem: "Failed to scrape prices"
**Solution:** 
- Check internet connection
- Verify URLs in `product_urls.txt` are still valid
- Website might be blocking requests (reduce delay to 5+ seconds)

### Problem: "Product URLs changed"
**Solution:** 
- Some products may be discontinued
- Re-run `collect_urls.py` to get fresh URLs
- Compare old and new `product_urls.txt` to see what changed

---

## 💾 Backup Your Data

**Important files to backup:**
- `product_urls.txt` - Your tracked product list
- `price_history.csv` - Your price data

**Recommendation:** Keep monthly backups:
```bash
# Windows
copy price_history.csv price_history_backup_2026-01.csv

# Mac/Linux
cp price_history.csv price_history_backup_2026-01.csv
```

---

## 📈 Example Timeline

| Date | Action | Result |
|------|--------|--------|
| Jan 10, 2026 | Run `collect_urls.py` | Created `product_urls.txt` (50 URLs) |
| Jan 10, 2026 | Run `monthly_price_tracker.py` | Created `price_history.csv` with `price_2026-01-10` column |
| Feb 10, 2026 | Run `monthly_price_tracker.py` | Added `price_2026-02-10` column |
| Mar 10, 2026 | Run `monthly_price_tracker.py` | Added `price_2026-03-10` column |
| Apr 10, 2026 | Run `monthly_price_tracker.py` | Added `price_2026-04-10` column |

After 6 months, you'll have complete price history!

---

## 🎯 Best Practices

1. ✅ Run on the **same day each month** for consistent tracking
2. ✅ Keep `product_urls.txt` unchanged (don't edit manually)
3. ✅ Backup `price_history.csv` before each run
4. ✅ Respect the website with appropriate delays (3+ seconds)
5. ✅ Check for failed scrapes and investigate why

---

**Happy price tracking! 📊**
