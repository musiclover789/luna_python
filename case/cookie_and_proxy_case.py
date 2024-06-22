import asyncio

from devtools.browser import Browser
from utils.kill_process import Process


async def main():
    Process.kill_process()

    chromium_path = f'/Users/Documents/workspace/golang/Chromium.app/Contents/MacOS/Chromium'
    user_data_dir = f'/Users/Documents/workspace/python/luna_python/cache'

    browser = await Browser().launch(
        chromium_path=chromium_path,
        user_data_dir=user_data_dir,  # create_cache_dir_in_sub_dir(user_data_dir),
        headless=False,
        proxy_str=f'http://ip:port'
        #
        #          格式示例:
        #           Support all types of proxies in the example.
        #              "http://ip:port"
        #              "http://username:password@ip:port"
        #              "https://ip:port"
        #              "https://username:password@ip:port"
        #              "socks5://ip:port"
        #              "socks5://username:password@ip:port"
        #              proxy_str: f'http://username:password@ip:port"'
    )
    page = await browser.open_page("https://www.baidu.com")
    await asyncio.sleep(1)
    # You have two ways to set cookies.
    await page.set_cookie_by_url("key", "value", "https://www.baidu.com")
    await page.set_cookie_by_domain("key", "value", "domain")
    # get cookies
    cookie = await page.get_cookies(["https://www.baidu.com", "https://www.baidu.com"])
    print(cookie)
    await asyncio.sleep(10000)


if __name__ == '__main__':
    asyncio.run(main())
