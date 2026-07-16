"""
BazarStore URL Collector
Collects product URLs and saves them to a text file for future price tracking
"""

import requests
from bs4 import BeautifulSoup
import time
from typing import List


class URLCollector:
    """Collect and save product URLs for future tracking"""
    
    def __init__(self, max_products: int = 50, delay: int = 3):
        self.base_url = "https://bazarstore.az/collections/bazarstore-bestsellers?filter.v.price.gte=&filter.v.price.lte=&filter.v.availability=1&filter.p.m.custom.lokasyonlar=4102"
        self.max_products = max_products
        self.delay = delay
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Multiple possible selectors to try
        self.product_selectors = [
            "a.product-card__image-link",
            "div.product-card a[href*='/products/']",
            "a[href*='/products/']",
            "div.product-item a",
            "div.grid__item a[href*='/products/']",
        ]
    
    def find_working_selector(self) -> bool:
        """Test selectors to find one that works"""
        print("🔍 Testing selectors...\n")
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Try each selector
                for selector in self.product_selectors:
                    try:
                        products = soup.select(selector)
                        if products:
                            print(f"✅ Found {len(products)} products")
                            print(f"   Using selector: {selector}\n")
                            self.working_selector = selector
                            return True
                    except:
                        continue
                
                print(f"⚠️  No products found with any selector")
                return False
        except Exception as e:
            print(f"❌ Error accessing URL: {e}")
            return False
    
    def collect_urls(self) -> List[str]:
        """Collect product URLs from all pages"""
        print("🔍 Collecting product URLs...\n")
        all_urls = []
        seen_products = set()
        page = 1
        
        while len(all_urls) < self.max_products:
            url = f"{self.base_url}&page={page}"
            
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Find products
                products = soup.select(self.working_selector)
                
                if not products:
                    print(f"ℹ️  No more products on page {page}")
                    break
                
                # Extract URLs
                for element in products:
                    if len(all_urls) >= self.max_products:
                        break
                    
                    # Get href
                    href = element.get('href')
                    if not href and element.find('a'):
                        href = element.find('a').get('href')
                    
                    if href and '/products/' in href:
                        if not href.startswith('http'):
                            href = "https://bazarstore.az" + href
                        
                        # Clean URL - remove query parameters
                        clean_url = href.split('?')[0]
                        
                        # Only add unique products
                        if clean_url not in seen_products:
                            seen_products.add(clean_url)
                            all_urls.append(clean_url)
                
                print(f"   Page {page}: Found {len(products)} products (Total: {len(all_urls)})")
                page += 1
                time.sleep(self.delay)
                
            except Exception as e:
                print(f"⚠️  Error on page {page}: {e}")
                break
        
        print(f"\n✅ Collected {len(all_urls)} unique product URLs\n")
        return all_urls
    
    def save_urls(self, urls: List[str], filename: str):
        """Save URLs to text file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for url in urls:
                    f.write(url + '\n')
            
            print(f"✅ Saved {len(urls)} URLs to {filename}")
            
        except Exception as e:
            print(f"❌ Error saving URLs: {e}")
    
    def run(self, filename: str = "product_urls.txt"):
        """Main workflow"""
        print("=" * 70)
        print("🛒 BazarStore URL Collector")
        print("=" * 70)
        print(f"Settings:")
        print(f"  • Max products: {self.max_products}")
        print(f"  • Delay: {self.delay}s")
        print(f"  • Output: {filename}")
        print("=" * 70 + "\n")
        
        # Step 1: Find working selector
        if not self.find_working_selector():
            print("❌ Could not find products. Exiting.")
            return
        
        # Step 2: Collect URLs
        urls = self.collect_urls()
        
        if not urls:
            print("❌ No URLs collected. Exiting.")
            return
        
        # Step 3: Save to file
        self.save_urls(urls, filename)
        
        print("\n" + "=" * 70)
        print("✅ URL collection complete!")
        print(f"📝 Next steps:")
        print(f"   1. Keep '{filename}' safe - you'll need it next month")
        print(f"   2. Run the price tracker script monthly to update prices")
        print("=" * 70)


def main():
    """Entry point"""
    collector = URLCollector(
        max_products=50,
        delay=3
    )
    
    collector.run(filename="product_urls.txt")


if __name__ == "__main__":
    main()
