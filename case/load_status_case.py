import asyncio
from devtools.browser import Browser
from utils.create_cache_dir import create_cache_dir_in_sub_dir
from utils.kill_process import Process
from utils.wait_group import WaitGroup


async def main():
    chromium_path = f'/Users/Documents/workspace/golang/Chromium.app/Contents/MacOS/Chromium'
    user_data_dir = f'/Users/Documents/workspace/python/luna_python/cache'
    browser = await Browser().launch(
        chromium_path=chromium_path,
        user_data_dir=create_cache_dir_in_sub_dir(user_data_dir),
        headless=False,
        window_size=(1000, 600)
    )

    # case 1 When you first open the page, you can monitor whether it has finished loading like this.
    async def callback(page_self_obj):
        await page_self_obj.page_enable()

        async def page_load_1(message):
            print("1页面加载完成", message)
            print("The page has finished loading.")

        page_self_obj.session.register_callback("Page.loadEventFired", page_load_1)

    page1 = await browser.open_page_and_listen("https://www.baidu.com", callback)

    # case 2 You can also write it this way anywhere you need.

    async def page_load_2(message):
        print("2页面加载完成", message)
        print("The page has finished loading.")

    page2 = await browser.open_page("https://www.google.com")
    await page2.page_enable()
    page2.session.register_callback("Page.loadEventFired", page_load_2)

    # case 3
    # You can integrate the functions of WaitGroup to determine if the page has finished loading.
    # If it hasn't finished, then make it wait until the loading is complete

    wg = WaitGroup()
    await wg.add(1)

    async def page_load_3(message):
        print("2页面加载完成", message)
        print("The page has finished loading.")
        await wg.done()

    page3 = await browser.open_page("https://www.baidu.com")
    await page3.page_enable()
    page3.session.register_callback("Page.loadEventFired", page_load_3)
    await wg.wait()
    print("=========================")
    await page1.close()
    await page2.close()
    await browser.close()
    #
    Process.kill_process_by_pid(browser.browser_pid)


if __name__ == '__main__':
    asyncio.run(main())
