import os
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv

load_dotenv()

class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self.app = FirecrawlApp(api_key=api_key)

    def search_drug_info(self, query: str, num_results: int = 5):
        """Search for drug information from medical databases and resources"""
        try:
            result = self.app.search(
                query=f"{query} drug information interactions dosage",
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            return result
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def search_drug_interactions(self, drug_name: str, num_results: int = 3):
        """Search specifically for drug interaction information"""
        try:
            result = self.app.search(
                query=f"{drug_name} drug interactions contraindications safety",
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            return result
        except Exception as e:
            print(f"Interaction search error: {e}")
            return []

    def scrape_medical_page(self, url: str):
        """Scrape medical information pages"""
        try:
            result = self.app.scrape_url(
                url,
                formats=["markdown"]
            )
            return result
        except Exception as e:
            print(f"Scraping error: {e}")
            return None
