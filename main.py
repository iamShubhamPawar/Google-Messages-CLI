from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, qrcode, datetime
from bs4 import BeautifulSoup

class Color:
    RED = '\033[91m'
    PURPLE = '\033[35m'
    ORANGE = '\033[33m'
    GRAY = '\033[90m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def initialize():
    """
    Initializes the web driver and opens the Google Messages web page.
    If the session is already restored, it prints "Session Restored!".
    Otherwise, it prompts the user to scan a QR code for login.
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-data-dir=/GsmsChromeData/")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    global driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://messages.google.com/web/authentication")
    time.sleep(3)
    if driver.current_url == "https://messages.google.com/web/conversations":
        print("Session Restored!")
    else:
        print("Please scan the QR code to login!")
        element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/mw-app/mw-bootstrap/div/main/mw-authentication-container/div/div/div/div[2]/div[2]/mw-qr-code")))
        qrdata = element.get_attribute("data-qr-code")
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qrdata)
        qr.print_ascii()
        input("Press Enter if you have scanned the QR code!")
        print("QR code scanned!")

def findContact(nums):
    """
    Finds a contact by entering the provided number in the contact search field.

    Args:
        nums (str): The number to search for.
    """
    search = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-main-nav/div/mw-fab-link/a/span[2]/div/div"))).click()
    data = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-new-conversation-container/mw-new-conversation-sub-header/div/div[2]/mw-contact-chips-input/div/div/input")))
    data.click()
    data.send_keys(nums)
    selectNum = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-new-conversation-container/div/mw-contact-selector-button/button/span[2]/span/span/span"))).click()

def sendMessage(msg):
    """
    This function sends a message in Google Messages.

    Args:
        msg (str): The message to be sent.
    """
    message = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-conversation-container/div/div[1]/div/mws-message-compose/div/div[2]/div/div/mws-autosize-textarea/textarea"))).send_keys(msg)
    submitButton = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/mw-app/mw-bootstrap/div/main/mw-main-container/div/mw-conversation-container/div/div[1]/div/mws-message-compose/div/mws-message-send-button/div/mw-message-send-button/button/span[4]"))).click()
    time.sleep(3)

def readMessage():
    """
    This function reads all messages in the current conversation.

    Returns:
    messages (list): A list of messages in the current conversation.
    """
    elements = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "msg-focus-element")))
    messages = [element.get_attribute("aria-label").replace(" said","") for element in elements]
    return messages

def print_message(message):
    """
    This function prints a message with its timestamp in a colorful format.

    Parameters:
    message (str): The message to print.
    """
    if ". Sent on" in message:
        msg = message.split(". Sent on ")
        timestamp = f"{Color.CYAN}[{datetime.datetime.strptime(msg[1], '%B %d, %Y at %I:%M %p. SMS.')}]{Color.RESET}"
        styled_message = (f"{timestamp} {Color.RED}→ {msg[0]}{Color.RESET}")
        print(styled_message)

    elif ". Received on" in message:
        msg = message.split(". Received on ")
        timestamp = f"{Color.CYAN}[{datetime.datetime.strptime(msg[1], '%B %d, %Y at %I:%M %p.')}]{Color.RESET}"
        styled_message = (f"{timestamp} {Color.GREEN}← {msg[0]}{Color.RESET}")
        print(styled_message)

def format_sms_messages(messages, max_message_length=100):
    """
    Formats SMS messages by truncating them to a maximum length and adding formatting.

    Args:
        messages (dict): A dictionary containing sender as keys and messages as values.
        max_message_length (int, optional): The maximum length of each message. Defaults to 100.

    Returns:
        list: A list of formatted messages.

    """
    formatted_messages = []
    for sender, message in messages.items():
        formatted_message = message[:max_message_length] + ('...' if len(message) > max_message_length else '')
        formatted = f"{Color.YELLOW}{sender.ljust(12)}{Color.RESET} {Color.GREEN}❯{Color.RESET} {Color.CYAN}{formatted_message}{Color.RESET}"
        formatted_messages.append(formatted)
    return formatted_messages

def getConvosList():
    """
    Retrieves a list of conversations and their corresponding messages from a web page.

    Returns:
        list: A list of formatted SMS messages.
    """
    convos = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "conv-container")))[0]
    ko = convos.get_attribute("innerHTML")
    soup = BeautifulSoup(ko, "html.parser")
    name_element = soup.findAll('span', {'data-e2e-conversation-name': True})
    message_element = soup.findAll('mws-conversation-snippet')
    data = {}
    for io in range(len(name_element)):
        data[name_element[io].text] = message_element[io].text
    formatted_dashboard = format_sms_messages(data)
    for message in formatted_dashboard:
        print(message)

def close():
    """
    Closes the driver and exits the program.
    """
    driver.quit()
    exit()
