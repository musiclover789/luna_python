def get_element_position_by_css(selector):
    return f'''
    function getElementViewportCoordinates(selector) {{
        const element = document.querySelector('{selector}');

        if (!element) {{
            return {{ ok: false }};
        }}
        const rect = element.getBoundingClientRect();
        return {{
            ok: true,
            top: rect.top,
            left: rect.left,
            width: rect.width,
            height: rect.height
        }};
    }}

getElementViewportCoordinates('{selector}')
'''


#########################################################################

#########################################################################
def get_element_position_by_xpath(selector):
    js_code = f'''
function getElementByXpath(path) {{
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}}

function getElementViewportCoordinatesByXpath(xpath) {{
    const element = getElementByXpath(xpath);

    if (!element) {{
        return {{ ok: false }};
    }}

    const rect = element.getBoundingClientRect();

    return {{
        ok: true,
        top: rect.top,
        left: rect.left,
        width: rect.width,
        height: rect.height
    }};
}}

// 调用函数并传递变量 selector，确保在两侧加上单引号
getElementViewportCoordinatesByXpath('{selector}');
'''
    return js_code


#########################################################################
######## xpath ########
#########################################################################

def js_get_element_by_xpath(selector):
    js_code = f'''
function getNodeInfo(selector) {{
    const element = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (!element) {{
        return null;
    }} else {{
        const nodeInfo = {{
            nodeType: element.nodeType,
            nodeName: element.nodeName,
            nodeValue: element.nodeValue,
            textContent: element.textContent,
            htmlContent: element.outerHTML,
            cssSelector: getCssSelector(element),
            xpathSelector: getXpathSelector(element)
        }};
        return JSON.stringify(nodeInfo, null, 2);
    }}
}}

function getCssSelector(element) {{
    if (!(element instanceof Element)) return;
    const selectorList = [];
    while (element.parentElement) {{
        let selector = element.tagName.toLowerCase();
         let siblings = Array.from(element.parentElement.children);
            let index = siblings.findIndex(sibling => sibling === element);
            selector += ':nth-child(' + (index + 1) + ')';
            selectorList.unshift(selector);
            element = element.parentElement;
    }}
    return selectorList.join(' > ');
}}

// 函数：获取元素的XPath
function getXpathSelector(element) {{
    if (element.id !== "")
        return 'id("' + element.id + '")';
    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {{
        var sibling = siblings[i];
        if (sibling === element)
            return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }}
}}

getNodeInfo('{selector}'); // 选择的CSS选择器
'''
    return js_code


#########################################################################

#########################################################################

def js_get_all_child_element_by_xpath(selector):
    js_code = f'''
function getAllChildNodesInfo(selector) {{
    const element = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (!element) {{
        return null;
    }} else {{
        const childNodes = Array.from(element.children).map(child => getNodeInfo(child));
        return JSON.stringify(childNodes, null, 2);
    }}
}}

function getNodeInfo(node) {{
    const nodeInfo = {{
        nodeType: node.nodeType,
        nodeName: node.nodeName,
        nodeValue: node.nodeValue,
        textContent: node.textContent,
        htmlContent: node.outerHTML,
        cssSelector: getCssSelector(node),
        xpathSelector: getXpathSelector(node)
    }};
    return nodeInfo;
}}

function getCssSelector(element) {{
    if (!(element instanceof Element)) return;
    const selectorList = [];
    while (element.parentElement) {{
        let selector = element.tagName.toLowerCase();
        let siblings = Array.from(element.parentElement.children);
        let index = siblings.findIndex(sibling => sibling === element);
        selector += ':nth-child(' + (index + 1) + ')';
        selectorList.unshift(selector);
        element = element.parentElement;
    }}
    return selectorList.join(' > ');
}}

// 函数：获取元素的XPath
function getXpathSelector(element) {{
    if (element.id !== "")
        return 'id("' + element.id + '")';
    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {{
        var sibling = siblings[i];
        if (sibling === element)
            return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }}
}}

getAllChildNodesInfo('{selector}');
'''
    return js_code


