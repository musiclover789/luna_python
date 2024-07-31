# Luna- python版本



		Luna是专为抗指纹自动化爬虫设计的工具，包含抗指纹浏览器和自动化框架，让您能够自由实现所需功能。






golang版:https://github.com/musiclover789/luna




## Luna 是什么？

- luna是一个自动化框架，类似Selenium Pyppeteer Playwright。满足专业的自动化测试需求。
- luna浏览器、支持浏览器指纹、防关联相关功能的浏览器。
- luna浏览器支持第三方框架、如playwright等、





## Luna 有什么不同？

- 你可以使用luna框架，结合  **luna浏览器**  实现模拟浏览器指纹的能力，从而达到防关联测试的效果。





## 普通框架拥有的能力，luna框架也有吗？

- 基本上都有、包括不限于

- 打开浏览器、访问页面、获取页面网页内容

- css、xpath选择器、鼠标点击、鼠标移动轨迹移动、键盘输入、等

- http、https、socks5、百名单、或者用户名密码方式代理IP 所有格式、所有类型均支持。

- 执行js

- cookie

- 数据包采集等



## 效果演示



![效果展示-加载可能有些慢](https://i.ibb.co/yPkZLd0/mnggiflab-compressed-20231026-215253-min.gif)

## 抗指纹效果演示

你不但可以模拟pc、还可以模拟手机。

![效果展示-加载可能有些慢](https://i.ibb.co/nftHyHW/511714127971-pic.jpg)

![效果展示-加载可能有些慢](https://i.ibb.co/hCXrxn2/BEE68478001-EBDF49-A93-FA7-CBC7-C60-FD.png)

经过大量测试，目前基本可以过掉主流抗指纹识别;



```
https://www.browserscan.net/
https://uutool.cn/browser/
https://abrahamjuliot.github.io/creepjs/
```



## 使用限制

1、目前仅支持 Windows   x86-64 ，其他平台测试尚不充分。



##  Luna文档部分








## Luna浏览器部分

请注意、本框架要搭配luna抗指纹浏览器才能达到防关联效果

目前，我们已经将浏览器文件上传到 百度 网盘，并提供了下载链接：


2024-7-31版


链接: https://pan.baidu.com/s/11I3BlmSuNJgHxaQmZzWf5Q 提取码: e4uh






<没有授权文件的用户,仅可以测试useragent指纹部分,其他指纹不会生效,付费获取授权文件，联系作者获取>

作者QQ: 80258153

email:80258153@qq.com

<仅框架部分是免费、开源的，浏览器部分不开源也不免费>





## 目前支持指纹项：



**注意**：您必须需要下载和使用luna浏览器，才能使在框架中设置的指纹生效。
如果你即便知道可以修改，但是不知道改成什么样子的指纹，建议直接咨询作者本人。



|      | 指纹项                                                   |
| ---- | -------------------------------------------------------- |
|      | user_agent指纹                                           |
|      | canvas指纹                                               |
|      | webgl指纹、webgpu                                                |
|      | platform平台                                             |
|      | timezone时区                                             |
|      | timezone_offset时区偏移量                                |
|      | languages语言                                            |
|      | userAgentData、全版本号、内核类型等                      |
|      | platform                                                 |
|      | header 修改                                              |
|      | deviceMemory                                             |
|      | hardwareConcurrency                                      |
|      | UNMASKED_VENDOR_WEBGL                                    |
|      | UNMASKED_RENDERER_WEBGL                                  |
|      | GL_VERSION                                               |
|      | GL_SupportedExtensions                                   |
|      | GL_VENDOR                                                |
|      | GL_RENDERER                                              |
|      | GL_SHADING_LANGUAGE_VERSION                              |
|      | 是否webdriver                                            |
|      | 是否brave                                                |
|      | 是否selenium                                             |
|      | 是否来自于真实键盘                                       |
|      | 是否来自于真实鼠标                                       |
|      | 鼠标移动轨迹                                             |
|      | 键盘拼音输入法模拟输入                                   |
|      | cdp检测                                                  |
|      | webRTC 公网ip4、局域网ip6                                |
|      | screen、屏幕尺寸、分辨率、色彩深度、devicePixelRatio等。 |
|      | 声卡指纹                                                 |
|      | 字体列表                                                 |
|      | 触控支持                                                 |
|      | 电池电量等                                               |
|      | client_rects                                               |








## 快速入门

###### 

```bash
import asyncio

from devtools.browser import Browser
from utils.kill_process import Process


async def main():
    Process.kill_process()

    chromium_path = f'C:\\luna\\chrome.exe'
    user_data_dir = f'C:\\luna\\cache'

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

```



**增加难度-等待页面加载**

```
import asyncio
from devtools.browser import Browser
from utils.create_cache_dir import create_cache_dir_in_sub_dir
from utils.kill_process import Process
from utils.wait_group import WaitGroup


async def main():
    chromium_path = f'C:\\luna\\chrome.exe'
    user_data_dir = f'C:\\luna\\cache'
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
        print("页面加载完成", message)
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
        print("页面加载完成", message)
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
    #Process.kill_process_by_pid(browser.browser_pid)


if __name__ == '__main__':
    asyncio.run(main())

```



**设置指纹项 示例**--请注意，这里只是示例，你需要改成正确的指纹，这里只是展示在哪里改。具体指纹说明，参考完整文档。



```
import asyncio
import json

from devtools.browser import Browser
from utils.create_cache_dir import create_cache_dir_in_sub_dir
from utils.kill_process import kill_process

cache_path = ""


async def main():
    kill_process()

    chromium_path = f'C:\\luna\\chrome.exe'
    user_data_dir = f'C:\\luna\\cache'

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

```



**选择器示例**



```
import asyncio
from devtools.browser import Browser
from devtools.input.wheel.wheel import Direction
from devtools.script.show_mouse_position import show_mouse_position
from utils.create_cache_dir import create_cache_dir_in_sub_dir
from utils.kill_process import Process


async def main():
    Process.kill_process()
    chromium_path = f'C:\\luna\\chrome.exe'
    user_data_dir = f'C:\\luna\\cache'

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
    #Process.kill_process_by_pid(browser.browser_pid)


if __name__ == '__main__':
    asyncio.run(main())

```







----------------------



#### 常见问题回复



1、**可以自己随便修改指纹吗？**

     是的、理论上无限指纹;



2、**目前支持Linux 系统吗？**

     暂时不支持



3、**我用了这个框架就可以换指纹吗？**

	您需要下载并使用luna浏览器，结合框架才可以，单独的框架是不能达到效果的。



4、**为什么我测试browserscan时候并不是100%**

     说明你设置的指纹有问题，或者您根本就不是授权用户，指纹设置不生效。



5、**为什么我测试browserscan时候并不是100%**

    浏览器源代码并不提供，另外luna抗指纹浏览器授权是收费的，200/台设备，无时间限制，不同版本不同授权，并不通用，不提供任何免费测试。
    
    如果您喜欢免费，您可以免费获取一个授权，前提是你需要用luna完成一个相对完整的案例，并且将教程发布到csdn、知乎、等平台，链接本github网址，持续2周以上，直接联系作者领取。



6、**支持其他框架吗？**

    暂时仅支持luna-goalng版本- python版本，其他第三方框架，暂不支持。



7、**为什么我测试browserscan时候并不是100%**

     说明你设置的指纹有问题，或者您根本就不是授权用户，指纹设置不生效。












##### 免责声明：



请在使用本框架之前仔细阅读并理解以下内容。本框架仅用于合法目的，并且作者不承担任何因非法或滥用本框架而导致的责任或后果。通过使用本框架，您同意自行承担风险，并对使用本框架的后果负全部责任。

1. 合法使用：本框架旨在为用户提供便利和支持，并帮助用户完成特定的任务。用户应确保在使用本框架时遵守所有适用的法律、法规和政策。禁止将本框架用于非法目的，包括但不限于侵犯他人隐私、违反知识产权、进行网络攻击等行为。
2. 自担风险：使用本框架的风险完全由用户自行承担。作者不对因使用本框架而导致的任何直接或间接损失或后果承担责任，包括但不限于数据损失、设备故障、业务中断或其他经济损失。
3. 免责声明的范围：本免责声明适用于本框架的所有功能和服务，无论是明示的还是暗示的。作者不提供任何形式的保证，明示或暗示，包括但不限于适销性、特定用途适用性、安全性和准确性。用户对于本框架的选择和使用应自行审慎考虑并承担相应风险。
4. 第三方链接：本框架可能包含指向第三方网站或资源的链接。这些链接仅作为方便提供，不代表作者对这些网站或资源的认可或控制。用户访问任何第三方链接所造成的风险由用户自行承担。
5. 法律适用：使用本框架和解释本免责声明的所有争议均受到适用法律的管辖。

请在使用本框架之前仔细阅读并理解本免责声明的内容。如果您不同意本免责声明的任何部分，请立即停止使用本框架。

如果您有任何问题或疑虑，请与作者联系。谢谢您的合作和理解！
