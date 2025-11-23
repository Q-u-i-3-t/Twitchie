"""
UwU~! This script checks StreamElements commands for streamers desu! >w<
Kyaa~! Looks for commands with "$(touser)" in the response and "Everyone" permissions nya~! ✨
So exciting to find all the matching commands desu~!
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
import re

def setup_driver():
    """UwU~! Sets up and returns a Chrome WebDriver instance desu! >w<"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Kyaa~! Runs in background so no one sees it nya~! ✨
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        print("Make sure ChromeDriver is installed and in your PATH.")
        print("You can download it from: https://chromedriver.chromium.org/")
        return None

def check_streamelements_commands(driver, username):
    """
    UwU~! Checks a streamer's StreamElements commands page for commands with "$(touser)" and "Everyone" permissions desu! >w<
    So many commands to check nya~! ✨
    
    Args:
        driver: Selenium WebDriver instance (the browser thingy desu~!)
        username: Streamer's username (so cute desu! >w<)
        
    Returns:
        list: List of tuples (command_name, response) for matching commands, or None if no matches found (so sad nya~!)
    """
    url = f"https://streamelements.com/{username}/commands"
    
    try:
        driver.get(url)
        
        # Kyaa~! Wait for page to load nya~! ✨
        time.sleep(3)
        
        # UwU~! Check if page exists (404 or similar) desu! >w<
        if "404" in driver.title.lower() or "not found" in driver.page_source.lower():
            return None
        
        # Kyaa~! Wait for commands table or content to load nya~! ✨
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            return None
        
        matching_commands = []
        
        # Method 1: UwU~! Look for table rows with command data desu! >w<
        try:
            # Kyaa~! Try to find command rows in a table structure nya~! ✨
            command_rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr, tr[class*='row'], [class*='command-row']")
            
            for row in command_rows:
                try:
                    row_text = row.text
                    row_html = row.get_attribute("innerHTML") + row.get_attribute("outerHTML")
                    row_text_lower = row_text.lower()
                    
                    # UwU~! Check if this row contains "$(touser)" and "Everyone" desu! >w<
                    if "$(touser)" in row_html or "$(touser)" in row_text:
                        if "everyone" in row_text_lower or "everyone" in row_html.lower():
                            # Kyaa~! Try to extract command name and response nya~! ✨
                            command_name = ""
                            response = ""
                            
                            # UwU~! Try to find command name (usually first column) desu! >w<
                            try:
                                cells = row.find_elements(By.TAG_NAME, "td")
                                if len(cells) >= 1:
                                    command_name = cells[0].text.strip()
                                if len(cells) >= 2:
                                    response = cells[2].text.strip() if len(cells) > 2 else cells[1].text.strip()
                            except:
                                pass
                            
                            # Kyaa~! If we couldn't get from cells, try parsing row text nya~! ✨
                            if not command_name or not response:
                                parts = row_text.split("\n")
                                if len(parts) >= 1:
                                    command_name = parts[0].strip()
                                if len(parts) >= 2:
                                    # Find the part with $(touser) as the response
                                    for part in parts[1:]:
                                        if "$(touser)" in part:
                                            response = part.strip()
                                            break
                            
                            if command_name and response:
                                matching_commands.append((command_name, response))
                except:
                    continue
        except:
            pass
        
        # Method 2: UwU~! Look for command elements in various structures desu! >w<
        if not matching_commands:
            try:
                # Kyaa~! Try to find all elements that might contain command data nya~! ✨
                all_elements = driver.find_elements(By.CSS_SELECTOR, 
                    "[class*='Command'], [class*='command-card'], [data-testid*='command'], "
                    "[class*='table-row'], tbody tr, [role='row'], div[class*='row']")
                
                for elem in all_elements:
                    try:
                        elem_html = elem.get_attribute("outerHTML")
                        elem_text = elem.text
                        elem_html_lower = elem_html.lower()
                        elem_text_lower = elem_text.lower()
                        
                        if "$(touser)" in elem_html or "$(touser)" in elem_text:
                            if "everyone" in elem_text_lower or "everyone" in elem_html_lower:
                                # UwU~! Try to extract command name and response desu! >w<
                                command_name = ""
                                response = ""
                                
                                # Kyaa~! Look for command name (often starts with !) nya~! ✨
                                parts = elem_text.split("\n")
                                for part in parts:
                                    part = part.strip()
                                    if part.startswith("!") and not command_name:
                                        command_name = part.split()[0] if part.split() else part
                                    if "$(touser)" in part and not response:
                                        response = part
                                
                                # UwU~! If we found both, add it desu! >w<
                                if command_name and response:
                                    matching_commands.append((command_name, response))
                                    break  # Kyaa~! Just get the first matching command nya~! ✨
                    except:
                        continue
            except:
                pass
        
        # Method 3: UwU~! Search page source and try to extract from text desu! >w<
        if not matching_commands:
            try:
                page_text = driver.find_element(By.TAG_NAME, "body").text
                page_html = driver.page_source
                
                if "$(touser)" in page_html and "everyone" in page_html.lower():
                    # Kyaa~! Try to find command patterns in the text nya~! ✨
                    # UwU~! Look for lines that might be commands desu! >w<
                    lines = page_text.split("\n")
                    for i, line in enumerate(lines):
                        if "$(touser)" in line and "everyone" in line.lower():
                            # Kyaa~! Look backwards for command name (usually starts with !) nya~! ✨
                            command_name = ""
                            response = line.strip()
                            
                            # UwU~! Check previous lines for command name desu! >w<
                            for j in range(max(0, i-3), i):
                                prev_line = lines[j].strip()
                                if prev_line.startswith("!") and len(prev_line.split()) == 1:
                                    command_name = prev_line
                                    break
                            
                            if command_name and response:
                                matching_commands.append((command_name, response))
                                break
            except:
                pass
        
        # Kyaa~! Remove duplicates nya~! We don't want the same command twice desu! ✨
        seen = set()
        unique_commands = []
        for cmd_name, cmd_response in matching_commands:
            if (cmd_name, cmd_response) not in seen:
                seen.add((cmd_name, cmd_response))
                unique_commands.append((cmd_name, cmd_response))
        
        return unique_commands if unique_commands else None
        
    except Exception as e:
        print(f"    Error checking {username}: {e}")
        return None

