"""
Legacy data scraper module - Use scrapers from utils.scrapers instead
This file is kept for backward compatibility
"""
from app.utils.scrapers import CasablancaBourseScraper, ASFIMScraper, AMMCScraper

# Re-export for backward compatibility
__all__ = ['CasablancaBourseScraper', 'ASFIMScraper', 'AMMCScraper']

