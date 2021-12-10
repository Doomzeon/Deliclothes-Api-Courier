
from bin.utils.dataclasses import CourierLogin
from bin.controller.courier_controller import CourierController
from flask import Flask, request, Response
import datetime
import json
import logging
from bin.utils.database import Database
from flask_socketio import emit
from bin.utils.database_md import DatabaseMD
from bin.services.database_fire import DatabaseFire


class CourierRouter:
    def __init__(self, app, socketio):
        self.app = app
        self.socketio = socketio

        @socketio.on('connect')
        def connect():
            logging.info(f'Connectoin established with: {request.sid}')
            #socketio.emit('new_order', {'order_id':'id_order'}, room=request.sid)

        @socketio.on('disconect')
        def disconnect(data):
            logging.info(f'Connectoin removed with: {request.sid}')
            db = DatabaseMD()
            db.update_sid_courier(sid='', id_courier=data['id_courier'])

        @socketio.on('queque')
        def handle_queque(data):
            db = DatabaseMD()
            logging.info(f'Validating if courier is already existing inside DB mongo')
            if db.find_courier_on_connect_socket(id_courier=data['id_courier']) == False:
                logging.info(f"Courier is new. Procced with his inserting inside DB queque")
                db.insert_courier_data(
                    id_courier=data['id_courier'], sid=request.sid)
            else:
                logging.info(f"Courier already in queque. Procced with updating of sid inside DB queque")
                db.update_sid_courier(
                    sid=request.sid, id_courier=data['id_courier'])

        @socketio.on('accept_order')
        def handle_new_order(data):
            #print(f"Received new order: {data} from {request.sid}")
            logging.info(f'Validating if order is already taked by someone or not')
            order = Database().select_order(order_id=data['id_order'])
            if order.courier_id is None:
                logging.info(f"Order is not taking by nobody. Adding order to courier with id {data['id_courier']}")
                Database().update_courier(
                    id_order=data['id_order'], id_courier=data['id_courier'])
                dbf = DatabaseMD()
                dbf.add_order_to_courier(
                    id_courier=data['id_courier'], order_id=order.id, time_start=order.start, time_end=order.end)
            else:
                logging.info(f"Order is taked by somebody. Emiting message to the user")
                emit('order_already_accepted', {
                     "message": "OOPs order is already taken by someone."})

        @app.route('/api_v1/courier/search_courier/<id_order>', methods=['GET'])
        def search_courier(id_order):
            try:
                logging.info(f'Executing /api_v1/courier/search_courier/<id_order> with id_order = {id_order}')
                return CourierController().find_couriers_to_take_delivery(id_order=id_order, socketio=socketio)
            except Exception as e:
                logging.error(f'An errore occured /api_v1/user/register: {e}')

        @app.route('/api_v1/courier/<id_courier>/delivery_done/<id_order>', methods=['GET'])
        def delivery_done(id_order, id_courier):
            try:
                logging.info(f'Executing /api_v1/courier/<id_courier>/delivery_done/<id_order> with id_order = {id_order} and id_courier = {id_courier}')
                return CourierController().delivery_done(id_order=id_order, id_courier=id_courier)
            except Exception as e:
                logging.error(f'An errore occured /api_v1/user/register: {e}')

        @app.route('/api_v1/courier/taked_refund_clothes/<id_order>', methods=['PUT'])
        def taked_refund_clothes(id_order):
            try:
                logging.info(f'Executing /api_v1/courier/taked_refund_clothes/<id_order> with id_order = {id_order}')
                return CourierController().refund_clothes_taked(id_order=id_order)
            except Exception as e:
                logging.error(f'An errore occured /api_v1/user/register: {e}')

        @app.route('/api_v1/select_orders/<id_courier>', methods=['GET'])
        def select_orders(id_courier):
            try:
                logging.info(f'Executing /api_v1/select_orders/<id_courier> with id_courier = {id_courier}')
                return CourierController().select_orders(id_courier=id_courier)
            except Exception as e:
                logging.error(f'An errore occured /api_v1/user/register: {e}')

        @app.route('/api_v1/courier/login', methods=['POST'])
        def login():
            try:
                courier_login_data = CourierLogin.Schema().loads(
                    json.dumps(request.get_json()['payload']))
                logging.info(f'Executing /api_v1/courier/login with courier_login_data = {courier_login_data}')
                return CourierController().courier_login(courier_login_data=courier_login_data)
            except Exception as e:
                logging.error(f'An errore occured /api_v1/user/register: {e}')

        @app.route('/api_v1/order_arrived/<id_order>/<id_courier>', methods=['PUT'])
        def order_arrived(id_order, id_courier):
            try:
                logging.info(f'Executing /api_v1/order_arrived/<id_order>/<id_courier> with id_courier = {id_courier} and id_order = {id_order}')
                return CourierController().delivery_done(id_order=id_order, id_courier=id_courier)
            except Exception as e:
                logging.error(f'An errore occured /api_v1/user/register: {e}')
