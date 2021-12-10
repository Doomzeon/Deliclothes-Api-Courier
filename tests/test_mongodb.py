
from bin.utils.database_md import DatabaseMD
from bin.utils.database import Database
from datetime import datetime, timezone


def test_select_couriers_ids_by_in_range_of_time_orders():
    db= DatabaseMD()
    assert db.select_couriers_ids_by_in_range_of_time_orders(start_time=datetime(2021, 5, 6, 17, 50, 0, tzinfo=timezone.utc), end_time=datetime(2021, 5, 6, 17, 0, 0, tzinfo=timezone.utc)) != None
    

"""def test_add_order_to_courier():
    order = Database().select_order(order_id= 55)
    db= DatabaseMD()
    assert db.add_order_to_courier(id_courier=0, order_id=order.id, time_start=order.start, time_end= order.end) == True"""
    