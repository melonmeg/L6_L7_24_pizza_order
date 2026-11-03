"""Lab 6 - tests written for BRANCH coverage of pizza_order.py.

Every decision is exercised for both its True and False outcome, including the
boundary values (toppings == 3, total == 300, minutes == 30 / 45, km == 10).
Run:  coverage run --branch -m pytest BranchCoverageTest_pizza_order.py
      coverage report -m
"""
import pytest
from pizza_order import pizza_price, order_discount, delivery_status


# ---- pizza_price ----
@pytest.mark.parametrize("size,base", [("small", 200), ("medium", 350), ("large", 500)])
def test_valid_sizes_plain(size, base):
    assert pizza_price(size, 0, False) == base


def test_unknown_size_raises():
    with pytest.raises(ValueError, match="unknown size"):
        pizza_price("huge", 1, False)


def test_negative_toppings_raises():
    with pytest.raises(ValueError, match="invalid toppings"):
        pizza_price("small", -1, False)


def test_zero_toppings_is_valid():
    assert pizza_price("small", 0, False) == 200


def test_exactly_three_toppings_uses_flat_rate():
    # toppings > 3 is False at the boundary
    assert pizza_price("medium", 3, False) == 350 + 3 * 40


def test_four_toppings_uses_discounted_rate():
    # toppings > 3 is True at the boundary: 3*40 + 1*30
    assert pizza_price("medium", 4, False) == 350 + 120 + 30


def test_cheese_burst_small_raises():
    with pytest.raises(ValueError, match="cheese burst"):
        pizza_price("small", 0, True)


def test_cheese_burst_medium_and_large():
    assert pizza_price("medium", 0, True) == 450
    assert pizza_price("large", 0, True) == 600


def test_no_cheese_burst_small_ok():
    assert pizza_price("small", 1, False) == 240


# ---- order_discount ----
def test_below_threshold_no_discount():
    assert order_discount(299, "monday", True) == 0


def test_threshold_boundary_is_eligible():
    assert order_discount(300, "monday", False) == 30


def test_tuesday_half_price_non_student():
    assert order_discount(400, "tuesday", False) == 200


def test_tuesday_student():
    assert order_discount(400, "tuesday", True) == 250


@pytest.mark.parametrize("day", ["saturday", "sunday"])
def test_weekend_no_base_discount(day):
    assert order_discount(400, day, False) == 0


def test_weekend_student_gets_only_student_discount():
    assert order_discount(400, "sunday", True) == 50


def test_weekday_ten_percent_non_student():
    assert order_discount(500, "wednesday", False) == 50


def test_weekday_student():
    assert order_discount(500, "wednesday", True) == 100


# ---- delivery_status ----
def test_not_deliverable_over_10km():
    assert delivery_status(5, 10.1) == "not deliverable"


def test_exactly_10km_is_deliverable():
    assert delivery_status(5, 10) == "on time"


def test_on_time_boundary_30():
    assert delivery_status(30, 5) == "on time"


def test_late_boundaries():
    assert delivery_status(31, 5) == "late"
    assert delivery_status(45, 5) == "late"


def test_free_pizza_after_45():
    assert delivery_status(46, 5) == "free pizza"
