import logging
from celery import shared_task
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from .models import ScrapeJob, CoinData
import json

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def scrape_coin_data(self, job_id, coin):
    logger.info(f"Starting scraping task for job_id: {job_id}, coin: {coin}")
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    url = f"https://coinmarketcap.com/currencies/{coin}/"
    driver.get(url)

    try:
        price = driver.find_element(By.CLASS_NAME, "priceValue").text
        price_change = driver.find_element(By.CLASS_NAME, "sc-15yy2pl-0").text
        market_cap = driver.find_element(By.XPATH, "//*[text()='Market Cap']/following-sibling::div").text
        volume = driver.find_element(By.XPATH, "//*[text()='Volume 24h']/following-sibling::div").text
        circulating_supply = driver.find_element(By.XPATH, "//*[text()='Circulating Supply']/following-sibling::div").text
        total_supply = driver.find_element(By.XPATH, "//*[text()='Total Supply']/following-sibling::div").text

        data = {
            "price": price,
            "price_change": price_change,
            "market_cap": market_cap,
            "volume": volume,
            "circulating_supply": circulating_supply,
            "total_supply": total_supply,
        }
    except Exception as e:
        logger.error(f"Error scraping data for coin {coin}: {e}")
        data = {"error": str(e)}

    driver.quit()

    try:
        job = ScrapeJob.objects.get(job_id=job_id)
        logger.info(f"Found job: {job}")
        CoinData.objects.create(job=job, coin=coin, data=json.dumps(data))
        logger.info(f"Data saved for job_id: {job_id}, coin: {coin}")
    except Exception as e:
        logger.error(f"Error saving data for coin {coin}: {e}")
