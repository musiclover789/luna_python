import asyncio
import json
import re

from devtools.browser import Browser
from devtools.script.show_mouse_position import show_mouse_position
from utils.create_cache_dir import create_cache_dir_in_sub_dir
from utils.kill_process import Process
from utils.wait_group import WaitGroup


async def main():
    Process.kill_process()
    chromium_path = f'/Users/hongyuji/Documents/workspace/golang/Chromium.app/Contents/MacOS/Chromium'
    user_data_dir = f'/Users/hongyuji/Documents/workspace/python/luna_python/cache'
    browser = await Browser().launch(
        chromium_path=chromium_path,
        user_data_dir=create_cache_dir_in_sub_dir(user_data_dir),
        fingerprint=["--luna_languages=en-US"],
        headless=False,
        window_size=(1024, 768)
    )
    wg = WaitGroup()
    await wg.add(1)

    async def callback(page_self_obj):
        async def request_response_date(request_data, response_data, response_body_data):
            print(len(json.dumps(request_data)))
            print(len(json.dumps(response_data)))
            print(len(json.dumps(response_body_data)))

        await page_self_obj.request_response(request_response_date)

        await page_self_obj.page_enable()

        async def page_load(message):
            print("页面加载完成", message)
            print("The page has finished loading.")
            await wg.done()

        page_self_obj.session.register_callback("Page.loadEventFired", page_load)

    page = await browser.open_page_and_listen("https://www.baidu.com", callback)
    await wg.wait()

    for i in range(10):
        await page.run_js(show_mouse_position())
        select_result = await page.get_element_position_by_xpath_on_page(f'//*[@id="kw"]')
        if select_result:
            await page.simulate_mouse_move_to_target(select_result["x"], select_result["y"])
            await page.simulate_mouse_click(select_result["x"], select_result["y"])
            await page.simulate_keyboard_input("luna browser 1")
            await page.simulate_backspace_key()
            await page.simulate_backspace_key()
            await asyncio.sleep(1)
            await page.simulate_enter_key()
            break
        else:
            await asyncio.sleep(1)

    for i in range(10):
        node_list = await page.get_all_child_element_by_xpath(f'//*[@id="content_left"]')
        if node_list:
            for node_item in node_list:
                first_node = await page.get_first_child_element_by_xpath(node_item["XPathSelector"])
                print(re.sub(r'\s+', '', first_node["TextContent"]))
                print()
        else:
            await asyncio.sleep(1)

    for page_item in await browser.get_pages():
        print(page_item.title)

    await asyncio.sleep(3)
    await browser.close()
    Process.kill_process_by_pid(browser.browser_pid)


if __name__ == '__main__':
    asyncio.run(main())
