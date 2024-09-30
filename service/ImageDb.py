import sys
from service.DbConnector import *
import logging as logger


class ImageDb:
    def get_images(self, diseaseId):

        query = "SELECT * FROM Disease_image WHERE disease_id='" + diseaseId + "'"
        image_array = []
        try:
            db = get_db_cursor()
            cursor = db.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                image = {
                    "id": row[0],
                    "image_url": row[2],
                    "image_ref": row[3]
                }
                image_array.append(image)

            db.commit()
        except:
            e = sys.exc_info()[0]
            logger.error(e)
            db.rollback()
        finally:
            if db.is_connected():
                cursor.close()
                db.close() 
            
        return image_array
