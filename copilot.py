import time
import re
import os
from playwright.sync_api import sync_playwright

def get_copilot_response(prompt_text, show_window=False):
    if not prompt_text:
        return "Error: Empty prompt provided."

    with sync_playwright() as p:
        user_data_dir = "./playwright_profile" 
        
        # Launch browser. headless=False makes it visible.
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="msedge", 
            headless=not show_window, 
            args=['--start-maximized'] if show_window else [],
            no_viewport=True if show_window else False
        )
        
        page = browser.pages[0]
        try:
            page.goto("https://m365.cloud.microsoft/chat/")
            
            # Dismiss 'Try the app' popover if it appears
            try:
                popover_btn = "button.fai-next, .fui-TeachingPopover button"
                if page.is_visible(popover_btn, timeout=2500):
                    page.click(popover_btn)
            except:
                pass

            # Find the input box and click it
            input_selector = '#m365-chat-editor-target-element, textarea, [contenteditable="true"]'
            page.wait_for_selector(input_selector, timeout=15000)
            
            # Use .last to ensure we hit the main chat box, not a header search bar
            chat_box = page.locator(input_selector).last
            chat_box.click()
            
            # Increased pause to let the server and React UI fully initialize
            page.wait_for_timeout(1500) 
            
            # Mimic human typing so the React UI registers the input
            # delay=1 types it fast, but triggers required keyboard events
            page.keyboard.type(prompt_text, delay=1)
            
            page.wait_for_timeout(500) 
            page.keyboard.press("Enter")
            
            # Smart send button click as a fallback if Enter does not register
            page.evaluate("""() => {
                const btn = document.querySelector('button[title*="Submit"], button[aria-label*="Send"]');
                if (btn && !btn.disabled) btn.click();
            }""")

            target_selector = '[data-testid="markdown-reply"], .fai-ChatMessage__content'
            final_text = ""
            last_length = 0
            stable_count = 0
            
            # Increased range to 180 (allowing up to 3 minutes total wait time)
            for _ in range(180): 
                current_text = page.evaluate(f"() => {{ const msgs = document.querySelectorAll('{target_selector}'); return msgs.length > 0 ? msgs[msgs.length - 1].innerText : ''; }}")
                
                if current_text.strip():
                    if len(current_text) == last_length: 
                        stable_count += 1
                    else: 
                        stable_count = 0 
                    
                    last_length = len(current_text)
                    final_text = current_text
                
                # Increased stability requirement: text must not change for 3 full seconds
                if stable_count >= 3: 
                    break
                    
                time.sleep(1)
            
            browser.close()
            return final_text.strip() if final_text else "Error: No response captured."
            
        except Exception as e:
            browser.close()
            return f"Automation failed: {str(e)[:100]}"