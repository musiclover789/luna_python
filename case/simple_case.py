import asyncio

from devtools.browser import Browser
from utils.kill_process import Process


async def main():
    Process.kill_process()

    chromium_path = f'/Users/hongyuji/Documents/workspace/golang/Chromium.app/Contents/MacOS/Chromium'
    user_data_dir = f'/Users/hongyuji/Documents/workspace/python/luna_python/cache'

    browser = await Browser().launch(
        chromium_path=chromium_path,
        user_data_dir=user_data_dir,  # create_cache_dir_in_sub_dir(user_data_dir),
        headless=False,
    )

    page = await browser.open_page("https://www.baidu.com")

    await asyncio.sleep(3)

    print(await page.get_html())

    await asyncio.sleep(10000)


if __name__ == '__main__':
    asyncio.run(main())
