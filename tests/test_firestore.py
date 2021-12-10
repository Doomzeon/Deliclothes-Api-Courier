

from bin.services.database_fire import DatabaseFire
from bin.utils.database import Database
import datetime
db2 =DatabaseFire()

def test_select_couriers_in_range_of_time():
    order = Database().select_order(order_id= 55)
    print(order.start)
    assert db2.select_couriers_in_range_of_time(start_timestamp= order.start, finish_timestamp= order.end)

"""def test_select_couriers_without_orders():
    assert db2.select_couriers_without_orders() is not None

def test_add_order_to_courier():
    assert db2.add_order_to_courier(courier_id=0, order_id=56, time_start='23:23', time_end='112:23') == ''

def test_find_courier_on_connect_socket():
    result_1 = db2.find_courier_on_connect_socket(id_courier=0)
    print(result_1)
    assert result_1 == False
    

def test_insert_courier_data():
    assert db2.insert_courier_data(sid='ss2', id_courier=0) == True


def test_ind_courier_on_connect_socket2():
    result_2 = db2.find_courier_on_connect_socket(id_courier=0)
    print(result_2)
    assert result_2 == True 


def test_update_sid_courier():
    result_2 =db2.update_sid_courier(id_courier=0,sid='22')
    print(result_2)
    assert result_2 == True """
    
    