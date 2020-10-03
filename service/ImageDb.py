import sys
from service.DbConnector import *
import logging as logger


class ImageDb:
    def get_images(self, diseaseId):

        query = "SELECT * FROM Disease_image WHERE disease_id='" + diseaseId + "'"
        db, cursor = get_db_cursor()
        image_array = []
        try:
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
            cursor.close()
            db.close()

        return image_array
