"""
UwU~! This script scans Twitch.tv for active streamers across all categories and logs their handles to a text file desu! >w<
Kyaa~! It's so exciting to find all the streamers nya~! ✨
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
import re

def setup_driver():
    """UwU~! Sets up and returns a Chrome WebDriver instance desu! >w<"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Runs in background so no one sees it nya~! ✨
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

def extract_streamers_from_page(driver):
    """
    Kyaa~! Extracts streamer usernames from the current Twitch page desu! >w<
    So many streamers to find nya~! ✨
    
    Args:
        driver: Selenium WebDriver instance (the browser thingy desu~!)
        
    Returns:
        set: Set of streamer usernames found on the page (so many usernames UwU~!)
    """
    streamer_handles = set()
    
    try:
        # UwU~! Wait for content to load nya~! So exciting desu! >w<
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )
        
        # Helper function to extract username from href (so helpful desu~! ✨)
        def extract_username_from_href(href):
            if not href:
                return None
            # UwU~! Handle both absolute and relative URLs desu! >w<
            if href.startswith("http"):
                parts = href.split("/")
                if len(parts) >= 4:
                    domain = parts[2] if len(parts) > 2 else ""
                    if "twitch.tv" in domain and len(parts) > 3:
                        username = parts[3].split("?")[0].split("#")[0]
                        return username
            elif href.startswith("/"):
                # Kyaa~! Relative URL like /username nya~! So cute desu! ✨
                parts = href.split("/")
                if len(parts) >= 2:
                    username = parts[1].split("?")[0].split("#")[0]
                    return username
            return None
        
        # Method 1: UwU~! Look for all links (both absolute and relative) desu! >w<
        try:
            links = driver.find_elements(By.TAG_NAME, "a")
            
            for link in links:
                try:
                    href = link.get_attribute("href")
                    if not href:
                        # Try getting href from JavaScript if attribute is None
                        href = driver.execute_script("return arguments[0].getAttribute('href');", link)
                    
                    username = extract_username_from_href(href)
                    if username:
                        # Kyaa~! Filter out common non-username paths nya~! We don't want those desu! >w<
                        if username not in ["directory", "videos", "p", "settings", "subscriptions",
                                              "wallet", "inventory", "drops", "download", "jobs", 
                                              "turbo", "prime", "partner", "advertise", "music",
                                              "browse", "search", "popout", "moderator", "manager",
                                              "discover", "pog", "clips", "collections", "chat",
                                              "bits", "extensions", "store", "help", "about"]:
                            if len(username) > 0 and not username.startswith("_") and username != "":
                                streamer_handles.add(username)
                except:
                    continue
        except:
            pass
        
        # Method 2: UwU~! Look for specific Twitch streamer card elements with data attributes desu! >w<
        try:
            streamer_elements = driver.find_elements(By.CSS_SELECTOR, 
                "[data-a-target='user-channel-link'], "
                "[data-a-target='preview-card-channel-link'], "
                "[data-a-target='user-card-link'], "
                "a[href^='https://www.twitch.tv/']:not([href*='/directory']):not([href*='/videos']):not([href*='/settings']), "
                "a[href^='/']:not([href*='/directory']):not([href*='/videos']):not([href*='/settings'])")
            for element in streamer_elements:
                href = element.get_attribute("href")
                username = extract_username_from_href(href)
                if username and username not in ["directory", "videos", "p", "settings", "subscriptions", 
                                                  "wallet", "inventory", "drops", "download", "jobs", 
                                                  "turbo", "prime", "partner", "advertise", "music",
                                                  "browse", "search", "popout", "moderator", "manager",
                                                  "discover", "pog", "clips", "collections", "chat"]:
                    if len(username) > 0 and not username.startswith("_") and username != "":
                        streamer_handles.add(username)
        except:
            pass
        
        # Method 2b: Kyaa~! Look for streamer cards by class names and relative links nya~! ✨
        try:
            # UwU~! Twitch uses various class names for streamer cards desu! So many different ones! >w<
            card_selectors = [
                "[class*='Layout-sc-'] a[href^='/']",
                "[class*='ScCoreLink']",
                "a[href^='/']:not([href*='directory']):not([href*='videos']):not([href*='settings'])",
                # Directory page specific selectors
                "[data-a-target='preview-card-image-link']",
                "[data-a-target='preview-card-avatar-link']"
            ]
            for selector in card_selectors:
                try:
                    cards = driver.find_elements(By.CSS_SELECTOR, selector)
                    for card in cards:
                        href = card.get_attribute("href")
                        username = extract_username_from_href(href)
                        if username and username not in ["directory", "videos", "p", "settings", "subscriptions", 
                                                          "wallet", "inventory", "drops", "download", "jobs", 
                                                          "turbo", "prime", "partner", "advertise", "music",
                                                          "browse", "search", "popout", "moderator", "manager",
                                                          "discover", "pog", "clips", "collections", "chat"]:
                            if len(username) > 0 and not username.startswith("_") and username != "":
                                streamer_handles.add(username)
                except:
                    continue
        except:
            pass
        
        # Method 3: UwU~! Look for elements with aria-label containing streamer names desu! >w<
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, "[aria-label]")
            for element in elements:
                aria_label = element.get_attribute("aria-label")
                if aria_label and ("'s channel" in aria_label or "streaming" in aria_label.lower()):
                    parts = aria_label.split("'s")
                    if parts:
                        potential_username = parts[0].strip()
                        if len(potential_username) > 0 and len(potential_username) < 30:
                            streamer_handles.add(potential_username)
        except:
            pass
        
        # Method 4: Kyaa~! Use JavaScript to get all links from the DOM (catches lazy-loaded content) nya~! ✨
        try:
            all_hrefs = driver.execute_script("""
                var links = document.querySelectorAll('a[href]');
                var hrefs = [];
                for (var i = 0; i < links.length; i++) {
                    var href = links[i].getAttribute('href');
                    if (href) {
                        // Also try getting href from the link element directly
                        if (!href || href === 'null' || href === 'undefined') {
                            href = links[i].href;
                        }
                        if (href) hrefs.push(href);
                    }
                }
                return hrefs;
            """)
            
            for href in all_hrefs:
                if href and href != "null" and href != "undefined":
                    username = extract_username_from_href(href)
                    if username and username not in ["directory", "videos", "p", "settings", "subscriptions", 
                                                      "wallet", "inventory", "drops", "download", "jobs", 
                                                      "turbo", "prime", "partner", "advertise", "music",
                                                      "browse", "search", "popout", "moderator", "manager",
                                                      "discover", "pog", "clips", "collections", "chat",
                                                      "bits", "extensions", "store", "help", "about"]:
                        if len(username) > 0 and not username.startswith("_") and username != "":
                            streamer_handles.add(username)
        except Exception as e:
            pass
        
        # Method 5: UwU~! Try to find streamer links by looking for patterns in the page source desu! >w<
        # Kyaa~! This is the most reliable method as it doesn't depend on DOM structure nya~! ✨
        # ALWAYS run this as a backup to catch streamers that DOM methods miss (so important desu~!)
        try:
            # Look for links that match the pattern of streamer channels
            page_source = driver.page_source
            import re
            
            # UwU~! More comprehensive patterns - try to catch all possible formats desu! >w<
            patterns = [
                # Kyaa~! Absolute URLs nya~! ✨
                    r'https?://(?:www\.)?twitch\.tv/([a-zA-Z0-9_]{1,25})(?:[?/#"\'<>\\s]|$)',
                    r'https?://twitch\.tv/([a-zA-Z0-9_]{1,25})(?:[?/#"\'<>\\s]|$)',
                    # UwU~! Relative URLs in href attributes desu! >w<
                    r'href=["\']/([a-zA-Z0-9_]{1,25})(?:[?/#"\'<>\\s]|["\'])',
                    r'href=/([a-zA-Z0-9_]{1,25})(?:[?/#"\'<>\\s]|["\'])',
                    # Just the path pattern
                    r'/([a-zA-Z0-9_]{1,25})["\']',  # Pattern like "/username" or '/username'
                    # Domain/username pattern
                    r'twitch\.tv/([a-zA-Z0-9_]{1,25})(?:[?/#"\'<>\\s]|$)',
                    # In JSON/data attributes
                    r'["\']/([a-zA-Z0-9_]{1,25})["\']',
                    r'user["\']?s?["\']?:["\']?([a-zA-Z0-9_]{1,25})["\']',
                ]
                
            excluded = ["directory", "videos", "p", "settings", "subscriptions", 
                       "wallet", "inventory", "drops", "download", "jobs", 
                       "turbo", "prime", "partner", "advertise", "music",
                       "browse", "search", "popout", "moderator", "manager",
                       "discover", "pog", "clips", "collections", "chat",
                       "bits", "extensions", "store", "help", "about",
                       "directory", "game", "category", "discover", "p"]
            
            for pattern in patterns:
                try:
                    matches = re.findall(pattern, page_source, re.IGNORECASE)
                    for match in matches:
                        if isinstance(match, tuple):
                            match = match[0] if match else ""
                        match = match.lower().strip()
                        if match and match not in excluded:
                        # Kyaa~! Additional validation: username should be reasonable nya~! ✨
                        # UwU~! Twitch usernames: 1-25 chars, alphanumeric and underscores desu! >w<
                            if (len(match) >= 1 and len(match) <= 25 and 
                                not match.startswith("_") and 
                                match.replace("_", "").isalnum() and
                                not match.isdigit()):  # Exclude pure numbers
                                streamer_handles.add(match)
                except:
                    continue
        except Exception as e:
            pass
        
    except Exception as e:
        print(f"    Error extracting streamers: {e}")
    
    # UwU~! Debug: Print how many streamers found (only if > 0 to avoid spam) desu! >w<
    if len(streamer_handles) > 0:
        pass  # Don't print, just for debugging if needed nya~! ✨
    
    return streamer_handles