#########################################################################

#########################################################################


def js_get_first_child_element_by_xpath(selector):
    return f'''
function getCssSelector(element) {{
    if (!(element instanceof Element)) return;
    const selectorList = [];
    while (element.parentElement) {{
        let selector = element.tagName.toLowerCase();
        let siblings = Array.from(element.parentElement.children);
        let index = siblings.findIndex(sibling => sibling === element);
        selector += ':nth-child(' + (index + 1) + ')';
        selectorList.unshift(selector);
        element = element.parentElement;
    }}
    return selectorList.join(' > ');
}}

// 函数：获取元素的XPath
function getXpathSelector(element) {{
    if (element.id !== "")
        return 'id("' + element.id + '")';
    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {{
        var sibling = siblings[i];
        if (sibling === element)
            return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }}
}}

function getFirstChildNodeInfo(selector) {{
    const parentElement = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;;
    if (parentElement) {{
        const firstChildNode = parentElement.firstElementChild;
        if (firstChildNode) {{
            const nodeInfo = {{
                nodeType: firstChildNode.nodeType,
                nodeName: firstChildNode.nodeName,
                nodeValue: firstChildNode.nodeValue,
                textContent: firstChildNode.textContent,
                htmlContent: firstChildNode.outerHTML,
                cssSelector: getCssSelector(firstChildNode),
                xpathSelector: getXpathSelector(firstChildNode)
            }};
            return JSON.stringify(nodeInfo, null, 2);
        }} else {{
            return null;
        }}
    }} else {{
        return null;
    }}
}}

getFirstChildNodeInfo('{selector}')
'''


#########################################################################

#########################################################################


def js_get_last_child_element_by_xpath(selector):
    return '''
function getCssSelector(element) {{
    if (!(element instanceof Element)) return;
    const selectorList = [];
    while (element.parentElement) {{
        let selector = element.tagName.toLowerCase();
        let siblings = Array.from(element.parentElement.children);
        let index = siblings.findIndex(sibling => sibling === element);
        selector += ':nth-child(' + (index + 1) + ')';
        selectorList.unshift(selector);
        element = element.parentElement;
    }}
    return selectorList.join(' > ');
}}

function getXpathSelector(element) {{
    if (element.id !== "")
        return 'id("' + element.id + '")';
    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {{
        var sibling = siblings[i];
        if (sibling === element)
            return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }}
}}

function getLastChildNodeInfo(selector) {{
    const parentElement = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (parentElement) {{
        const lastChildNode = parentElement.lastElementChild;
        if (lastChildNode) {{
            const nodeInfo = {{
                nodeType: lastChildNode.nodeType,
                nodeName: lastChildNode.nodeName,
                nodeValue: lastChildNode.nodeValue,
                textContent: lastChildNode.textContent,
                htmlContent: lastChildNode.outerHTML,
                cssSelector: getCssSelector(lastChildNode),
                xpathSelector: getXpathSelector(lastChildNode)
            }};
            return JSON.stringify(nodeInfo, null, 2);
        }} else {{
            return null;
        }}
    }} else {{
        return null;
    }}
}}
getLastChildNodeInfo('{}');
'''.format(selector)


#########################################################################

#########################################################################

def js_get_next_sibling_element_by_xpath(selector):
    return '''
function getCssSelector(element) {{
    if (!(element instanceof Element)) return;
    const selectorList = [];
    while (element.parentElement) {{
        let selector = element.tagName.toLowerCase();
        let siblings = Array.from(element.parentElement.children);
        let index = siblings.findIndex(sibling => sibling === element);
        selector += ':nth-child(' + (index + 1) + ')';
        selectorList.unshift(selector);
        element = element.parentElement;
    }}
    return selectorList.join(' > ');
}}

function getXpathSelector(element) {{
    if (element.id !== "")
        return 'id("' + element.id + '")';
    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {{
        var sibling = siblings[i];
        if (sibling === element)
            return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }}
}}

function getNextSiblingNodeInfo(selector) {{
    const currentNode = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (currentNode) {{
        const nextSiblingNode = currentNode.nextElementSibling;
        if (nextSiblingNode) {{
            const nodeInfo = {{
                nodeType: nextSiblingNode.nodeType,
                nodeName: nextSiblingNode.nodeName,
                nodeValue: nextSiblingNode.nodeValue,
                textContent: nextSiblingNode.textContent,
                htmlContent: nextSiblingNode.outerHTML,
                cssSelector: getCssSelector(nextSiblingNode),
                xpathSelector: getXpathSelector(nextSiblingNode)
            }};
            return JSON.stringify(nodeInfo, null, 2);
        }} else {{
            return null;
        }}
    }} else {{
        return null;
    }}
}}

getNextSiblingNodeInfo('{}');
'''.format(selector)


