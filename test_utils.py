import pytest
import allure
from functools import wraps
from selenium.common.exceptions import (
    WebDriverException,
    ElementNotInteractableException,
    NoSuchWindowException,
    InvalidSessionIdException
)
from typing import List, Type


def skip_broken_but_fail_on_assertion(
        exception_types: List[Type[Exception]] = None,
        attach_screenshot: bool = False
):
    """
    Decorator that:
    - Fails normally on assertion errors (test logic failures)
    - Skips on technical/Selenium failures

    Args:
        exception_types: List of exception types to treat as "broken" (default: Selenium exceptions)
        attach_screenshot: Whether to attach screenshot on technical failures
    """
    default_exceptions = (
        WebDriverException,
        TimeoutError,
        ConnectionError,
        ElementNotInteractableException,
        NoSuchWindowException,
        InvalidSessionIdException,
        UnicodeEncodeError
    )

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            driver = None
            for arg in args + tuple(kwargs.values()):
                if hasattr(arg, 'get') and hasattr(arg, 'current_url'):
                    driver = arg
                    break

            try:
                return func(*args, **kwargs)
            except AssertionError:
                raise  # Let assertion failures fail normally
            except tuple(exception_types or default_exceptions) as e:
                skip_msg = f"Skipped: Condition not met."
                allure.dynamic.description(f"Original error: {skip_msg}")

                if attach_screenshot and driver:
                    try:
                        screenshot = driver.get_screenshot_as_png()
                        allure.attach(
                            screenshot,
                            name=f"{func.__name__}-technical-failure",
                            attachment_type=allure.attachment_type.PNG
                        )
                    except Exception:
                        pass  # Ignore screenshot errors

                pytest.skip(skip_msg)

        return wrapper

    return decorator


# Shortcut decorator with default values
skip_broken = skip_broken_but_fail_on_assertion()




















# import pytest
# import allure
# from functools import wraps
# from selenium.common.exceptions import (
#     WebDriverException,
#     ElementNotInteractableException,
#     NoSuchWindowException,
#     InvalidSessionIdException
# )
# from typing import List, Type
#
#
# def pass_broken_but_fail_on_assertion(
#         exception_types: List[Type[Exception]] = None,
#         attach_screenshot: bool = False
# ):
#     """
#     Decorator that:
#     - Fails on assertion errors (test logic failures)
#     - Marks as passed on technical/Selenium failures (e.g., WebDriverException)
#
#     Args:
#         exception_types: List of exception types to treat as "broken" (default: Selenium-related)
#         attach_screenshot: Whether to attach a screenshot in Allure for technical errors
#     """
#     default_exceptions = (
#         WebDriverException,
#         TimeoutError,
#         ConnectionError,
#         ElementNotInteractableException,
#         NoSuchWindowException,
#         InvalidSessionIdException,
#         UnicodeEncodeError
#     )
#
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             driver = None
#             for arg in args + tuple(kwargs.values()):
#                 if hasattr(arg, 'get') and hasattr(arg, 'current_url'):
#                     driver = arg
#                     break
#
#             try:
#                 return func(*args, **kwargs)
#
#             except AssertionError:
#                 raise  # Fail normally on assertions
#
#             except tuple(exception_types or default_exceptions) as e:
#                 pass_msg = f"Test passed (broken condition): {e.__class__.__name__}: {e}"
#                 allure.dynamic.description(f"Original error treated as PASS: {pass_msg}")
#
#                 if attach_screenshot and driver:
#                     try:
#                         screenshot = driver.get_screenshot_as_png()
#                         allure.attach(
#                             screenshot,
#                             name=f"{func.__name__}-broken-passed",
#                             attachment_type=allure.attachment_type.PNG
#                         )
#                     except Exception:
#                         pass  # Ignore screenshot issues
#
#                 # Return None or pass silently — test will be marked as passed
#                 return
#
#         return wrapper
#
#     return decorator
#
#
# # Shortcut
# skip_broken = pass_broken_but_fail_on_assertion()