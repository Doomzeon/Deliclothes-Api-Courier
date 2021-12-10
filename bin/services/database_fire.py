import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class DatabaseFire():

    def __init__(self):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate({
                    "type": "service_account",
                    "project_id": "deliclothes-dce05",
                    "private_key_id": "a138df046f887c11170f5e88c3df7839417a7191",
                    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEugIBADANBgkqhkiG9w0BAQEFAASCBKQwggSgAgEAAoIBAQCQG/OXcacc7xQx\nLpuCcuW1O80NoBeMS7MboVmQ5p/0RTBsKzp5M9k8DQzGRygTMJMeeH4AeuFQzVUD\nL5hOQrnzQpA3FjLh58DPWSxpEQW92Mudq4I2Ij3vdMN0UGtW+NuzN46NtYVV5/Jg\nps2+ShSJ4PeJiYqAlwnXkH48ch4vXV+psUa3tfCBikyUn+nwO6ERWsk3XIgNyOzy\npNSYVeuEo2wDM+eQRRk7CF0v11S1CRLccpMedQS7MDCO1VA+PWZ3BrRFzoCRjzuu\nV6ryTtaTPdERzA4znrBAglR0sioBBkX8pEz5O73uKqyaeDktdz6xYMwke+kZXpIh\n7UTus0olAgMBAAECgf9C047ZGW1lRp1fnvQ1HDdpZeQekfoQXi7VDv15xp1BqR05\nC/daz2c2lkRWQF/nYZ8gpr9+VOsCsewDaaESqZWRXXE50TYQZ4yUCFhrO+dJIj+T\nAqxfSYG4P/+HzAxD2toGr07+HsFIXiJ1QcAm66Es4Up7NAO9C3HyqTNOi1O9NLjf\nVFvEmiCI5bbR90DA1ODcJge6HlrkcEmegtkzFkaAGYy4HPkGDOizLuy7jwynb3Bf\nZXbQ6PszIvPhE2YH8EAUCZcoQPyR34nwpzKw1e/2bgBuPCWqtuD5k3gsQGuK+G93\nJZngfV9geN9FYEuvA0CSCj0qjr0qxSW+OJZ2NUECgYEAwNZwx4q2Xe89EDR46lVm\nRz1NRICZslUtpMQb8IiV5Qh5ce3+XHupByTSjQYwqgUw702vxi01E8pfkI9wq505\n1uhuQDsF48gbgOOVgT2stlShmqZVC06+DHWMlMwRwfSaeoAjcktbJEIE5bYpmSpj\nhu8uRFR6qkEv5OjUi6T585ECgYEAv0+ZB2/u2vquqbsa04qhxlDCloqyBcFeg4Ng\nwi6yEAAhPj83cJmkiJzxTvUpcnf2vp6E7IXaaNkl8A9Z4MdpOxybodTmfg2HNhyY\n5JL7V4O/t32/FZbtok5yLAWlmNuFaTLaW2XnJdIQ6GiL8JhwRl3BRDXL2Np5KmwO\ndePjO1UCgYBqAPd6GVxqgqq0j8OwPUW9/4rMD01t5Lj0jAE31j1f66qm4EclG60t\nCibb8v0pWTUvNyta61r0CBlEZDVxgTpcUuTYVhnEvymvTmvO4dJhYGB9nNW/I4gB\nXVTsLsnMLuQEVxAlMhtl8Qy0IdD4K38Om8h5M19C3Bax5POB2Cy2oQKBgF08qdQa\nFUrbyawm6BgZBGbmjS9ZQRHU//8QVGPO5jEuHwV7QcW625lJA8H7ccu786FLGHU9\ndwiKbBbnJGKMTRjmBGOGox7j8PXKUil0CNLJ/vGqcypOeFoV6UbTKbWppwdyJUFO\nFK02B898xFbptC5XGw3nOgXh1BN8vj9uZRxRAoGAQtAFBwcgp6P2z2EIqU9xhl7J\nSvFK6FHJWxxQULGb36cD4q8feHGnlZ3vHRyd5FBBpNHsNb2oqz0NobB294Iv6KnY\nM4zFog3ESoVNfbTH++WEMX80A7yTv80uyl9t9SGmZs998odhqHd0scu6zkFDcJLg\nPavzb7ja9cwurYYPxtQ=\n-----END PRIVATE KEY-----\n",
                    "client_email": "firebase-adminsdk-krrik@deliclothes-dce05.iam.gserviceaccount.com",
                    "client_id": "113043869901042798216",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-krrik%40deliclothes-dce05.iam.gserviceaccount.com"
                })
                self.app = firebase_admin.initialize_app(cred)
            self.db = firestore.client()
        except Exception as e:
            print(e)


    def find_courier_on_connect_socket(self, id_courier):
        try:
            courier = self.db.collection('couriers').where(
                'id', '==', id_courier
            ).get()
            print(courier)
            for courie in courier:
                print(courie)
            if len(courier) ==0:
                return False
            else:
                return True

        except Exception as e:
            print(e)


    def update_sid_courier(self, sid, id_courier):
        try:
            docs = self.db.collection('couriers').where(
                'id', '==', id_courier
            ).get()
            for doc in docs:
                self.db.collection('couriers').document(doc.id).update({'sid':sid})
            return True

        except Exception as e:
            print(e)
            return False


    def insert_courier_data(self, sid, id_courier):
        try:
            self.db.collection('couriers').add(
                {'id': id_courier, 'orders': [], "sid": sid}
            )
            return True
        except Exception as e:
            print(e)
            return False
        

    def select_couriers_without_orders(self):
        try:
            couriers = self.db.collection('couriers').where(
                'orders', '==', []
            ).get()
            print(couriers)
            if len(couriers) == 0:
                return None
            else:
                return couriers
        except Exception as e:
            print(e)


    def add_order_to_courier(self, courier_id, order_id, time_start, time_end):
        try:
            docs = self.db.collection('couriers').where(
                'id', '==', courier_id
            ).get()
            for doc in docs:
                self.db.collection('couriers').document(doc.id).update({'orders':firestore.ArrayUnion([{'order_id':order_id, 'time_start':time_start, 'time_end':time_end}])})
            
        except Exception as e:
            print(e)

    
    def select_couriers_in_range_of_time(self, start_timestamp, finish_timestamp):
        try:
            print(start_timestamp)
            result = self.db.collection('couriers').where()#.where('time_start', '==', start_timestamp).get()
            print('selected')
            print(result)
            return None
        except Exception as e:
            print(e)
            return None