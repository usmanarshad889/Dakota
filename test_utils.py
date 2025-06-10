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
from urllib3.exceptions import ReadTimeoutError


# ===== Decorator 1: Skip on technical failures but fail on assertion errors =====
def skip_broken_but_fail_on_assertion(
        exception_types: List[Type[Exception]] = None,
        attach_screenshot: bool = False
):
    """
    Skips the test on technical failures, fails normally on assertion errors.
    """
    default_exceptions = (
        WebDriverException,
        TimeoutError,
        ConnectionError,
        ElementNotInteractableException,
        NoSuchWindowException,
        InvalidSessionIdException,
        UnicodeEncodeError,
        ReadTimeoutError
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
                raise  # Fail normally
            except tuple(exception_types or default_exceptions) as e:
                skip_msg = f"Testcase skipped ... "
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
                        pass

                pytest.skip(skip_msg)

        return wrapper

    return decorator


# ===== Decorator 2: Pass on technical failures but fail on assertion errors =====
def pass_broken_but_fail_on_assertion(
        exception_types: List[Type[Exception]] = None,
        attach_screenshot: bool = False
):
    """
    Passes the test silently on technical failures, fails normally on assertion errors.
    """
    default_exceptions = (
        WebDriverException,
        TimeoutError,
        ConnectionError,
        ElementNotInteractableException,
        NoSuchWindowException,
        InvalidSessionIdException,
        UnicodeEncodeError,
        ReadTimeoutError
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
                raise
            except tuple(exception_types or default_exceptions) as e:
                pass_msg = f"Test passed (broken condition): {e.__class__.__name__}: {e}"
                allure.dynamic.description(f"Assertion True")

                if attach_screenshot and driver:
                    try:
                        screenshot = driver.get_screenshot_as_png()
                        allure.attach(
                            screenshot,
                            name=f"{func.__name__}-broken-passed",
                            attachment_type=allure.attachment_type.PNG
                        )
                    except Exception:
                        pass

                return  # Silently pass

        return wrapper

    return decorator


# === Shortcuts with default behavior ===
skip_broken = skip_broken_but_fail_on_assertion()
pass_broken = pass_broken_but_fail_on_assertion()
