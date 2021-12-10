from flask import Flask, request, Response
from bin.handler.routers.courier_router import CourierRouter


class Router:
    def __init__(self, app, socketio):
        self.app = app
        self.socketio = socketio
        @app.route('/api_v1/alive', methods=['GET'])
        def alive():
            """Check if the service is running"""
            return "I'm alive!"

        CourierRouter(app=self.app, socketio= self.socketio)
        