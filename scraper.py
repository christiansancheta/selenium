from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Start the webdriver server
driver = webdriver.Remote(
   command_executor='http://localhost:4444/wd/hub',
   desired_capabilities=DesiredCapabilities.FIREFOX
)

# Use the webdriver as you would with a local webdriver
driver.get("https://finance.yahoo.com/most-active?offset=0&count=50")
# time.sleep(5)

ticker_element = driver.find_element(By.XPATH, '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[1]/td[1]/a')

ticker_text = ticker_element.text
tickers = ticker_text.split('\n')

# Save the stock prices to a file in the current working directory
with open('stock_prices.csv', 'a', newline='') as csvfile:
  fieldnames = ['time', 'ticker', 'price', 'percent']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()

  for ticker in tickers:
    driver.get(f"https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch")
    # time.sleep(5)
    price_element = driver.find_element(By.CSS_SELECTOR,'fin-streamer.Fw\(b\):nth-child(1)')
    price = price_element.text
    percent_element = driver.find_element(By.CSS_SELECTOR, 'fin-streamer.Fw\(500\):nth-child(2) > span:nth-child(1)')
    percent = percent_element.text

    now = datetime.now()
    time = now.strftime("%m/%d/%Y %H:%M:%S")

    writer.writerow({'time': time, 'ticker': ticker, 'price': price, 'percent': percent})

# Close the webdriver
driver.close()
