
import logging
import sqlalchemy
from bin.models import order_entity,courier_entity, user_entity
from sqlalchemy.orm import scoped_session, sessionmaker
import bin.utils.logger as logger #import LogLevel, Logger

_logger = logger.Logger()

class Database:
    
    def __init__(self):
        self.__session = None
        
        
    def update_direction_status(self, order_id, data):
        try:
            self.__session = self.__create_session()
            order_ent = self.__session.query(order_entity.OrderEntity).filter_by(order_id= order_id).first()
            for i in range(len(order_ent.directions)):
                if order.directions[i]['id'] == data['id']:
                    del order.clothes[i]
                    order.clothes.append(data)
                    break
            self.__session.commit()
            
            return True
        except Exception as e:
            self.__error_handling()
            print(e)
            #_logger.log(e, logger.LogLevel.fatal, message=f'An error occured while adding new user inside the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()
                
                
    def select_order(self, order_id):
        try:
            self.__session = self.__create_session()
            order_ent = self.__session.query(order_entity.OrderEntity).filter_by(id= order_id).first()
            return order_ent
        except Exception as e:
            self.__error_handling()
            print(e)
            #_logger.log(e, logger.LogLevel.fatal, message=f'An error occured while adding new user inside the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()
            
        
    def select_orders(self, id_courier:int, status:int):
        try:
            self.__session = self.__create_session()
            orders_ent = self.__session.query(order_entity.OrderEntity).filter_by(courier_id= id_courier, status_int= status).order_by(order_entity.OrderEntity.start).all()
            return orders_ent
        except Exception as e:
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()
                
                
    def update_courier(self, id_order, id_courier):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(order_entity.OrderEntity).filter_by(id= id_order).first()
            order.status_int = 3
            order.courier_id = id_courier
            self.__session.commit()
        except Exception as e:
            self.__error_handling()
            print(e)
            #_logger.log(e, logger.LogLevel.fatal, message=f'An error occured while adding new user inside the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()
        
    
    def select_all_couriers(self):
        try:
            self.__session = self.__create_session()
            ids = self.__session.query(courier_entity.CourierEntity.id).all()
            return ids
        except Exception as e:
            self.__error_handling()
            print(e)
            #_logger.log(e, logger.LogLevel.fatal, message=f'An error occured while adding new user inside the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()
        
    
    def login(self, email, password):
        try:
            self.__session = self.__create_session()
            courier = self.__session.query(courier_entity.CourierEntity).filter_by(email= email, password= password).first()
            return courier
        except Exception as e:
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()
            
    
    def select_user(self, user_id):
        try:
            self.__session = self.__create_session()
            user = self.__session.query(user_entity.UserEntity).filter_by(id = user_id).first()
            logging.info(f'\nSelected from Database: {user}')
            return user
        except Exception as e:
            self.__error_handling()
           #_logger.log(e, logger.LogLevel.fatal, message=f'An error occured while adding new user inside the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()
            
    
        
    def update_status_order(self, status:int, id_order:int):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(order_entity.OrderEntity).filter_by(id= id_order).first()
            order.status_int = status
            self.__session.commit()
            return True
        except Exception as e:
            self.__error_handling()
           #_logger.log(e, logger.LogLevel.fatal, message=f'An error occured while adding new user inside the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()
            
        
        
    def __error_handling(self):
        self.__session.rollback()
        self.__close_session()
    
    
    def __close_session(self):
        if self.__session is not None:
            self.__session.close()
        
        
    def __create_session(self):
        try:
            logging.info('\nCreating session object with the Database')
            Session = sessionmaker(bind = self.__get_db_engine(), expire_on_commit=False)
            return Session()
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'An errore occured while creating session with the Database')
            
            
    def __get_db_engine(self):
        try:
            logging.info('\nConnecting to the Database')
            engine = sqlalchemy.create_engine("postgresql+psycopg2://doomzeon:doomzeon@localhost/doomzeon", pool_pre_ping=True)
            
            logging.info("\nConnection with the Database established")
            return engine
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Fail to establish connection with the database')
        