def get_categories(driver):
    """
    Kyaa~! Gets a list of all Twitch categories/games from the directory desu! >w<
    So many categories to explore nya~! ✨
    
    Args:
        driver: Selenium WebDriver instance (the browser thingy UwU~!)
        
    Returns:
        list: List of category slugs/names (so many categories desu~!)
    """
    categories = []
    
    try:
        print("Loading Twitch directory to get categories...")
        driver.get("https://www.twitch.tv/directory")
        time.sleep(5)
        
        # UwU~! Scroll to load more categories desu! >w<
        print("Loading categories...")
        for i in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # Kyaa~! Find category links nya~! So exciting desu! ✨
        try:
            # Look for links to category pages
            category_links = driver.find_elements(By.CSS_SELECTOR, 
                "a[href*='/directory/game/'], "
                "a[href*='/directory/category/'], "
                "[data-a-target='game-link']")
            
            for link in category_links:
                href = link.get_attribute("href")
                if href and "/directory/game/" in href:
                    # Extract category name from URL
                    parts = href.split("/directory/game/")
                    if len(parts) > 1:
                        category = parts[1].split("?")[0].split("#")[0]
                        if category and category not in categories:
                            categories.append(category)
                elif href and "/directory/category/" in href:
                    parts = href.split("/directory/category/")
                    if len(parts) > 1:
                        category = parts[1].split("?")[0].split("#")[0]
                        if category and category not in categories:
                            categories.append(category)
        except Exception as e:
            print(f"Error extracting categories: {e}")
        
        # UwU~! If we didn't find many categories, try alternative method desu! >w<
        if len(categories) < 10:
            print("Trying alternative method to find categories...")
            try:
                # Kyaa~! Look for any links containing game names nya~! ✨
                all_links = driver.find_elements(By.TAG_NAME, "a")
                for link in all_links:
                    href = link.get_attribute("href")
                    if href and "/directory/game/" in href:
                        parts = href.split("/directory/game/")
                        if len(parts) > 1:
                            category = parts[1].split("?")[0].split("#")[0]
                            if category and category not in categories and len(category) > 0:
                                categories.append(category)
            except:
                pass
        
        print(f"Found {len(categories)} categories")
        
    except Exception as e:
        print(f"Error getting categories: {e}")
    
    return categories

