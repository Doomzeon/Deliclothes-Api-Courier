import flask_pymongo as pymongo


class DatabaseMD():

    def __init__(self):
        try:
            self.mongodb_client = pymongo.MongoClient(
                "mongodb+srv://admin:admin@couriers.vyr0z.mongodb.net/Couriers?retryWrites=true&w=majority")
            print(self.mongodb_client.db)
            self.db = self.mongodb_client.Couriers
        except Exception as e:
            raise(e)

    def find_courier_on_connect_socket(self, id_courier):
        try:
            courier = self.db.courier.find_one({"id": id_courier})
            if courier is None:
                return False
            else:
                return True
        except Exception as e:
            raise(e)

    def update_sid_courier(self, sid, id_courier):
        try:
            self.db.courier.update_one(
                {'id': id_courier}, {"$set": {'sid': sid}})
        except Exception as e:
            raise(e)

    def insert_courier_data(self, id_courier, sid, orders=None):
        try:
            self.db.courier.insert_one(
                {'id': id_courier, 'orders': [], "sid": sid})
        except Exception as e:
            raise(e)

    def add_order_to_courier(self, id_courier, order_id, time_start, time_end):
        try:
            self.db.courier.update(
                {"id": id_courier},
                {
                    "$push": {
                        "orders": {
                            "order_id": order_id,
                            "time_start": time_start,
                            "time_end": time_end
                        }
                    }

                }
            )
            return True
        except Exception as e:
            raise(e)

    def select_couriers_without_orders(self):
        try:
            courier = self.db.courier.find({"orders": []})
            print(f'Select couriers: {courier}')
            return courier
        except Exception as e:
            raise(e)

    def remove_order(self, id_order: int, id_courier):
        try:
            self.db.courier.update(
                {'id': id_courier},
                {"$pull": {"orders": {"order_id": id_order}}})
            return True
        except Exception as e:
            raise(e)

    def select_couriers_ids_by_in_range_of_time_orders(self, start_time, end_time):
        try:
            couriers = self.db.courier.aggregate(
                [
                    {
                        '$match': {

                            '$or': [
                                {
                                    'orders.time_start': {
                                        '$gt': end_time
                                    },
                                    'orders.time_end': {
                                        '$gt': start_time
                                    }
                                }, {
                                    "orders": []
                                }],
                        }}, {
                        '$project': {
                            'id_courier': '$id',
                            'sid': '$sid',
                            'length': {
                                '$size': '$orders'
                            }
                        }
                    }, {
                        '$sort': {
                            'length': 1
                        }
                    }
                ]
            )
            for cor in couriers:
                print(cor)
            return couriers
        except Exception as e:
            raise(e)
