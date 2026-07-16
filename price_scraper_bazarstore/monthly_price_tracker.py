"""
BazarStore Monthly Price Tracker
Reads URLs from text file and adds new price columns to CSV each month
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time
from typing import List, Dict, Optional


class MonthlyPriceTracker:
    """Track prices monthly by adding new columns to CSV"""
    
    def __init__(self, delay: int = 5):
        self.delay = delay
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Price selectors
        self.name_selectors = [
            ("h1.product__title", None),
            ("h1", {"class": "product__title"}),
            ("h1.product-title", None),
            ("h1", None),
        ]
        
        self.price_selectors = [
            ("span.price-item--regular", None),
            ("span", {"class": "price-item"}),
            ("div.price span", None),
            ("span.price", None),
        ]
    
    def load_urls(self, filename: str) -> List[str]:
        """Load URLs from text file"""
        print(f"📂 Loading URLs from {filename}...\n")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
            
            print(f"✅ Loaded {len(urls)} URLs\n")
            return urls
            
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
            return []
        except Exception as e:
            print(f"❌ Error loading URLs: {e}")
            return []
    
    def scrape_product(self, url: str) -> Optional[Dict[str, any]]:
        """Scrape product name and price"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find product name
            product_name = None
            for selector, attrs in self.name_selectors:
                try:
                    if attrs:
                        tag = soup.find(selector.split()[0], attrs)
                    else:
                        tag = soup.select_one(selector)
                    
                    if tag:
                        product_name = tag.text.strip()
                        break
                except:
                    continue
            
            if not product_name:
                return None
            
            # Find price
            price = None
            for selector, attrs in self.price_selectors:
                try:
                    if attrs:
                        tag = soup.find(selector.split()[0], attrs)
                    else:
                        tag = soup.select_one(selector)
                    
                    if tag:
                        price_text = tag.text.replace("₼", "").replace(",", "").replace("AZN", "").strip()
                        try:
                            price = float(price_text)
                            break
                        except ValueError:
                            continue
                except:
                    continue
            
            if price is None:
                return None
            
            return {
                'name': product_name,
                'price': price,
                'url': url
            }
            
        except Exception as e:
            print(f"⚠️  Error scraping {url}: {e}")
            return None
    
    def load_existing_csv(self, filename: str) -> Dict[str, Dict]:
        """Load existing CSV data"""
        products = {}
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    url = row.get('url', '')
                    if url:
                        products[url] = row
        except FileNotFoundError:
            pass
        
        return products
    
    def update_prices(self, urls: List[str], csv_filename: str):
        """Update CSV with new price column"""
        today = datetime.today().strftime("%Y-%m-%d")
        price_column = f"price_{today}"
        
        print(f"📊 Scraping prices for {today}...\n")
        
        # Load existing data
        existing_products = self.load_existing_csv(csv_filename)
        
        # Scrape new prices
        new_data = []
        success = 0
        failed = 0
        
        for i, url in enumerate(urls, 1):
            print(f"   [{i}/{len(urls)}] ", end="")
            
            product = self.scrape_product(url)
            
            if product:
                success += 1
                print(f"✓ {product['name'][:40]}... | {product['price']} ₼")
                
                # Get existing data or create new
                if url in existing_products:
                    existing_data = existing_products[url]
                else:
                    existing_data = {
                        'product_name': product['name'],
                        'url': url
                    }
                
                # Add new price
                existing_data[price_column] = product['price']
                new_data.append(existing_data)
            else:
                failed += 1
                print(f"✗ Failed")
                
                # Keep existing data even if scraping failed
                if url in existing_products:
                    existing_data = existing_products[url]
                    existing_data[price_column] = ''  # Empty for failed scrape
                    new_data.append(existing_data)
            
            if i < len(urls):
                time.sleep(self.delay)
        
        # Save updated CSV
        if new_data:
            self.save_csv(new_data, csv_filename, price_column)
        
        return success, failed
    
    def save_csv(self, products: List[Dict], filename: str, new_column: str):
        """Save updated CSV with new price column"""
        print(f"\n💾 Saving to {filename}...\n")
        
        # Get all unique columns
        all_columns = set()
        for product in products:
            all_columns.update(product.keys())
        
        # Sort columns: product_name, all price columns sorted by date, url
        price_columns = sorted([col for col in all_columns if col.startswith('price_')])
        fieldnames = ['product_name'] + price_columns + ['url']
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(products)
            
            print(f"✅ Successfully saved {len(products)} products")
            print(f"✅ Added new column: {new_column}")
            
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
    
    def run(self, urls_file: str = "product_urls.txt", csv_file: str = "price_history.csv"):
        """Main workflow"""
        print("=" * 70)
        print("📈 BazarStore Monthly Price Tracker")
        print("=" * 70)
        print(f"Settings:")
        print(f"  • URLs file: {urls_file}")
        print(f"  • CSV file: {csv_file}")
        print(f"  • Delay: {self.delay}s")
        print(f"  • Date: {datetime.today().strftime('%Y-%m-%d')}")
        print("=" * 70 + "\n")
        
        # Step 1: Load URLs
        urls = self.load_urls(urls_file)
        
        if not urls:
            print("❌ No URLs to process. Exiting.")
            return
        
        # Step 2: Update prices
        success, failed = self.update_prices(urls, csv_file)
        
        # Step 3: Summary
        print("\n" + "=" * 70)
        print("📊 Summary:")
        print(f"  • Total URLs: {len(urls)}")
        print(f"  • Successfully scraped: {success}")
        print(f"  • Failed: {failed}")
        print(f"  • Success rate: {(success/len(urls)*100):.1f}%")
        print("=" * 70)
        print("\n💡 Run this script again next month to add another price column!")


def main():
    """Entry point"""
    tracker = MonthlyPriceTracker(delay=3)
    
    tracker.run(
        urls_file="product_urls.txt",
        csv_file="price_history.csv"
    )


if __name__ == "__main__":
    main()
