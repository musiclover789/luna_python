import asyncio
import json
import math
import time
import random
from typing import Optional, Dict, Any, List
import pyautogui
from xpinyin import Pinyin
from common.id_generator import next_id
from devtools.base.network import network_enable
from devtools.input.wheel.wheel import Direction, get_scroll_point
from devtools.script.selector import get_element_position_by_css, get_element_position_by_xpath, \
    js_get_element_by_xpath, js_get_all_child_element_by_xpath, js_get_first_child_element_by_xpath, \
    js_get_last_child_element_by_xpath, js_get_next_sibling_element_by_xpath, \
    js_get_previous_sibling_element_by_xpath, js_get_parent_element_by_xpath, js_get_parent_element_by_css, \
    js_get_previous_sibling_element_by_css, js_get_next_sibling_element_by_css, js_get_last_child_element_by_css, \
    js_get_first_child_element_by_css, js_get_all_child_element_by_css, js_get_element_by_css, get_random_coordinates


class Page:
    def __init__(self):
        # Private attributes
        self._url = None  # URL of the page
        self._title = None  # Title of the page
        self._type = None  # Type of the page
        self._target_id = None  # Target ID related to the page
        self._session = None  # Session information related to the page
        self._port = None  # Port number associated with the page

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def target_id(self):
        return self._target_id

    @target_id.setter
    def target_id(self, value):
        self._target_id = value

    """
        导航到指定网址
    """

    async def page_enable(self):
        message = {
            "id": next_id(),
            "method": "Page.enable",
            "params": {}
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)

    async def page_disable(self):
        message = {
            "id": next_id(),
            "method": "Page.disable",
            "params": {}
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)

    async def navigate(self, url):
        message = {
            "id": next_id(),
            "method": "Page.navigate",
            "params": {
                "url": url,
            },
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)

    async def _response_body(self, requestId):
        id = next_id()
        message = {
            "id": id,
            "method": "Network.getResponseBody",
            "params": {
                "requestId": requestId
            }
        }
        excute = []

        async def callback_function(message):
            excute.append(message)

        self.session.register_callback(id, callback_function)
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)
        while True:
            if len(excute) > 0:
                self.session.remove_callback(id)
                return excute[0]
            await asyncio.sleep(0.1)
        self.session.remove_callback(id)
        return None

    async def set_touch_emulation_enabled(self, maxTouchPoints: int):
        id = next_id()
        message = {
            "id": id,
            "method": "Emulation.setTouchEmulationEnabled",
            "params": {
                "enabled": True,
                "maxTouchPoints": maxTouchPoints,
            }
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)

    async def dispatch_touch_event(self, touch_type: str, x: int, y: int, ):
        id = next_id()
        message = {
            "id": id,
            "method": "Input.dispatchTouchEvent",
            "params": {
                "type": touch_type,
                "touchPoints": [
                    {
                        "x": x,
                        "y": y,
                    }
                ]
            }
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)

    def touch(self, x, y):
        self.dispatch_touch_event("touchStart", x, y)
        time.sleep(random.uniform(0.001, 0.8))  # 随机等待时间在1到800毫秒之间
        self.dispatch_touch_event("touchEnd", x, y)

    def touch_drag(self, start_x, start_y, end_x, end_y):
        target_size = random.randint(1, 100)
        # Calculate the Fitts' Law index of difficulty
        a = abs(end_x - start_x)
        b = abs(end_y - start_y)
        d = math.sqrt(a * a + b * b)
        id = math.log2(d / target_size + 1)

        # Calculate the number of interpolation points
        n = int(id * 100)
        if n < 5:
            n = 5

        # Set up the control points of the multi-order Bezier curve
        dx = end_x - start_x
        dy = end_y - start_y
        x2 = end_x
        y2 = end_y
        c1x = start_x + dx * 0.1
        c1y = start_y + dy * 0.5
        c2x = start_x + dx * 0.3
        c2y = start_y + dy * 0.9

        # Generate the interpolation points using a cubic Bezier curve
        self.dispatch_touch_event("touchStart", start_x, start_y)
        for i in range(n + 1):
            t = i / float(n)
            if t < 0.5:
                t = 2 * t * t
            else:
                t = -2 * t * t + 4 * t - 1

            x = (1 - t) ** 3 * start_x + 3 * (1 - t) ** 2 * t * c1x + 3 * (1 - t) * t ** 2 * c2x + t ** 3 * x2
            y = (1 - t) ** 3 * start_y + 3 * (1 - t) ** 2 * t * c1y + 3 * (1 - t) * t ** 2 * c2y + t ** 3 * y2

            self.dispatch_touch_event("touchMove", x, y)
            time.sleep(random.uniform(0.001, 0.01))  # 随机等待时间在1到10毫秒之间

        self.dispatch_touch_event("touchEnd", end_x, end_y)

    async def upload_file(self, file_path: str):
        await asyncio.sleep(2)
        pyautogui.write(file_path)
        pyautogui.press('enter', 2)

    # async def _extract_frames(self, json_data):
    #     frames = []
    #     stack = []
    #     if 'result' in json_data and 'frameTree' in json_data['result']:
    #         stack.append(json_data['result']['frameTree'])
    #     else:
    #         return None
    #     while stack:
    #         frame_tree = stack.pop()
    #         frame = frame_tree.get('frame', None)
    #         if frame:
    #             frames.append(frame)
    #
    #         child_frames = frame_tree.get('childFrames', [])
    #         for child_frame in child_frames:
    #             stack.append(child_frame)
    #     return frames

    async def _attach_to_target(self, target_id):
        current_id = next_id()
        message = {
            "id": current_id,
            "method": "Target.attachToTarget",
            "params": {
                "targetId": target_id,
                "flatten": False
            }
        }
        if not self.session.is_connected():
            await self.session.connect()
        excute = []

        async def callback_function(result_message):
            excute.append(result_message)

        self.session.register_callback(current_id, callback_function)
        await self.session.send_message(message)
        while True:
            if len(excute) > 0:
                self.session.remove_callback(current_id)
                return excute[0]
            await asyncio.sleep(0.001)
        self.session.remove_callback(current_id)
        return None

    # async def get_frams(self):
    #     current_id = next_id()
    #     message = {
    #         "id": current_id,
    #         "method": "Page.getFrameTree",
    #     }
    #     if not self.session.is_connected():
    #         await self.session.connect()
    #     excute = []
    #
    #     async def callback_function(message):
    #         excute.append(message)
    #         print(message)
    #
    #     self.session.register_callback(current_id, callback_function)
    #     await self.session.send_message(message)
    #     while True:
    #         if len(excute) > 0:
    #             self.session.remove_callback(current_id)
    #             break
    #         await asyncio.sleep(0.001)
    #     self.session.remove_callback(current_id)
    #     ###解析iframe
    #     jr = await self._extract_frames(excute[0])
    #     if jr:
    #         for frame in reversed(jr):
    #             print("__________________________")
    #             print(frame)
    #             print(frame["id"])
    #             print(await self.get_document())
    #             print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", await self._attach_to_target(frame["id"]))
    #             print("$$$$$$$__________________________%%%%%%%%%")
    #             await asyncio.sleep(1)
    # print(">>>>===>>>", await self.get_element_position_by_css_on_page("body > input[type=text]"))

    # async def upload_files(self, selector: str, files: []):
    #     id = next_id()
    #     doc_node_id = self.get_document()
    #     node_id = self._query_selector(doc_node_id, selector)
    #     message = {
    #         "id": id,
    #         "method": "DOM.setFileInputFiles",
    #         "params": {
    #             "files": files,
    #             "nodeId": node_id,
    #         }
    #     }
    #     if not self.session.is_connected():
    #         await self.session.connect()
    #     await self.session.send_message(message)

    # async def _query_selector(self, node_id, selector):
    #     id = next_id()
    #     message = {
    #         "id": id,
    #         "method": "DOM.querySelector",
    #         "params": {
    #             "nodeId": node_id,
    #             "selector": selector,
    #         }
    #     }
    #     excute = []
    #
    #     async def callback_function(message):
    #         excute.append(message)
    #
    #     self.session.register_callback(id, callback_function)
    #     if not self.session.is_connected():
    #         await self.session.connect()
    #     await self.session.send_message(message)
    #     while True:
    #         if len(excute) > 0:
    #             self.session.remove_callback(id)
    #             return excute[0]
    #         await asyncio.sleep(0.1)
    #     self.session.remove_callback(id)
    #     return None

    async def set_cookie_by_url(self, key: str, value: str, url: str):
        id = next_id()
        message = {
            "id": id,
            "method": "Network.setCookie",
            "params": {
                "name": key,
                "value": value,
                "url": url,
            },
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)

    async def set_cookie_by_domain(self, key: str, value: str, domain: str):
        id = next_id()
        message = {
            "id": id,
            "method": "Network.setCookie",
            "params": {
                "name": key,
                "value": value,
                "domain": domain,
            },
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)

    async def get_cookies(self, urls: List[str]) -> Optional[Dict[str, Any]]:
        id = next_id()
        message = {
            "id": id,
            "method": "Network.getCookies",
            "params": {
                "urls": urls,
            },
        }
        excute = []

        async def callback_function(message):
            excute.append(message)

        self.session.register_callback(id, callback_function)
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)
        while True:
            if len(excute) > 0:
                self.session.remove_callback(id)
                return excute[0]
            await asyncio.sleep(0.1)
        self.session.remove_callback(id)
        return None

    """
    拦截所有的请求&返回
    """

    async def request_response(self, callback):
        if not self.session.is_connected():
            await self.session.connect()

        request_response = {}  # 创建一个空字典

        async def callback_request(message):
            key = message["params"]["requestId"]
            value = message["params"]
            request_response[key] = value

        async def callback_response(message):
            requestId = message["params"]["requestId"]
            response_data = message["params"]
            if request_response[requestId]:
                # 说明找到了匹配的request 和 response
                result = await self._response_body(requestId)
                await callback(request_response[requestId], response_data, result)

        self.session.register_callback("Network.requestWillBeSent", callback_request)
        self.session.register_callback("Network.responseReceived", callback_response)
        await network_enable(self.session)

    async def run_js_sync(self, js: str):
        id = next_id()
        message = {
            "id": id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": js,
                "includeCommandLineAPI": False,
                "silent": True,
                "returnByValue": False,
                "generatePreview": True,
                "userGesture": True,
                "awaitPromise": False,
                "throwOnSideEffect": False,
                "disableBreaks": False,
                "replMode": False,
                "allowUnsafeEvalBlockedByCSP": True,
            }
        }
        if not self.session.is_connected():
            await self.session.connect()

        excute = []

        async def callback_function(message):
            excute.append(message)

        self.session.register_callback(id, callback_function)
        await self.session.send_message(message)

        while True:
            if len(excute) > 0:
                self.session.remove_callback(id)
                return excute[0]
            await asyncio.sleep(0.001)
        self.session.remove_callback(id)
        return None

    async def run_js(self, js: str):
        id = next_id()
        message = {
            "id": id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": js,
                "includeCommandLineAPI": False,
                "silent": True,
                "returnByValue": False,
                "generatePreview": True,
                "userGesture": True,
                "awaitPromise": False,
                "throwOnSideEffect": False,
                "disableBreaks": False,
                "replMode": False,
                "allowUnsafeEvalBlockedByCSP": True,
            }
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)

    #
    async def close(self):
        id = next_id()
        message = {
            "id": id,
            "method": "Page.close"
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)
        await asyncio.sleep(1)
        await self.session.close()

    async def get_document(self):
        id = next_id()
        message = {
            "id": id,
            "method": "DOM.getDocument",
            "params": {
                "depth": 1,
                "pierce": False
            }
        }
        if not self.session.is_connected():
            await self.session.connect()
        excute = []

        async def callback_function(message):
            excute.append(message)

        self.session.register_callback(id, callback_function)
        await self.session.send_message(message)

        while True:
            if len(excute) > 0:
                self.session.remove_callback(id)
                return excute[0]
            await asyncio.sleep(0.001)
        self.session.remove_callback(id)
        return None

    async def get_html(self):
        document = await self.get_document()
        nodeId = document["result"]["root"]["nodeId"]
        id = next_id()
        message = {
            "id": id,
            "method": "DOM.getOuterHTML",
            "params": {
                "nodeId": nodeId
            }
        }

        if not self.session.is_connected():
            await self.session.connect()
        excute = []

        async def callback_function(message):
            excute.append(message)

        self.session.register_callback(id, callback_function)
        await self.session.send_message(message)

        while True:
            if len(excute) > 0:
                self.session.remove_callback(id)
                return excute[0]["result"]["outerHTML"]
            await asyncio.sleep(0.001)
        self.session.remove_callback(id)
        return None

    async def simulate_mouse_click(self, x, y):
        params = {
            "type": "mousePressed",
            "button": "left",
            "clickCount": 1,
            "x": x,
            "y": y
        }
        message = {
            "id": next_id(),
            "method": "Input.dispatchMouseEvent",
            "params": params
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)
        time.sleep(random.randint(1, 50) / 1000)
        params = {
            "type": "mouseReleased",
            "button": "left",
            "clickCount": 1,
            "x": x,
            "y": y
        }
        message = {
            "id": next_id(),
            "method": "Input.dispatchMouseEvent",
            "params": params
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)

    async def _mouse_wheel(self, x, y, delta_x, delta_y):
        params = {
            "type": "mouseWheel",
            "x": x,
            "y": y,
            "deltaX": delta_x,
            "deltaY": delta_y,
        }
        message = {
            "id": next_id(),
            "method": "Input.dispatchMouseEvent",
            "params": params,
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)

    async def simulate_enter_key(self):
        key_params_down = {
            "type": "keyDown",
            "key": "Enter",
        }
        await self._dispatch_key_event(key_params_down)
        key_params_char = {
            "type": "char",
            "key": "Enter",
            "unmodifiedText": "\r",
            "text": "\r",
        }
        await self._dispatch_key_event(key_params_char)
        key_params_up = {
            "type": "keyUp",
            "key": "Enter",
        }
        await self._dispatch_key_event(key_params_up)

    async def simulate_backspace_key(self):
        key_params_down = {
            "type": "keyDown",
            "key": "Backspace",
            "windowsVirtualKeyCode": 8,
            "nativeVirtualKeyCode": 8
        }
        await self._dispatch_key_event(key_params_down)
        key_params_up = {
            "type": "keyUp",
            "key": "Backspace",
            "windowsVirtualKeyCode": 8,
            "nativeVirtualKeyCode": 8
        }
        await self._dispatch_key_event(key_params_up)

    async def simulate_mouse_scroll(self, x, y, total_distance, direction):
        if direction == Direction.DOWN:
            points = get_scroll_point(total_distance, True)
        if direction == Direction.UP:
            points = get_scroll_point(total_distance, False)

        for point in points:
            await self._mouse_wheel(x, y, 0, point.distance)
            time.sleep(2 * math.sqrt(point.duration) * 0.001)

    async def _dispatch_mouse_event(self, params):
        message = {
            "id": next_id(),
            "method": "Input.dispatchMouseEvent",
            "params": params
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)

    async def simulate_mouse_move_to_target(self, end_x, end_y):
        pass
        js_result = await self.run_js_sync(get_random_coordinates())
        try:
            if js_result["result"]["result"]["value"]:
                r = json.loads(js_result["result"]["result"]["value"])
                x = r["x"]
                y = r["y"]
                await self.simulate_move_mouse(int(x), int(y), int(end_x), int(end_y))
        except Exception as e:
            print(" No such element found", e)

    async def simulate_move_mouse(self, start_x: int, start_y: int, end_x: int, end_y: int):
        # Generate a random target size
        target_size = random.randint(1, 100)

        # Calculate the Fitts' Law index of difficulty
        a = abs(end_x - start_x)
        b = abs(end_y - start_y)
        d = math.sqrt(a * a + b * b)
        id_value = math.log2(d / target_size + 1)

        # Calculate the number of interpolation points
        n = int(id_value * 10)
        if n < 5:
            n = 5

        # Set up the control points of the multi-order Bezier curve
        dx = end_x - start_x
        dy = end_y - start_y
        x2 = end_x
        y2 = end_y
        c1x = start_x + dx * 0.1
        c1y = start_y + dy * 0.5
        c2x = start_x + dx * 0.3
        c2y = start_y + dy * 0.9

        # Generate the interpolation points using a cubic Bezier curve
        points = []
        for i in range(n + 1):
            t = i / n
            if t < 0.5:
                t = 2 * t * t
            else:
                t = -2 * t * t + 4 * t - 1
            x = (1 - t) * (1 - t) * (1 - t) * start_x + 3 * (1 - t) * (1 - t) * t * c1x + 3 * (
                    1 - t) * t * t * c2x + t * t * t * x2
            y = (1 - t) * (1 - t) * (1 - t) * start_y + 3 * (1 - t) * (1 - t) * t * c1y + 3 * (
                    1 - t) * t * t * c2y + t * t * t * y2
            points.append({"type": "mouseMoved", "x": x, "y": y, "button": "none"})

        # Send the interpolation points using input.dispatchMouseEvent
        for point in points:
            await self._dispatch_mouse_event(point)
            time.sleep(0.01 * math.sqrt(n / id_value))

    async def _dispatch_key_event(self, params):
        message = {
            "id": next_id(),
            "method": "Input.dispatchKeyEvent",
            "params": params
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)

    async def simulate_keyboard_input(self, text):
        for item_char in text:
            time.sleep(random.uniform(0.01, 0.1))
            for char in ''.join(Pinyin().get_pinyin(item_char)):
                key_params_down = {
                    "type": "keyDown",
                    "key": char
                }
                await self._dispatch_key_event(key_params_down)

                key_params_char = {
                    "type": "char",
                    "key": char
                }
                await self._dispatch_key_event(key_params_char)

                key_params_up = {
                    "type": "keyUp",
                    "key": char
                }
                await self._dispatch_key_event(key_params_up)
            key_params_down = {
                "type": "keyDown",
                "key": " "
            }
            await self._dispatch_key_event(key_params_down)

            key_params_char = {
                "type": "char",
                "key": " "
            }
            await self._dispatch_key_event(key_params_char)

            key_params_up = {
                "type": "keyUp",
                "key": " "
            }
            await self._dispatch_key_event(key_params_up)

            key_params_down = {
                "type": "keyDown",
            }
            await self._dispatch_key_event(key_params_down)
            key_params_char = {
                "type": "char",
                "text": item_char
            }
            await self._dispatch_key_event(key_params_char)

            key_params_up = {
                "type": "keyUp",
            }
            await self._dispatch_key_event(key_params_up)

        # 先写选择器吧.
        # 先写选择器吧.

    async def get_element_position_by_css_on_page(self, selector):
        js_result = await self.run_js_sync(get_element_position_by_css(selector))
        try:
            ok = bool(js_result["result"]["result"]["preview"]["properties"][0]["value"])
            if ok:
                try:
                    top = float(js_result["result"]["result"]["preview"]["properties"][1]["value"])
                    left = float(js_result["result"]["result"]["preview"]["properties"][2]["value"])
                    width = float(js_result["result"]["result"]["preview"]["properties"][3]["value"])
                    height = float(js_result["result"]["result"]["preview"]["properties"][4]["value"])
                    result_position = get_random_point(top, left, width, height)
                    return {
                        'x': result_position[0],
                        'y': result_position[1],
                    }
                except (KeyError, ValueError) as e:
                    print(" No such element found", e)
                return None
        except Exception as e:
            print(" No such element found", e)
        return None

        # 先写选择器吧.

    async def get_element_position_by_xpath_on_page(self, selector):
        js_result = await self.run_js_sync(get_element_position_by_xpath(selector))
        try:
            ok = bool(js_result["result"]["result"]["preview"]["properties"][0]["value"])
            if ok:
                try:
                    top = float(js_result["result"]["result"]["preview"]["properties"][1]["value"])
                    left = float(js_result["result"]["result"]["preview"]["properties"][2]["value"])
                    width = float(js_result["result"]["result"]["preview"]["properties"][3]["value"])
                    height = float(js_result["result"]["result"]["preview"]["properties"][4]["value"])
                    result_position = get_random_point(top, left, width, height)
                    return {
                        'x': result_position[0],
                        'y': result_position[1],
                    }
                except (KeyError, ValueError) as e:
                    print(" No such element found", e)
                return None
        except Exception as e:
            print(" No such element found", e)
        return None

        # 先写选择器吧.

    async def get_element_by_xpath(self, selector):
        js_result = await self.run_js_sync(js_get_element_by_xpath(selector))
        try:
            item = json.loads(js_result["result"]["result"]["value"])
            if 'nodeType' in item:
                return {
                    'NodeType': item['nodeType'],
                    'NodeName': item['nodeName'],
                    'NodeValue': item['nodeValue'],
                    'TextContent': item['textContent'],
                    'HTMLContent': item['htmlContent'],
                    'CSSSelector': item['cssSelector'],
                    'XPathSelector': item['xpathSelector']
                }

        except Exception as e:
            print("No such element found", e)
        return None

        # 先写选择器吧.

    async def get_all_child_element_by_xpath(self, selector):
        js_result = await self.run_js_sync(js_get_all_child_element_by_xpath(selector))
        try:
            result_str = js_result["result"]["result"]["value"]
            array = json.loads(result_str)
            nodes = []
            for item in array:
                if 'nodeType' in item:
                    nodes.append({
                        'NodeType': item['nodeType'],
                        'NodeName': item['nodeName'],
                        'NodeValue': item['nodeValue'],
                        'TextContent': item['textContent'],
                        'HTMLContent': item['htmlContent'],
                        'CSSSelector': item['cssSelector'],
                        'XPathSelector': item['xpathSelector']
                    })
            return nodes
        except Exception as e:
            print(" No such element found", e)
        return None

    async def get_first_child_element_by_xpath(self, selector):
        js_result = await self.run_js_sync(js_get_first_child_element_by_xpath(selector))
        try:
            item = json.loads(js_result["result"]["result"]["value"])
            if 'nodeType' in item:
                return {
                    'NodeType': item['nodeType'],
                    'NodeName': item['nodeName'],
                    'NodeValue': item['nodeValue'],
                    'TextContent': item['textContent'],
                    'HTMLContent': item['htmlContent'],
                    'CSSSelector': item['cssSelector'],
                    'XPathSelector': item['xpathSelector']
                }

        except Exception as e:
            print("No such element found", e)
        return None

    async def get_last_child_element_by_xpath(self, selector):
        js_result = await self.run_js_sync(js_get_last_child_element_by_xpath(selector))
        try:
            item = json.loads(js_result["result"]["result"]["value"])
            if 'nodeType' in item:
                return {
                    'NodeType': item['nodeType'],
                    'NodeName': item['nodeName'],
                    'NodeValue': item['nodeValue'],
                    'TextContent': item['textContent'],
                    'HTMLContent': item['htmlContent'],
                    'CSSSelector': item['cssSelector'],
                    'XPathSelector': item['xpathSelector']
                }

        except Exception as e:
            print("No such element found", e)
        return None

    async def get_next_sibling_element_by_xpath(self, selector):
        js_result = await self.run_js_sync(js_get_next_sibling_element_by_xpath(selector))
        try:
            item = json.loads(js_result["result"]["result"]["value"])
            if 'nodeType' in item:
                return {
                    'NodeType': item['nodeType'],
                    'NodeName': item['nodeName'],
                    'NodeValue': item['nodeValue'],
                    'TextContent': item['textContent'],
                    'HTMLContent': item['htmlContent'],
                    'CSSSelector': item['cssSelector'],
                    'XPathSelector': item['xpathSelector']
                }

        except Exception as e:
            print("No such element found", e)
        return None

    async def get_previous_sibling_element_by_xpath(self, selector):
        js_result = await self.run_js_sync(js_get_previous_sibling_element_by_xpath(selector))
        try:
            item = json.loads(js_result["result"]["result"]["value"])
            if 'nodeType' in item:
                return {
                    'NodeType': item['nodeType'],
                    'NodeName': item['nodeName'],
                    'NodeValue': item['nodeValue'],
                    'TextContent': item['textContent'],
                    'HTMLContent': item['htmlContent'],
                    'CSSSelector': item['cssSelector'],
                    'XPathSelector': item['xpathSelector']
                }

        except Exception as e:
            print("No such element found", e)
        return None

    async def get_parent_element_by_xpath(self, selector):
        js_result = await self.run_js_sync(js_get_parent_element_by_xpath(selector))
        try:
            item = json.loads(js_result["result"]["result"]["value"])
            if 'nodeType' in item:
                return {
                    'NodeType': item['nodeType'],
                    'NodeName': item['nodeName'],
                    'NodeValue': item['nodeValue'],
                    'TextContent': item['textContent'],
                    'HTMLContent': item['htmlContent'],
                    'CSSSelector': item['cssSelector'],
                    'XPathSelector': item['xpathSelector']
                }

        except Exception as e:
            print("No such element found", e)
        return None

        # =========css
        # 先写选择器吧.

    async def get_element_by_css(self, selector):
        js_result = await self.run_js_sync(js_get_element_by_css(selector))
        try:
            item = json.loads(js_result["result"]["result"]["value"])
            if 'nodeType' in item:
                return {
                    'NodeType': item['nodeType'],
                    'NodeName': item['nodeName'],
                    'NodeValue': item['nodeValue'],
                    'TextContent': item['textContent'],
                    'HTMLContent': item['htmlContent'],
                    'CSSSelector': item['cssSelector'],
                    'XPathSelector': item['xpathSelector']
                }

        except Exception as e:
            print("No such element found", e)
        return None

        # 先写选择器吧.

    async def get_all_child_element_by_css(self, selector):
        js_result = await self.run_js_sync(js_get_all_child_element_by_css(selector))
        try:
            result_str = js_result["result"]["result"]["value"]
            array = json.loads(result_str)
            nodes = []
            for item in array:
                if 'nodeType' in item:
                    nodes.append({
                        'NodeType': item['nodeType'],
                        'NodeName': item['nodeName'],
                        'NodeValue': item['nodeValue'],
                        'TextContent': item['textContent'],
                        'HTMLContent': item['htmlContent'],
                        'CSSSelector': item['cssSelector'],
                        'XPathSelector': item['xpathSelector']
                    })
            return nodes
        except Exception as e:
            print(" No such element found", e)
        return None

    async def get_first_child_element_by_css(self, selector):
        js_result = await self.run_js_sync(js_get_first_child_element_by_css(selector))
        try:
            item = json.loads(js_result["result"]["result"]["value"])
            if 'nodeType' in item:
                return {
                    'NodeType': item['nodeType'],
                    'NodeName': item['nodeName'],
                    'NodeValue': item['nodeValue'],
                    'TextContent': item['textContent'],
                    'HTMLContent': item['htmlContent'],
                    'CSSSelector': item['cssSelector'],
                    'XPathSelector': item['xpathSelector']
                }

        except Exception as e:
            print("No such element found", e)
        return None

    async def get_last_child_element_by_css(self, selector) -> Optional[Dict[str, Any]]:
        """
        通过CSS选择器获取最后一个子元素。

        使用JavaScript执行同步函数来获取匹配选择器的最后一个子元素，然后解析返回的结果。
        如果找到匹配的元素，返回包含其节点类型、节点名称、节点值、文本内容、HTML内容、CSS选择器和XPath选择器的字典。
        如果未找到匹配元素或解析出错，返回None。

        :param selector: CSS选择器字符串，用于定位要操作的元素。
        :return: 包含元素信息的字典或None，如果未找到匹配的元素或解析出错。
        Retrieve the last child element using a CSS selector.

        Executes a synchronous JavaScript function to fetch the last child element
        matching the selector, then parses the returned result. Returns a dictionary
        containing node type, node name, node value, text content, HTML content,
        CSS selector, and XPath selector of the element if found. Returns None if
        no matching element is found or if parsing fails.

        :param selector: CSS selector string to locate the element to operate on.
        :return: A dictionary containing element information or None if no matching
                 element is found or parsing fails.
        """
        js_result = await self.run_js_sync(js_get_last_child_element_by_css(selector))
        try:
            item = json.loads(js_result["result"]["result"]["value"])
            if 'nodeType' in item:
                return {
                    'NodeType': item['nodeType'],
                    'NodeName': item['nodeName'],
                    'NodeValue': item['nodeValue'],
                    'TextContent': item['textContent'],
                    'HTMLContent': item['htmlContent'],
                    'CSSSelector': item['cssSelector'],
                    'XPathSelector': item['xpathSelector']
                }

        except Exception as e:
            print("No such element found", e)
        return None

    async def get_next_sibling_element_by_css(self, selector) -> Optional[Dict[str, Any]]:
        """
          通过CSS选择器获取下一个兄弟元素。

          使用JavaScript执行同步函数来获取下一个兄弟元素，然后解析返回的结果。
          如果找到匹配的元素，返回包含其节点类型、节点名称、节点值、文本内容、HTML内容、CSS选择器和XPath选择器的字典。
          如果未找到匹配元素或解析出错，返回None。

          :param selector: CSS选择器字符串，用于定位要操作的元素。
          :return: 包含元素信息的字典或None，如果未找到匹配的元素或解析出错。

         Retrieve the next sibling element using a CSS selector.

         Executes a synchronous JavaScript function to fetch the next sibling element,
         then parses the returned result. Returns a dictionary containing node type,
         node name, node value, text content, HTML content, CSS selector, and XPath selector
         of the element if found. Returns None if no matching element is found or if parsing fails.

         :param selector: CSS selector string to locate the element to operate on.
         :return: A dictionary containing element information or None if no matching element is found or parsing fails.
        """
        js_result = await self.run_js_sync(js_get_next_sibling_element_by_css(selector))
        try:
            item = json.loads(js_result["result"]["result"]["value"])
            if 'nodeType' in item:
                return {
                    'NodeType': item['nodeType'],
                    'NodeName': item['nodeName'],
                    'NodeValue': item['nodeValue'],
                    'TextContent': item['textContent'],
                    'HTMLContent': item['htmlContent'],
                    'CSSSelector': item['cssSelector'],
                    'XPathSelector': item['xpathSelector']
                }
        except Exception as e:
            print("No such element found", e)
        return None

    async def get_previous_sibling_element_by_css(self, selector) -> Optional[Dict[str, Any]]:
        """
            Get the previous sibling element by CSS selector.

            Executes a synchronous JavaScript function to retrieve the previous sibling element,
            then parses the returned result. Returns a dictionary containing node type, node name,
            node value, text content, HTML content, CSS selector, and XPath selector of the element
            if found. Returns None if no matching element is found or if parsing fails.

            :param selector: CSS selector string to locate the element to operate on.
            :return: A dictionary containing element information or None if no matching element
                     is found or parsing fails.
            通过CSS选择器获取前一个兄弟元素。

            使用JavaScript执行同步函数来获取前一个兄弟元素，然后解析返回的结果。
            如果找到匹配的元素，返回包含其节点类型、节点名称、节点值、文本内容、HTML内容、CSS选择器和XPath选择器的字典。
            如果未找到匹配元素或解析出错，返回None。

            :param selector: CSS选择器字符串，用于定位要操作的元素。
            :return: 包含元素信息的字典或None，如果未找到匹配的元素或解析出错。
        """
        js_result = await self.run_js_sync(js_get_previous_sibling_element_by_css(selector))
        try:
            item = json.loads(js_result["result"]["result"]["value"])
            if 'nodeType' in item:
                return {
                    'NodeType': item['nodeType'],
                    'NodeName': item['nodeName'],
                    'NodeValue': item['nodeValue'],
                    'TextContent': item['textContent'],
                    'HTMLContent': item['htmlContent'],
                    'CSSSelector': item['cssSelector'],
                    'XPathSelector': item['xpathSelector']
                }

        except Exception as e:
            print("No such element found", e)
        return None

    async def get_parent_element_by_css(self, selector) -> Optional[Dict[str, Any]]:
        """
                根据 CSS 选择器获取父元素的信息。

                1. 调用 run_js_sync 方法执行 JavaScript 代码，获取父元素信息。
                2. 使用 try-except 块解析返回的 JSON 结果。
                3. 如果元素存在，返回包含元素详细信息的字典。
                4. 如果发生异常（例如元素不存在），打印错误信息，并返回 None。

                1. Call the run_js_sync method to execute JavaScript code and get the parent element information.
                2. Use a try-except block to parse the returned JSON result.
                3. If the element exists, return a dictionary containing detailed information about the element.
                4. If an exception occurs (e.g., the element does not exist), print an error message and return None.

                :param selector: The CSS selector used to identify the element.
                :return: A dictionary with element details if found, otherwise None.
        """
        js_result = await self.run_js_sync(js_get_parent_element_by_css(selector))
        try:
            item = json.loads(js_result["result"]["result"]["value"])
            if 'nodeType' in item:
                return {
                    'NodeType': item['nodeType'],
                    'NodeName': item['nodeName'],
                    'NodeValue': item['nodeValue'],
                    'TextContent': item['textContent'],
                    'HTMLContent': item['htmlContent'],
                    'CSSSelector': item['cssSelector'],
                    'XPathSelector': item['xpathSelector']
                }

        except Exception as e:
            print("No such element found", e)
        return None


def get_random_point(top, left, width, height):
    def split_segment(min_x, max_x, segments):
        segment_length = (max_x - min_x) / segments
        middle_segment_min_x = min_x + segment_length
        middle_segment_max_x = middle_segment_min_x + segment_length
        return middle_segment_min_x, middle_segment_max_x

    def random_in_range(min_val, max_val):
        random.seed(time.time())
        return min_val + random.random() * (max_val - min_val)

    middle_segment_min_x, middle_segment_max_x = split_segment(left, left + width, 3)
    middle_segment_min_y, middle_segment_max_y = split_segment(top, top + height, 3)

    random_x = random_in_range(middle_segment_min_x + 1, middle_segment_max_x - 1)
    random_y = random_in_range(middle_segment_min_y + 1, middle_segment_max_y - 1)
    return random_x, random_y
