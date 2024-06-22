import asyncio
from devtools.browser import Browser
from devtools.page import Page
from devtools.script.show_mouse_position import show_mouse_position
from utils.create_cache_dir import create_cache_dir_in_sub_dir
from utils.kill_process import Process


async def main():
    Process.kill_process()
    chromium_path = f'/Users/Documents/workspace/golang/Chromium.app/Contents/MacOS/Chromium'
    user_data_dir = f'/Users/Documents/workspace/python/luna_python/cache'

    browser = await Browser().launch(
        chromium_path=chromium_path,
        user_data_dir=create_cache_dir_in_sub_dir(user_data_dir),  # create_cache_dir_in_sub_dir(user_data_dir),
        headless=False,
        # proxy_str="",
        window_size=(1000, 600)
    )


    async def callback(page_self_obj: Page):
        async def request_response_date(request_data, response_data, response_body_data):
            print(request_data)
            print(response_data)
            print(response_body_data)
        await page_self_obj.request_response(request_response_date)

    page = await browser.open_page_and_listen("https://www.baidu.com", callback)

    async def callback(page_self_obj: Page):
        async def request_response_date(request_data, response_data, response_body_data):
            print(request_data)
            print(response_data)
            print(response_body_data)
        await page_self_obj.request_response(request_response_date)

    page = await browser.open_page_and_listen("https://www.baidu.com", callback)
    # case 1
    for i in range(10):
        await asyncio.sleep(1)
        node_result = await page.get_element_position_by_xpath_on_page(f'//*[@id="kw"]')
        print(node_result)
        if node_result:
            await page.run_js(show_mouse_position())
            await page.simulate_mouse_move_to_target(node_result["x"], node_result["y"])
        break
    browser.close()
    await asyncio.sleep(10000)


if __name__ == '__main__':
    asyncio.run(main())