#########################################################################

#########################################################################
def js_get_previous_sibling_element_by_xpath(selector):
    return '''
function getCssSelector(element) {{
    if (!(element instanceof Element)) return;
    const selectorList = [];
    while (element.parentElement) {{
        let selector = element.tagName.toLowerCase();
       let siblings = Array.from(element.parentElement.children);
            let index = siblings.findIndex(sibling => sibling === element);
            selector += ':nth-child(' + (index + 1) + ')';
            selectorList.unshift(selector);
            element = element.parentElement;
    }}
    return selectorList.join(' > ');
}}

// 函数：获取元素的XPath
function getXpathSelector(element) {{
    if (element.id !== "")
        return 'id("' + element.id + '")';
    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {{
        var sibling = siblings[i];
        if (sibling === element)
            return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }}
}}


function getPreviousSiblingNodeInfo(selector) {{
    const currentNode =  document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (currentNode) {{
        const previousSiblingNode = currentNode.previousElementSibling;
        if (previousSiblingNode) {{
            const nodeInfo = {{
                nodeType: previousSiblingNode.nodeType,
                nodeName: previousSiblingNode.nodeName,
                nodeValue: previousSiblingNode.nodeValue,
                textContent: previousSiblingNode.textContent,
                htmlContent: previousSiblingNode.outerHTML,
                cssSelector: getCssSelector(previousSiblingNode),
                xpathSelector: getXpathSelector(previousSiblingNode)
            }};
            return JSON.stringify(nodeInfo, null, 2);
        }} else {{
            return null;
        }}
    }} else {{
        return null;
    }}
}}

getPreviousSiblingNodeInfo('{}');
'''.format(selector)


#########################################################################

#########################################################################


def js_get_parent_element_by_xpath(selector):
    return '''
    function getCssSelector(element) {{
        if (!(element instanceof Element)) return;
        const selectorList = [];
        while (element.parentElement) {{
            let selector = element.tagName.toLowerCase();
            let siblings = Array.from(element.parentElement.children);
            let index = siblings.findIndex(sibling => sibling === element);
            selector += ':nth-child(' + (index + 1) + ')';
            selectorList.unshift(selector);
            element = element.parentElement;
        }}
        return selectorList.join(' > ');
    }}

    // 函数：获取元素的XPath
    function getXpathSelector(element) {{
        if (element.id !== "")
            return 'id("' + element.id + '")';
        if (element === document.body)
            return element.tagName;

        var ix = 0;
        var siblings = element.parentNode.childNodes;
        for (var i = 0; i < siblings.length; i++) {{
            var sibling = siblings[i];
            if (sibling === element)
                return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
                ix++;
        }}
    }}

    function getParentNodeInfo(selector) {{
        const currentNode = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (!currentNode) {{
             return null;
        }} else {{
            const parentNode = currentNode.parentNode;
            if (parentNode) {{
                const nodeInfo = {{
                    nodeType: parentNode.nodeType,
                    nodeName: parentNode.nodeName,
                    nodeValue: parentNode.nodeValue,
                    textContent: parentNode.textContent,
                    htmlContent: parentNode.outerHTML,
                    cssSelector: getCssSelector(parentNode),
                    xpathSelector: getXpathSelector(parentNode)
                }};
                return JSON.stringify(nodeInfo, null, 2);
            }} else {{
                return null;
            }}
        }}
    }}

    getParentNodeInfo('{}');
    '''.format(selector)


