
from bin.utils.dataclasses import CourierLogin
from flask import Response
import logging
import json
from bin.utils.database import Database
import bin.utils.logger as logger
import requests
import datetime
from bin.utils.statuses_enum import OrderSuccecedStatuses
from bin.utils.database_md import DatabaseMD
import time

from flask_socketio import emit

_logger = logger.Logger()


class CourierController:

    def courier_login(self, courier_login_data: CourierLogin) -> Response:
        try:
            db = Database()
            response_db = db.login(
                email=courier_login_data.email, password=courier_login_data.password)
            logging.info(f'Selected with succes courier data {response_db}')
            if response_db is not None:
                return Response(self.__build_payload_response(message='Selected width success', payload={"id": response_db.id}), status=200, mimetype="application/json")
            else:
                return Response(self.__build_payload_response(message='Username or password is invalid'), status=404, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during login of a the user. User data: {courier_login_data}')
            return Response(self.__build_payload_response(message='An errore occured during loggin'), status=500, mimetype="application/json")

    def select_orders(self, id_courier: int) -> Response:
        try:
            db = Database()
            orders = db.select_orders(
                id_courier=id_courier, status=OrderSuccecedStatuses.delivery_in_progress.value)
            logging.info(F'Selected with success orders: {orders}')
            list_orders = []
            for order in orders:
                user = db.select_user(user_id=order.id_user)
                list_orders.append({
                    'order_id': order.id,
                    'start_time': order.start.strftime('%H:%M'),
                    'end_time': order.end.strftime('%H:%M'),
                    'date': order.start.strftime('%d/%m/%Y'),
                    'month': order.start.strftime("%B"),
                    'day': order.start.strftime("%A")+'\n'+order.start.strftime("%d"),
                    'street_delivery': order.street_delivery,
                    'user_phone':user.phone_number,
                    'cap': order.zip_code,
                    'city': order.city,
                    'quantity': 4,
                    'directions': order.directions
                })
            return Response(self.__build_payload_response(message='Selected width success', payload=list_orders), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during selecting orders of  the user with id :{id_courier}')
            return Response(self.__build_payload_response(message='An errore occured during loggin'), status=500, mimetype="application/json")

    def delivery_done(self, id_order:int, id_courier:int)-> Response:
        try:
            db = Database()
            response_db = db.update_status_order(status=OrderSuccecedStatuses.delivery_done.value, id_order=id_order)
            logging.info(f'Updated status of order {id_order} with success')
            dbm = DatabaseMD()
            response_dbm = dbm.remove_order(id_order=id_order, id_courier= id_courier)
            logging.info(f'Removed order {id_order} with success from courier {id_courier}')
            return Response(self.__build_payload_response(message='Delivery done!'), status=200, mimetype="application/json")
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during updating status of order {id_order}. Courier :{id_courier}')
            return Response(self.__build_payload_response(message='An errore occured during loggin'), status=500, mimetype="application/json")

    def refund_clothes_taked(self, id_order)->Response:
        try:
            db = Database()
            response_db = db.update_status_order(status=OrderSuccecedStatuses.delivery_refund_clothes_in_progress.value, id_order= id_order)
            logging.info(f'Updated status of order {id_order} with success')
            logging.info(f'Makeng get call to main API to make refund of money')
            requests.get(
                f'http://localhost:8080/api_v1/user/make_refund/{id_order}')
            return Response(self.__build_payload_response(message='Refund money executed'), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during updating status of order {id_order} on which user made refund!')
            return Response(self.__build_payload_response(message='An errore occured during loggin'), status=500, mimetype="application/json")
     
    def find_couriers_to_take_delivery(self, id_order:int, socketio)-> Response:
        try:
            dbm = DatabaseMD()
            order = Database().select_order(order_id= id_order)
            #logging.info(f'Selected with succes couriers from DbM {couriers}')
            loop = True
            logging.info(f'Entering in while loop to find courier for the order with id {id_order}')
            #logging.info(f'Courier queque is: {couriers}')
            while loop:
                logging.info('ssss')
                couriers = dbm.select_couriers_ids_by_in_range_of_time_orders(start_time= order.start, end_time= order.end)
                logging.info(f'Selected with succes couriers from DbM {couriers}')
                for courier in couriers:
                    logging.info(f'Trying to send order to courier: {courier} from the queque of the couriers...')
                    if courier['sid'] == '':
                        # TODO notify user/s by Firebase cloud messaging
                        logging.info(f'Courier is disonnected... Trying to notify courier via notification of Firebase')
                    else:
                        logging.info(f"Courier is connected. Emiting new_order to courier with sid: {courier['sid']}")
                        socketio.emit('new_order', {'order_id':id_order}, room=courier['sid'])
                    logging.info(f'Sleeping for 1 minute to give courier time to accept order....')
                    #time.sleep(60)
                    socketio.sleep(60)
                    order = Database().select_order(order_id= id_order)
                    logging.info(f'Looking if the order is taked or not')
                    if order.courier_id is not None:
                        logging.info(F'Order {order.id} is taked by courier {order.courier_id}. Breaking while loop')
                        loop = False
                        break
                #socketio.sleep(60)
                
                    #logging.info(f'Order is not taked')
                    
            return Response(self.__build_payload_response(message='Courier found'), status=200, mimetype="application/json") 
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during updating status of order {id_order} on which user made refund!')
            return Response(self.__build_payload_response(message='An errore occured during loggin'), status=500, mimetype="application/json")
    
    def __build_payload_response(self, message: str, payload=None) -> dict:
        return json.dumps({
            "message": message,
            "payload": payload
        })