def scan_category(driver, category, all_streamers):
    """
    UwU~! Scans a specific category page for streamers desu! >w<
    So many streamers to find in each category nya~! ✨
    
    Args:
        driver: Selenium WebDriver instance (the browser thingy desu~!)
        category: Category name/slug (so cute desu! >w<)
        all_streamers: Set to add streamers to (collecting all the streamers nya~!)
    """
    try:
        url = f"https://www.twitch.tv/directory/game/{category}"
        driver.get(url)
        time.sleep(5)  # Initial load wait
        
        # Kyaa~! Wait for content to start loading nya~! So exciting desu! ✨
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "a"))
            )
        except:
            pass
        
        # UwU~! Verify page loaded - check if we're on the right page desu! >w<
        current_url = driver.current_url
        page_title = driver.title.lower()
        
        # Kyaa~! Check if page loaded correctly nya~! ✨
        if "directory" not in current_url.lower() and "game" not in current_url.lower():
            # UwU~! Might have been redirected, try again desu! >w<
            driver.get(url)
            time.sleep(5)
        
        # UwU~! Check if page has content - look for common Twitch page elements desu! >w<
        try:
            # Kyaa~! Wait for streamer cards or links to appear nya~! ✨
            WebDriverWait(driver, 15).until(
                lambda d: len(d.find_elements(By.TAG_NAME, "a")) > 10
            )
            # UwU~! Additional wait for lazy-loaded content to start appearing desu! >w<
            time.sleep(3)
        except:
            # Kyaa~! Page might be loading slowly, wait a bit more nya~! ✨
            time.sleep(5)
        
        # UwU~! Wait for any loading indicators to disappear desu! >w<
        try:
            # Kyaa~! Wait for page to stabilize (no more major changes) nya~! ✨
            for stability_check in range(3):
                initial_height = driver.execute_script("return document.body.scrollHeight;")
                time.sleep(2)
                final_height = driver.execute_script("return document.body.scrollHeight;")
                if initial_height == final_height:
                    break
        except:
            time.sleep(3)
        
        # UwU~! Track count at start of this category desu! >w<
        streamers_at_start = len(all_streamers)
        no_change_count = 0
        max_scrolls = 30  # Kyaa~! Increased from 5 nya~! So many scrolls desu! ✨
        
        # UwU~! Extract initial streamers desu! >w<
        category_streamers = extract_streamers_from_page(driver)
        
        # Kyaa~! Debug: Check if page has any content at all nya~! ✨
        if len(category_streamers) == 0:
            # UwU~! Check if page actually loaded content and has streamers desu! >w<
            page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            link_count = len(driver.find_elements(By.TAG_NAME, "a"))
            page_source = driver.page_source.lower()
            
            # Kyaa~! Check for indicators that streamers might be present nya~! ✨
            has_live_indicators = ("live" in page_text or "viewers" in page_text or 
                                  "watching" in page_text or "streaming" in page_text)
            has_twitch_links = "twitch.tv/" in page_source
            
            # UwU~! If no streamers found initially, wait longer and try different approaches desu! >w<
            time.sleep(5)
            
            # Kyaa~! Try scrolling to trigger lazy loading nya~! ✨
            driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 1000);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            
            # UwU~! Try extraction again desu! >w<
            category_streamers = extract_streamers_from_page(driver)
            
            # Kyaa~! If still no streamers but page seems to have content, try more aggressive extraction nya~! ✨
            if len(category_streamers) == 0 and (has_live_indicators or has_twitch_links):
                # UwU~! Page has content but we're not finding streamers - try JavaScript extraction desu! >w<
                try:
                    # Kyaa~! Use JavaScript to find all possible streamer links nya~! ✨
                    js_streamers = driver.execute_script("""
                        var streamers = new Set();
                        var links = document.querySelectorAll('a[href]');
                        for (var i = 0; i < links.length; i++) {
                            var href = links[i].href || links[i].getAttribute('href');
                            if (href) {
                                var match = href.match(/twitch\\.tv\\/([a-zA-Z0-9_]{1,25})(?:[?/#]|$)/i);
                                if (match && match[1]) {
                                    var username = match[1].toLowerCase();
                                    if (username && !['directory', 'videos', 'settings', 'subscriptions'].includes(username)) {
                                        streamers.add(username);
                                    }
                                }
                                // Also check relative URLs
                                match = href.match(/^\\/([a-zA-Z0-9_]{1,25})(?:[?/#]|$)/i);
                                if (match && match[1]) {
                                    var username = match[1].toLowerCase();
                                    if (username && !['directory', 'videos', 'settings', 'subscriptions'].includes(username)) {
                                        streamers.add(username);
                                    }
                                }
                            }
                        }
                        return Array.from(streamers);
                    """)
                    if js_streamers:
                        for username in js_streamers:
                            category_streamers.add(username)
                except:
                    pass
        
        all_streamers.update(category_streamers)
        previous_total = len(all_streamers)
        
        # UwU~! Scroll and load more content desu! >w<
        for i in range(max_scrolls):
            # Kyaa~! Get current page height and scroll position before scroll nya~! ✨
            previous_height = driver.execute_script("return document.body.scrollHeight;")
            previous_link_count = len(driver.find_elements(By.TAG_NAME, "a"))
            
            # UwU~! Scroll down to bottom desu! >w<
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Kyaa~! Wait for lazy-loaded content to appear nya~! ✨
            # UwU~! Wait for page height to increase or new links to appear desu! >w<
            try:
                WebDriverWait(driver, 8).until(
                    lambda d: (
                        d.execute_script("return document.body.scrollHeight;") > previous_height or
                        len(d.find_elements(By.TAG_NAME, "a")) > previous_link_count + 5
                    )
                )
            except:
                # Kyaa~! If no change detected, wait a bit anyway for content to load nya~! ✨
                time.sleep(3)
            
            # UwU~! Additional wait for content to fully render desu! >w<
            time.sleep(2)
            
            # Kyaa~! Check if content actually loaded nya~! ✨
            new_height = driver.execute_script("return document.body.scrollHeight;")
            new_link_count = len(driver.find_elements(By.TAG_NAME, "a"))
            
            # UwU~! If page height increased, wait a bit more for images/content to load desu! >w<
            if new_height > previous_height:
                time.sleep(2)  # Kyaa~! Give lazy-loaded images and content time to render nya~! ✨
            
            # UwU~! Also try scrolling in smaller increments to trigger lazy loading desu! >w<
            if i % 2 == 0:
                # Kyaa~! Scroll a bit more to ensure we trigger lazy loading nya~! ✨
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # UwU~! Extract streamers after each scroll to catch newly loaded content desu! >w<
            new_streamers = extract_streamers_from_page(driver)
            all_streamers.update(new_streamers)
            current_total = len(all_streamers)
            
            # Kyaa~! Get new page height after scroll (already got it above, but recalculate) nya~! ✨
            final_height = driver.execute_script("return document.body.scrollHeight;")
            
            # UwU~! Check if we're still finding new streamers desu! >w<
            if current_total == previous_total:
                no_change_count += 1
                # Kyaa~! If we haven't found new streamers in 3 consecutive scrolls, try scrolling more nya~! ✨
                if no_change_count >= 3:
                    # UwU~! Try scrolling to different positions to trigger more loading desu! >w<
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.7);")
                    time.sleep(3)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.9);")
                    time.sleep(3)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)  # UwU~! Wait longer for content to load desu! >w<
                    
                    # Kyaa~! Wait for content to appear nya~! ✨
                    try:
                        WebDriverWait(driver, 5).until(
                            lambda d: len(d.find_elements(By.TAG_NAME, "a")) > new_link_count
                        )
                    except:
                        time.sleep(2)
                    
                    new_streamers = extract_streamers_from_page(driver)
                    all_streamers.update(new_streamers)
                    current_total = len(all_streamers)
                    
                    if current_total == previous_total:
                        # Kyaa~! Still no change, likely reached the end nya~! ✨
                        break
                    else:
                        no_change_count = 0
            else:
                no_change_count = 0
            
            previous_total = current_total
            
            # UwU~! Check if page height changed (indicates new content loaded) desu! >w<
            if final_height == previous_height and no_change_count >= 2:
                # Kyaa~! Page height hasn't changed and no new streamers, likely no more content nya~! ✨
                break
        
        # UwU~! Final extraction to catch any remaining streamers desu! >w<
        final_streamers = extract_streamers_from_page(driver)
        all_streamers.update(final_streamers)
        
        # Kyaa~! Return the number of NEW streamers found in this category nya~! ✨
        category_count = len(all_streamers) - streamers_at_start
        
        # UwU~! Debug: If we found 0, try one more time with a longer wait and more scrolling desu! >w<
        if category_count == 0:
            # Kyaa~! Wait longer and try multiple extraction methods nya~! ✨
            time.sleep(5)
            
            # UwU~! Try scrolling through the entire page more thoroughly desu! >w<
            page_height = driver.execute_script("return document.body.scrollHeight;")
            scroll_positions = [0.2, 0.4, 0.6, 0.8, 1.0]
            
            for scroll_pos in scroll_positions:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight * {});".format(scroll_pos))
                time.sleep(2.5)
                retry_streamers = extract_streamers_from_page(driver)
                all_streamers.update(retry_streamers)
            
            # Kyaa~! Scroll back to top and then to bottom to trigger any lazy loading nya~! ✨
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            
            # UwU~! Final extraction desu! >w<
            final_retry = extract_streamers_from_page(driver)
            all_streamers.update(final_retry)
            category_count = len(all_streamers) - streamers_at_start
        
        return category_count
    except Exception as e:
        print(f"    Error scanning category {category}: {e}")
        return 0