#########################################################################
###css
#########################################################################


def js_get_element_by_css(selector):
    js_code = f'''
function getNodeInfo(selector) {{
    const element =document.querySelector(selector); 
    if (!element) {{
        return null;
    }} else {{
        const nodeInfo = {{
            nodeType: element.nodeType,
            nodeName: element.nodeName,
            nodeValue: element.nodeValue,
            textContent: element.textContent,
            htmlContent: element.outerHTML,
            cssSelector: getCssSelector(element),
            xpathSelector: getXpathSelector(element)
        }};
        return JSON.stringify(nodeInfo, null, 2);
    }}
}}

function getCssSelector(element) {{
    if (!(element instanceof Element)) return;
    const selectorList = [];
    while (element.parentElement) {{
        let selector = element.tagName.toLowerCase();
         let siblings = Array.from(element.parentElement.children);
            let index = siblings.findIndex(sibling => sibling === element);
            selector += ':nth-child(' + (index + 1) + ')';
            selectorList.unshift(selector);
            element = element.parentElement;
    }}
    return selectorList.join(' > ');
}}

// 函数：获取元素的XPath
function getXpathSelector(element) {{
    if (element.id !== "")
        return 'id("' + element.id + '")';
    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {{
        var sibling = siblings[i];
        if (sibling === element)
            return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }}
}}

getNodeInfo('{selector}'); // 选择的CSS选择器
'''
    return js_code


#########################################################################

#########################################################################

def js_get_all_child_element_by_css(selector):
    js_code = f'''
function getAllChildNodesInfo(selector) {{
    const element =document.querySelector(selector); 
    if (!element) {{
        return null;
    }} else {{
        const childNodes = Array.from(element.children).map(child => getNodeInfo(child));
        return JSON.stringify(childNodes, null, 2);
    }}
}}

function getNodeInfo(node) {{
    const nodeInfo = {{
        nodeType: node.nodeType,
        nodeName: node.nodeName,
        nodeValue: node.nodeValue,
        textContent: node.textContent,
        htmlContent: node.outerHTML,
        cssSelector: getCssSelector(node),
        xpathSelector: getXpathSelector(node)
    }};
    return nodeInfo;
}}

function getCssSelector(element) {{
    if (!(element instanceof Element)) return;
    const selectorList = [];
    while (element.parentElement) {{
        let selector = element.tagName.toLowerCase();
        let siblings = Array.from(element.parentElement.children);
        let index = siblings.findIndex(sibling => sibling === element);
        selector += ':nth-child(' + (index + 1) + ')';
        selectorList.unshift(selector);
        element = element.parentElement;
    }}
    return selectorList.join(' > ');
}}

// 函数：获取元素的XPath
function getXpathSelector(element) {{
    if (element.id !== "")
        return 'id("' + element.id + '")';
    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {{
        var sibling = siblings[i];
        if (sibling === element)
            return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }}
}}

getAllChildNodesInfo('{selector}');
'''
    return js_code


#########################################################################

#########################################################################


def js_get_first_child_element_by_css(selector):
    return f'''
function getCssSelector(element) {{
    if (!(element instanceof Element)) return;
    const selectorList = [];
    while (element.parentElement) {{
        let selector = element.tagName.toLowerCase();
        let siblings = Array.from(element.parentElement.children);
        let index = siblings.findIndex(sibling => sibling === element);
        selector += ':nth-child(' + (index + 1) + ')';
        selectorList.unshift(selector);
        element = element.parentElement;
    }}
    return selectorList.join(' > ');
}}

// 函数：获取元素的XPath
function getXpathSelector(element) {{
    if (element.id !== "")
        return 'id("' + element.id + '")';
    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {{
        var sibling = siblings[i];
        if (sibling === element)
            return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }}
}}

function getFirstChildNodeInfo(selector) {{
    const parentElement =document.querySelector(selector); 
    if (parentElement) {{
        const firstChildNode = parentElement.firstElementChild;
        if (firstChildNode) {{
            const nodeInfo = {{
                nodeType: firstChildNode.nodeType,
                nodeName: firstChildNode.nodeName,
                nodeValue: firstChildNode.nodeValue,
                textContent: firstChildNode.textContent,
                htmlContent: firstChildNode.outerHTML,
                cssSelector: getCssSelector(firstChildNode),
                xpathSelector: getXpathSelector(firstChildNode)
            }};
            return JSON.stringify(nodeInfo, null, 2);
        }} else {{
            return null;
        }}
    }} else {{
        return null;
    }}
}}

getFirstChildNodeInfo('{selector}')
'''


