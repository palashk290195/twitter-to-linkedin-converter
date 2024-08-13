# Twitter Thread to LinkedIn Carousel Converter

This Python script converts Twitter threads into LinkedIn carousel-style PDFs. It's perfect for repurposing your Twitter content for LinkedIn, creating visually appealing slides from your tweets.

## Features

- Scrapes tweets from a specified Twitter thread
- Converts tweets into a multi-page PDF suitable for LinkedIn carousels
- Customizable user name display on each slide
- Consistent formatting with large, readable text
- Dark background for enhanced visibility

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system
- Chrome browser installed (required for Selenium WebDriver)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/palashk290195/twitter-to-linkedin-converter.git
   cd twitter-to-linkedin-converter
   ```

2. Install the required Python packages:
   ```
   pip install selenium reportlab webdriver-manager
   ```

## Usage

1. Run the script:
   ```
   python twitter_to_linkedin_converter.py
   ```

2. When prompted, enter the following information:
   - The URL of the Twitter thread you want to convert
   - The user name to display on the slides
   - The name for the output PDF file

3. The script will open a Chrome browser window. Log in to Twitter manually when prompted.

4. After logging in, press Enter in the console to continue the script.

5. The script will process the thread and generate a PDF in the same directory as the script.

## Example

```
Welcome to the Twitter Thread to LinkedIn Carousel Converter!
Please enter the URL of the Twitter thread: https://twitter.com/username/status/tweetid
Please enter the name for the output PDF file (e.g., carousel.pdf): my_carousel.pdf
```

## Customization

You can customize the appearance of the PDF by modifying the following parameters in the `create_pdf_carousel` function:

- Font sizes
- Colors
- Padding and margins

## Contributing

Contributions to this project are welcome. Please feel free to submit a Pull Request.

## Disclaimer

This tool is for personal use only. Please respect Twitter's and LinkedIn's terms of service when using this script. Ensure you have the right to repurpose the content you're converting.

## Support

If you encounter any problems or have any questions, please open an issue in this repository.