def scan_twitch_streamers(output_file='twitch_streamers.txt', max_categories=None):
    """
    UwU~! Scans Twitch.tv for active streamers across all categories and saves their handles to a file desu! >w<
    So exciting to find all the streamers nya~! ✨
    
    Args:
        output_file (str): Path to the output text file (where we save all the streamers desu~!)
        max_categories (int): Maximum number of categories to scan (None for all - so many categories nya~!)
    """
    driver = setup_driver()
    if not driver:
        return
    
    all_streamers = set()
    
    try:
        # Step 1: Get all categories
        categories = get_categories(driver)
        
        if not categories:
            print("No categories found. Falling back to homepage scan...")
            # Kyaa~! Fallback to homepage nya~! ✨
            driver.get("https://www.twitch.tv")
            time.sleep(5)
            for i in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            all_streamers = extract_streamers_from_page(driver)
        else:
            # Step 2: Scan each category
            if max_categories:
                categories = categories[:max_categories]
            
            print(f"\nScanning {len(categories)} categories for streamers...")
            print("=" * 70)
            
            for idx, category in enumerate(categories, 1):
                print(f"[{idx}/{len(categories)}] Scanning category: {category}")
                count = scan_category(driver, category, all_streamers)
                print(f"    Found {count} streamers in this category (Total unique: {len(all_streamers)})")
                time.sleep(1)  # Small delay between categories
        
        # UwU~! Also scan the homepage for additional streamers desu! >w<
        print("\nScanning homepage for additional streamers...")
        driver.get("https://www.twitch.tv")
        time.sleep(5)
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        homepage_streamers = extract_streamers_from_page(driver)
        all_streamers.update(homepage_streamers)
        print(f"Found {len(homepage_streamers)} additional streamers on homepage")
        
        # Kyaa~! Write to file nya~! ✨
        if all_streamers:
            print(f"\n{'=' * 70}")
            print(f"Total unique streamers found: {len(all_streamers)}")
            with open(output_file, 'w', encoding='utf-8') as f:
                for handle in sorted(all_streamers):
                    f.write(handle + '\n')
            print(f"Streamer handles saved to {output_file}")
        else:
            print("No streamer handles found. The page structure might have changed.")
            print("You may need to update the selectors in the script.")
        
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user.")
        if all_streamers:
            print(f"Saving {len(all_streamers)} streamers found so far...")
            with open(output_file, 'w', encoding='utf-8') as f:
                for handle in sorted(all_streamers):
                    f.write(handle + '\n')
            print(f"Partial results saved to {output_file}")
    except Exception as e:
        print(f"Error scanning Twitch: {e}")
    finally:
        driver.quit()
        print("Scan complete.")

if __name__ == "__main__":
    import sys
    
    output_filename = "twitch_streamers.txt"
    max_categories = None
    
    # Allow limiting categories via command line argument
    if len(sys.argv) > 1:
        try:
            max_categories = int(sys.argv[1])
            print(f"Limiting scan to {max_categories} categories")
        except ValueError:
            print("Invalid argument. Usage: python scan_twitch_streamers.py [max_categories]")
            sys.exit(1)
    
    scan_twitch_streamers(output_filename, max_categories)