#########################################################################

#########################################################################


def js_get_last_child_element_by_css(selector):
    return '''
function getCssSelector(element) {{
    if (!(element instanceof Element)) return;
    const selectorList = [];
    while (element.parentElement) {{
        let selector = element.tagName.toLowerCase();
        let siblings = Array.from(element.parentElement.children);
        let index = siblings.findIndex(sibling => sibling === element);
        selector += ':nth-child(' + (index + 1) + ')';
        selectorList.unshift(selector);
        element = element.parentElement;
    }}
    return selectorList.join(' > ');
}}

function getXpathSelector(element) {{
    if (element.id !== "")
        return 'id("' + element.id + '")';
    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {{
        var sibling = siblings[i];
        if (sibling === element)
            return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }}
}}

function getLastChildNodeInfo(selector) {{
    const parentElement = document.querySelector(selector); 
    if (parentElement) {{
        const lastChildNode = parentElement.lastElementChild;
        if (lastChildNode) {{
            const nodeInfo = {{
                nodeType: lastChildNode.nodeType,
                nodeName: lastChildNode.nodeName,
                nodeValue: lastChildNode.nodeValue,
                textContent: lastChildNode.textContent,
                htmlContent: lastChildNode.outerHTML,
                cssSelector: getCssSelector(lastChildNode),
                xpathSelector: getXpathSelector(lastChildNode)
            }};
            return JSON.stringify(nodeInfo, null, 2);
        }} else {{
            return null;
        }}
    }} else {{
        return null;
    }}
}}
getLastChildNodeInfo('{}');
'''.format(selector)


#########################################################################

#########################################################################

def js_get_next_sibling_element_by_css(selector):
    return '''
function getCssSelector(element) {{
    if (!(element instanceof Element)) return;
    const selectorList = [];
    while (element.parentElement) {{
        let selector = element.tagName.toLowerCase();
        let siblings = Array.from(element.parentElement.children);
        let index = siblings.findIndex(sibling => sibling === element);
        selector += ':nth-child(' + (index + 1) + ')';
        selectorList.unshift(selector);
        element = element.parentElement;
    }}
    return selectorList.join(' > ');
}}

function getXpathSelector(element) {{
    if (element.id !== "")
        return 'id("' + element.id + '")';
    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {{
        var sibling = siblings[i];
        if (sibling === element)
            return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }}
}}

function getNextSiblingNodeInfo(selector) {{
    const currentNode = document.querySelector(selector); 
    if (currentNode) {{
        const nextSiblingNode = currentNode.nextElementSibling;
        if (nextSiblingNode) {{
            const nodeInfo = {{
                nodeType: nextSiblingNode.nodeType,
                nodeName: nextSiblingNode.nodeName,
                nodeValue: nextSiblingNode.nodeValue,
                textContent: nextSiblingNode.textContent,
                htmlContent: nextSiblingNode.outerHTML,
                cssSelector: getCssSelector(nextSiblingNode),
                xpathSelector: getXpathSelector(nextSiblingNode)
            }};
            return JSON.stringify(nodeInfo, null, 2);
        }} else {{
            return null;
        }}
    }} else {{
        return null;
    }}
}}

getNextSiblingNodeInfo('{}');
'''.format(selector)


#########################################################################

