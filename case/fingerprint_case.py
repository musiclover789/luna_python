import asyncio
import json

from devtools.browser import Browser
from utils.create_cache_dir import create_cache_dir_in_sub_dir
from utils.kill_process import kill_process

cache_path = ""


async def main():
    kill_process()

    chromium_path = f'/Users/Documents/workspace/golang/Chromium.app/Contents/MacOS/Chromium'
    user_data_dir = f'/Users/Documents/workspace/python/luna_python/cache'

    fingerprint = [
        "--luna_platform=Win32",
        "--luna_audio_random_int_number=981",
        "--luna_cavans_random_int_number=99981",
        "--luna_deviceMemory=8",
        "--luna_hardwareConcurrency=16",
        "--luna_devicePixelRatio=3",
        "--luna_header_set=true"
        "--luna_header_1=accept-language-lunareplace-en;q=0.9",
        "--luna_header_2=sec-ch-ua-arch-lunaremove-",
        "--luna_language=zh-CN",
        "--luna_languages=zh-CN",
        "--luna_timezone=Europe/London",
        "--luna_timezone_offset=3600000",
        "--luna_webrtc_public_ip=10.29.120.2",
        "--luna_webrtc_local_ip6_ip=0f0d8599-9999-4130-87ad-ec008a1c8d63.local",
        "--luna_user_agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "--luna_userAgentData=Google Chrome:92-luna-Chromium:92-luna-Not-A.Brand:24-luna-platform:win32-luna-mobile:false-luna-platform_version:6.1-luna-ua_full_version:92.0.4515.186-luna-model:PC-luna-architecture:x86_64",
        "--luna_screen=height:803,width:360,availHeight:803,availWidth:360,availLeft:0,availTop:0,colorDepth:24,pixelDepth:24",
        #
    ]
    browser = await Browser().launch(
        chromium_path=chromium_path,
        user_data_dir=create_cache_dir_in_sub_dir(user_data_dir),  # create_cache_dir_in_sub_dir(user_data_dir),
        headless=False,
        fingerprint=fingerprint,
    )

    await browser.open_page("https://www.baidu.com")

    await asyncio.sleep(10000)


if __name__ == '__main__':
    asyncio.run(main())
