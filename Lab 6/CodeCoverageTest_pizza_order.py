"""Lab 6 - tests written for LINE (code) coverage of pizza_order.py.

Each test drives execution through lines that the starter tests never reached.
Run:  coverage run -m pytest CodeCoverageTest_pizza_order.py
      coverage report -m
"""
import pytest
from pizza_order import pizza_price, order_discount, delivery_status


# ---- starter tests ----
def test_plain_medium_pizza():
    assert pizza_price("medium", 0, False) == 350


def test_on_time_delivery():
    assert delivery_status(20, 3) == "on time"


# ---- pizza_price ----
def test_unknown_size_raises():
    with pytest.raises(ValueError, match="unknown size"):
        pizza_price("huge", 1, False)


def test_negative_toppings_raises():
    with pytest.raises(ValueError, match="invalid toppings"):
        pizza_price("small", -1, False)


def test_more_than_three_toppings():
    # 500 + 3*40 + 2*30
    assert pizza_price("large", 5, False) == 680


def test_cheese_burst_small_raises():
    with pytest.raises(ValueError, match="cheese burst"):
        pizza_price("small", 0, True)


def test_cheese_burst_medium():
    assert pizza_price("medium", 2, True) == 350 + 80 + 100


# ---- order_discount ----
def test_discount_below_threshold():
    assert order_discount(299, "monday", False) == 0


def test_discount_tuesday_half_price():
    assert order_discount(400, "tuesday", False) == 200


def test_discount_weekend_none():
    assert order_discount(400, "saturday", False) == 0


def test_discount_weekday_student():
    assert order_discount(500, "friday", True) == 50 + 50


# ---- delivery_status ----
def test_not_deliverable():
    assert delivery_status(10, 11) == "not deliverable"


def test_late_delivery():
    assert delivery_status(40, 5) == "late"


def test_free_pizza():
    assert delivery_status(60, 5) == "free pizza"
