import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import Color

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scroll_to_bottom(driver):
    """Scroll to the bottom of the page to load all tweets."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def capture_tweet_contents(url, max_tweets=10):
    """
    Capture tweet contents from a thread using Selenium, with manual login.
    """
    logger.info(f"Starting to capture tweet contents from URL: {url}")
    options = Options()
    options.add_argument("start-maximized")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        logger.info("WebDriver initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {str(e)}")
        raise

    try:
        driver.get("https://twitter.com/login")
        logger.info("Navigated to Twitter login page")
        
        input("Please log in to Twitter manually, then press Enter to continue...")
        logger.info("User indicated login is complete")

        driver.get(url)
        logger.info("Navigated to the thread URL")
        time.sleep(5)  # Wait for initial load

        scroll_to_bottom(driver)
        logger.info("Scrolled to bottom of page")

        tweets = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')
        logger.info(f"Found {len(tweets)} tweet elements")

        tweet_contents = []
        for i, tweet in enumerate(tweets[:max_tweets], 1):
            logger.info(f"Capturing content of tweet {i}")
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="User-Name"]'))
                )
                user_name = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Name"]').text.split('\n')[0]
                tweet_text = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]').text
                tweet_contents.append((user_name, tweet_text))
            except Exception as e:
                logger.error(f"Failed to capture content for tweet {i}: {str(e)}")

        logger.info(f"Captured content of {len(tweet_contents)} tweets successfully")
        return tweet_contents
    except Exception as e:
        logger.error(f"Error during tweet content capture: {str(e)}")
        raise
    finally:
        driver.quit()
        logger.info("WebDriver closed")

def create_pdf_carousel(tweet_contents, output_file):
    """
    Create a PDF carousel from the captured tweet contents, formatting each tweet as requested.
    """
    logger.info(f"Creating PDF carousel with {len(tweet_contents)} tweets")
    try:
        c = canvas.Canvas(output_file, pagesize=landscape(letter))
        width, height = landscape(letter)
        
        for i, (user_name, tweet_text) in enumerate(tweet_contents, 1):
            logger.info(f"Adding tweet {i} to PDF")
            
            # Set background color
            c.setFillColor(Color(0.2, 0.2, 0.2))  # Dark grey
            c.rect(0, 0, width, height, fill=1)
            
            # Add user info at the top
            c.setFillColor(Color(1, 1, 1))  # White color for text
            c.setFont("Helvetica-Bold", 40)
            c.drawString(50, height - 80, user_name)
            
            # Add tweet text
            style = ParagraphStyle(
                'Tweet',
                fontName='Helvetica',
                fontSize=40,
                leading=48,
                textColor=Color(1, 1, 1)
            )
            p = Paragraph(tweet_text, style)
            frame = Frame(50, 50, width - 100, height - 150, showBoundary=0)
            frame.addFromList([p], c)
            
            c.showPage()
        
        c.save()
        logger.info(f"PDF carousel saved as {output_file}")
    except Exception as e:
        logger.error(f"Error creating PDF: {str(e)}")
        raise

def twitter_thread_to_linkedin_carousel(thread_url, output_file):
    """
    Convert a Twitter thread to a LinkedIn carousel PDF.
    """
    logger.info("Starting Twitter thread to LinkedIn carousel conversion")
    tweet_contents = capture_tweet_contents(thread_url)
    create_pdf_carousel(tweet_contents, output_file)
    logger.info(f"Created LinkedIn carousel PDF with {len(tweet_contents)} slides")

def main():
    print("Welcome to the Twitter Thread to LinkedIn Carousel Converter!")
    thread_url = input("Please enter the URL of the Twitter thread: ")
    output_file = input("Please enter the name for the output PDF file (e.g., carousel.pdf): ")
    
    try:
        twitter_thread_to_linkedin_carousel(thread_url, output_file)
        print(f"Conversion complete! Check {output_file} for your LinkedIn carousel PDF.")
    except Exception as e:
        logger.exception("An error occurred during conversion")
        print(f"An error occurred: {str(e)}")
        print("Please check the log for more details.")

if __name__ == "__main__":
    main()