def scan_streamelements_commands(input_file='twitch_streamers.txt', output_file='streamelements_streamers.txt'):
    """
    UwU~! Scans StreamElements commands for all streamers in the input file desu! >w<
    Kyaa~! Outputs streamer usernames with their matching command names and responses nya~! ✨
    So exciting to find all the commands desu~!
    
    Args:
        input_file (str): Path to file containing streamer usernames (one per line - so many streamers desu! >w<)
        output_file (str): Path to output file for results (where we save everything nya~!)
    """
    # Kyaa~! Read streamer usernames nya~! ✨
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        print("Please run scan_twitch_streamers.py first to generate the streamer list.")
        return
    
    with open(input_file, 'r', encoding='utf-8') as f:
        usernames = [line.strip() for line in f if line.strip()]
    
    if not usernames:
        print(f"No usernames found in {input_file}")
        return
    
    print(f"Found {len(usernames)} streamers to check")
    print("Starting StreamElements command scan...")
    print("Looking for streamers with commands containing '$(touser)' and 'Everyone' permissions\n")
    
    driver = setup_driver()
    if not driver:
        return
    
    results = []  # UwU~! List of (username, command_name, response) tuples desu! >w<
    checked = 0
    
    try:
        for username in usernames:
            checked += 1
            print(f"[{checked}/{len(usernames)}] Checking {username}...", end=" ")
            
            matching_commands = check_streamelements_commands(driver, username)
            
            if matching_commands:
                # Kyaa~! Add the first matching command (or all if multiple) nya~! ✨
                for cmd_name, cmd_response in matching_commands:
                    results.append((username, cmd_name, cmd_response))
                print(f"✓ Found {len(matching_commands)} matching command(s)")
            else:
                print("✗")
            
            # UwU~! Small delay to avoid overwhelming the server desu! >w<
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user.")
        print(f"Saving {len(results)} results found so far...")
    except Exception as e:
        print(f"\nError during scan: {e}")
    finally:
        driver.quit()
    
    # Kyaa~! Write results to file nya~! ✨
    print(f"\n\nScan complete!")
    print(f"Checked: {checked} streamers")
    print(f"Found matching commands: {len(results)}")
    
    if results:
        with open(output_file, 'w', encoding='utf-8') as f:
            # UwU~! Group by username to handle multiple commands per streamer desu! >w<
            current_username = None
            
            for username, cmd_name, cmd_response in sorted(results):
                if current_username != username:
                    # Kyaa~! If this is a new streamer (not the first), add separator after previous streamer nya~! ✨
                    if current_username is not None:
                        f.write('\n---------------------\n\n')
                    
                    f.write(f"{username}\n")
                    current_username = username
                
                f.write(f"{cmd_name} {cmd_response}\n")
            
            # UwU~! Add final separator after the last streamer desu! >w<
            if results:
                f.write('\n---------------------\n')
        
        print(f"\nResults saved to: {output_file}")
        print(f"File contains {len(set(r[0] for r in results))} unique streamers with matching commands.")
    else:
        print("\nNo streamers found with matching commands.")
        print("This could mean:")
        print("  - The streamers don't use StreamElements")
        print("  - They don't have commands with '$(touser)' and 'Everyone' permissions")
        print("  - The page structure has changed and selectors need updating")

if __name__ == "__main__":
    scan_streamelements_commands()

