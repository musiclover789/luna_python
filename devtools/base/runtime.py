# from common.id_generator import next_id
#
#
# async def evaluate_with_result_sync(devtools_conn, id, expression):
#     message = {
#         "id": id,
#         "method": "Runtime.evaluate",
#         "params": {
#             "expression": expression,
#             "includeCommandLineAPI": False,
#             "silent": True,
#             "returnByValue": False,
#             "generatePreview": True,
#             "userGesture": True,
#             "awaitPromise": False,
#             "throwOnSideEffect": False,
#             "disableBreaks": False,
#             "replMode": False,
#             "allowUnsafeEvalBlockedByCSP": True,
#         }
#     }
#     if not devtools_conn.is_connected():
#         await devtools_conn.connect()
#     await devtools_conn.send_message(message)
