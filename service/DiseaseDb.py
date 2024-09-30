import sys
import os
from service.DbConnector import *
import logging as logger
import json


class DiseaseDb:
    def get_diseases(self):
        query = "SELECT * FROM Disease"
        
        disease_array = []
        try:
            connection = get_db_cursor()
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                disease = {
                    "id": row[0],
                    "orpha_code": row[1],
                    "name": row[2],
                    "abbreviation": row[3],
                    "sub_category": row[4],
                    "gene_name": row[5],
                    "gene_reference": row[6],
                }
                disease_array.append(disease)

            connection.commit()            

        except:
            err = sys.exc_info()[0]
            logger.error(err)
            print(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()                

        return disease_array

    def get_diseases_by_orpha_code(self, orpha_code):
        query = "SELECT * FROM Disease WHERE orpha_code='" + orpha_code + "'"
        count = 0
        try:
            connection = get_db_cursor()
            cursor = connection.cursor()
            cursor.execute(query)
            row = cursor.fetchall()
            count = len(row)
            connection.commit()            
        except:
            err = sys.exc_info()[0]
            logger.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            

        return count

    def get_diseases_by(self, searchStr, searchBy):

        column_name = ""
        if searchBy == "name":
            column_name = "name"
        elif searchBy == "gene":
            column_name = "gene_name"
        elif searchBy == "category":
            column_name = "sub_category"

        query = "SELECT * FROM Disease WHERE " + column_name + " LIKE '%" + searchStr + "%'"
        disease_array = []
        try:
            connection = get_db_cursor()
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                disease = {
                    "id": row[0],
                    "orpha_code": row[1],
                    "name": row[2],
                    "abbreviation": row[3],
                    "sub_category": row[4],
                    "gene_name": row[5],
                    "gene_reference": row[6],
                }
                disease_array.append(disease)

            connection.commit()            
        except:
            err = sys.exc_info()[0]
            logger.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            

        return disease_array

    def add_disease(self, disease):
        count = DiseaseDb.get_diseases_by_orpha_code(self, disease['orpha_code'])
        if count > 0:
            return 0

        query = "INSERT INTO Disease " \
                "(orpha_code, name, abbreviation, sub_category, gene_name, gene_reference) " \
                "VALUES (%s,%s,%s,%s,%s,%s)"
        val = (
            disease['orpha_code'].strip(), disease['name'].strip(), disease['abbreviation'].strip(),
            disease['sub_category'].strip(), disease['gene_name'].strip(), disease['gene_ref'].strip())
        
        files = json.loads(disease['files'])
        refs = json.loads(disease['refs'])

        result = -1
        try:
            connection = get_db_cursor()
            cursor = connection.cursor()
            cursor.execute(query, val)
            disease_id = cursor.lastrowid
            i = 0
            for fileName in files:
                query = "INSERT INTO Disease_image " \
                        "(disease_id, image_url, image_ref) " \
                        "VALUES (%s,%s,%s)"
                val = (disease_id, fileName, refs[i])
                cursor.execute(query, val)
                i = i + 1

            connection.commit()
            result = 1            
        except:
            err = sys.exc_info()[0]
            logger.error(err)
            print(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            

        return result

    def update_disease(self, disease, filesToDeleteArr):

        query = "UPDATE Disease " \
                "SET orpha_code=%s, name=%s, abbreviation=%s, sub_category=%s, gene_name=%s, gene_reference=%s" \
                "WHERE id=%s"
        val = (
            disease['orpha_code'].strip(), disease['name'].strip(), disease['abbreviation'].strip(),
            disease['sub_category'].strip(), disease['gene_name'].strip(), disease['gene_ref'].strip(),
            disease['id'].strip())
        

        files = json.loads(disease['files'])
        refs = json.loads(disease['refs'])
        filesToDelete = json.loads(filesToDeleteArr)

        result = -1
        try:
            connection = get_db_cursor()
            cursor = connection.cursor()
            cursor.execute(query, val)
            i = 0
            for fileName in files:
                query = "INSERT INTO Disease_image " \
                        "(disease_id, image_url, image_ref) " \
                        "VALUES (%s,%s,%s)"
                val = (disease['id'], fileName, refs[i])
                cursor.execute(query, val)
                i = i + 1

            # Keep image file names in an array
            image_urls = []
            for fileId in filesToDelete:
                query = "SELECT image_url FROM Disease_image WHERE id=" + str(fileId)
                cursor.execute(query)
                result = cursor.fetchall()
                for row in result:
                    image_urls.append(row[0])

            for fileId in filesToDelete:
                query = "DELETE FROM Disease_image WHERE id=" + str(fileId)
                cursor.execute(query)

            connection.commit()

            # remove image files from server folder
            for file_name in image_urls:
                os.remove(os.path.join('static', file_name))

            result = 1
        except:
            err = sys.exc_info()[0]
            logger.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            

        return result

    def remove_disease(self, disease_id):
        result = -1
        
        try:
            connection = get_db_cursor()
            cursor = connection.cursor()
            # Keep image file names in an array
            image_urls = []
            query = "SELECT image_url FROM Disease_image WHERE disease_id='" + disease_id + "'"
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                image_urls.append(row[0])

            query = "DELETE FROM Disease WHERE id='" + disease_id + "'"
            cursor.execute(query)
            connection.commit()
            
            # remove image files from server folder
            for file_name in image_urls:
                os.remove(os.path.join('static', file_name))

            result = 1
        except:
            err = sys.exc_info()[0]
            logger.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            

        return result

    def get_all_diseases_category(self):        
        query = "SELECT sub_category FROM Disease"
        

        disease_categories = []
        try:
            connection = get_db_cursor()
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()         
            items = []
            for row in result:
                if row[0] != "":
                    items.append(row[0].lower().title())

            disease_categories = sorted(list(set(items)))
            connection.commit()
            
        except:
            err = sys.exc_info()[0]
            logger.error(err)
            print(err)            
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            

        return disease_categories

    def get_dieases_by_category(self, category):
        query = "SELECT * FROM Disease WHERE sub_category='" + category + "'"
        
        disease_array = []
        try:
            connection = get_db_cursor()
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                disease = {
                    "id": row[0],
                    "orpha_code": row[1],
                    "name": row[2],
                    "abbreviation": row[3],
                    "sub_category": row[4],
                    "gene_name": row[5],
                    "gene_reference": row[6],
                }
                disease_array.append(disease)

            connection.commit()            
        except:
            err = sys.exc_info()[0]
            logger.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            

        return disease_array