#########################################################################
def js_get_previous_sibling_element_by_css(selector):
    return '''
function getCssSelector(element) {{
    if (!(element instanceof Element)) return;
    const selectorList = [];
    while (element.parentElement) {{
        let selector = element.tagName.toLowerCase();
       let siblings = Array.from(element.parentElement.children);
            let index = siblings.findIndex(sibling => sibling === element);
            selector += ':nth-child(' + (index + 1) + ')';
            selectorList.unshift(selector);
            element = element.parentElement;
    }}
    return selectorList.join(' > ');
}}

// 函数：获取元素的XPath
function getXpathSelector(element) {{
    if (element.id !== "")
        return 'id("' + element.id + '")';
    if (element === document.body)
        return element.tagName;

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {{
        var sibling = siblings[i];
        if (sibling === element)
            return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }}
}}


function getPreviousSiblingNodeInfo(selector) {{
    const currentNode = document.querySelector(selector); 
    if (currentNode) {{
        const previousSiblingNode = currentNode.previousElementSibling;
        if (previousSiblingNode) {{
            const nodeInfo = {{
                nodeType: previousSiblingNode.nodeType,
                nodeName: previousSiblingNode.nodeName,
                nodeValue: previousSiblingNode.nodeValue,
                textContent: previousSiblingNode.textContent,
                htmlContent: previousSiblingNode.outerHTML,
                cssSelector: getCssSelector(previousSiblingNode),
                xpathSelector: getXpathSelector(previousSiblingNode)
            }};
            return JSON.stringify(nodeInfo, null, 2);
        }} else {{
            return null;
        }}
    }} else {{
        return null;
    }}
}}

getPreviousSiblingNodeInfo('{}');
'''.format(selector)


#########################################################################

#########################################################################


def js_get_parent_element_by_css(selector):
    return '''
    function getCssSelector(element) {{
        if (!(element instanceof Element)) return;
        const selectorList = [];
        while (element.parentElement) {{
            let selector = element.tagName.toLowerCase();
            let siblings = Array.from(element.parentElement.children);
            let index = siblings.findIndex(sibling => sibling === element);
            selector += ':nth-child(' + (index + 1) + ')';
            selectorList.unshift(selector);
            element = element.parentElement;
        }}
        return selectorList.join(' > ');
    }}

    // 函数：获取元素的XPath
    function getXpathSelector(element) {{
        if (element.id !== "")
            return 'id("' + element.id + '")';
        if (element === document.body)
            return element.tagName;

        var ix = 0;
        var siblings = element.parentNode.childNodes;
        for (var i = 0; i < siblings.length; i++) {{
            var sibling = siblings[i];
            if (sibling === element)
                return getXpathSelector(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
                ix++;
        }}
    }}

    function getParentNodeInfo(selector) {{
        const currentNode =document.querySelector(selector); 
        if (!currentNode) {{
             return null;
        }} else {{
            const parentNode = currentNode.parentNode;
            if (parentNode) {{
                const nodeInfo = {{
                    nodeType: parentNode.nodeType,
                    nodeName: parentNode.nodeName,
                    nodeValue: parentNode.nodeValue,
                    textContent: parentNode.textContent,
                    htmlContent: parentNode.outerHTML,
                    cssSelector: getCssSelector(parentNode),
                    xpathSelector: getXpathSelector(parentNode)
                }};
                return JSON.stringify(nodeInfo, null, 2);
            }} else {{
                return null;
            }}
        }}
    }}

    getParentNodeInfo('{}');
    '''.format(selector)


#########################################################################

#########################################################################

def get_random_coordinates():
    return '''
	function getRandomCoordinates() {
		var windowWidth = window.innerWidth;
		var windowHeight = window.innerHeight;
		
		var randomX = Math.floor(Math.random() * windowWidth);
		var randomY = Math.floor(Math.random() * windowHeight);
    
		//return { x: randomX, y: randomY };
	   return JSON.stringify({
			x: randomX,
			y: randomY
		});
	}

	getRandomCoordinates();
'''
