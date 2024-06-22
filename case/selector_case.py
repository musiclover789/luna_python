import asyncio
from devtools.browser import Browser
from devtools.input.wheel.wheel import Direction
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
        window_size=(1000, 600)
    )

    page = await browser.open_page("https://www.baidu.com")
    # case 1 This will return the coordinates of this element.
    await asyncio.sleep(3)
    node_result = await page.get_element_position_by_xpath_on_page(f'//*[@id="kw"]')
    print(node_result["x"], node_result["y"])
    # case 2 Some elements may be dynamic, so to wait for element loading, you can also implement it this way.
    for i in range(1):
        await asyncio.sleep(1)
        node_result = await page.get_element_position_by_xpath_on_page(f'//*[@id="kw"]')
        if node_result:
            await page.run_js(show_mouse_position())
            await page.simulate_mouse_move_to_target(node_result["x"], node_result["y"])
            await page.simulate_mouse_click(node_result["x"], node_result["y"])

    # case 3 more case
    await page.simulate_keyboard_input("luna")
    await page.simulate_enter_key()
    await page.simulate_backspace_key()
    await page.get_element_position_by_css_on_page(f'body > input[type=text]')
    await page.get_element_position_by_xpath_on_page(f'body > input[type=text]')
    await page.simulate_move_mouse(1, 2, 100, 200)
    await page.simulate_mouse_move_to_target(2, 200)
    await page.simulate_mouse_scroll(2, 3, 200, Direction.DOWN)
    await page.navigate("https://www.baidu.com")
    # case 4 more case
    for pageItem in await browser.get_pages():
        print("pages", pageItem, pageItem.url)
    # case 5
    await page.get_element_position_by_xpath_on_page(f'//*[@id="kw"]')
    await page.get_element_position_by_css_on_page(f'css selector')
    await page.get_element_by_xpath(f'//*[@id="kw"]')
    await page.get_element_by_css(f'css selector')
    result = await page.get_all_child_element_by_xpath(f'//*[@id="form"]/span[1]')
    for item in result:
        print(item, ">>>>>")
    result = await page.get_all_child_element_by_css(f'css selector')
    for item in result:
        print(item, ">>>>>")
    result = await page.get_first_child_element_by_xpath(f'//*[@id="form"]/span[1]')
    result = await page.get_first_child_element_by_css(f'css selector')
    result = await page.get_last_child_element_by_xpath(f'//*[@id="form"]/span[1]')
    result = await page.get_last_child_element_by_css(f'css selector')
    result = await page.get_next_sibling_element_by_xpath(f'//*[@id="form"]/span[1]/i[2]')
    result = await page.get_next_sibling_element_by_css(f'css selector')
    result = await page.get_previous_sibling_element_by_xpath(f'//*[@id="form"]/span[1]/i[2]')
    result = await page.get_previous_sibling_element_by_css(f'css selector')
    result = await page.get_parent_element_by_xpath(f'//*[@id="form"]/span[1]/i[2]')
    result = await page.get_parent_element_by_css(f'css selector')
    await asyncio.sleep(100)
    browser.close()
    Process.kill_process_by_pid(browser.browser_pid)


if __name__ == '__main__':
    asyncio.run(main())
