import psycopg2
import os
from data_set import exception_dict
from data_search import material_flags, finishing_numbers, heat_treat_search, form_tool_search, fabricate, stamp, mirror_t_or_f, inplant

# Convert sql data into normal obj/dict to call git/key on (FOR STRUT)
class PartDataObjStrut:
    def __init__(self, part_id, part_name,  zone_, stock_size, material, heat_treat, finish, part_mark, formed, tooling, mirror_part, mirror_part_num, machined):
        self.part_id = part_id
        self.part_name = part_name
        self.zone = zone_
        self.stock_size = stock_size
        self.material = material
        self.heat_treat = heat_treat
        self.finish = finish
        self.part_mark = part_mark
        self.formed = formed
        self.tooling = tooling
        self.mirror_part = mirror_part
        self.mirror_part_num = mirror_part_num
        self.machined = machined
    
    def get(self, attribute_name):
        return getattr(self, attribute_name)
    
    def keys(self):
        return [key for key in self.__dict__.keys() if not key.startswith('__')]


# Convert sql data into normal obj/dict to call git/key on (FOR NACELLE)
class PartDataObjA10:
    def __init__(self, part_id, part_name,  zone_, stock_size, material):
        self.part_id = part_id
        self.part_name = part_name
        self.zone = zone_
        self.stock_size = stock_size
        self.material = material
    
    

    def get(self, attribute_name):
        try:
            if isinstance(attribute_name, str):
                print("IS A STRING?")
            elif isinstance(attribute_name, list):
                print("IS A LIST?")
            elif isinstance(attribute_name, dict):
                print("Is a dict?")
            return getattr(self, attribute_name)
        
        #ACCOUNT FOR DIFFRENCES BETWEEN STRUT AND NACELLE TRAVELERS
        except AttributeError:
            return ""
    
    def keys(self):
        return [key for key in self.__dict__.keys() if not key.startswith('__')]

#Access portal_data_base. connect, disconnect, find parts and images
class PostgresDB:
    def __init__(self, dbname, user, password, host, port, part_num):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.part_num = part_num

    def connect(self):
        try:
            #will need to update credentials when different users logged in
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connected to data_base")
        except psycopg2.Error as e:
            print(f"Error: Unable to connect. {e}")

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            print("Successfuly disconnected from database")

   
    def insert_part(self, table, data):
        if self.conn is None:
            print("Error: Not connected to the database")
            return False
        try: 
            cursor = self.conn.cursor()
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"
            cursor.execute(query, list(data.values()))
            self.conn.commit()
            cursor.close()
            print("Part inserted successfully")
            return True
        
        except psycopg2.Error as e:
            print(f"Error: unable to insert. {e}")
            return False
        

    def determine_contract(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM a10_nacelle_parts
            WHERE part_id = %s
        ) AS pk_exists;
        """, (self.part_num,))

        pk_exists = cursor.fetchone()[0]

        cursor.close()

        if pk_exists:
            print(f"FOUND PART {self.part_num} IN NACELLE DB, VALUE: {pk_exists}")
            return True
        else:
            print(f"DID NOT FIND {self.part_num} IN NACELLE DB, VALUE: {pk_exists}")
            return False
        
        
    #check parts(strut database) first then the a10_nacelle database(a10_nacelle_parts)
    def find_part(self):
        if self.conn is None:
            print("Error: Not connected to the database")
            return False
        cursor = self.conn.cursor()
        
        try:   
            cursor.execute("""
            SELECT *
            FROM parts
            WHERE part_id = %s
            LIMIT 1
            """, (self.part_num,))

            part_id = self.part_num
          
            result = cursor.fetchone()

            if result:
              
                part_data = PartDataObjStrut(*result)
                return part_data
            
            else:
                cursor.execute("""
                SELECT *
                FROM a10_nacelle_parts
                WHERE part_id = %s
                LIMIT 1
                """, (self.part_num,))

                result = cursor.fetchone()

                if result:
                    
                    part_data = PartDataObjA10(*result)
                    return part_data
       
                else:
                  
                    print(f"Part with part_id {part_id} not found")

        except psycopg2.Error as e:
           
            print(f"Error: unable to find part. {e}")
            return False
        
        finally:
            cursor.close()


        
    def find_image(self):
        try:
            #Ensure part_number is a string
           
            if not isinstance(self.part_num, str):
               
                wrong_type = type(self.part_num)
                raise TypeError(f"WRONG TYPE ENTRY: part_number is a {wrong_type} should be a string ")
            
            #Attrmpt to get the part information using part_number
        
        except TypeError as e:
        #Handle TypeError 
        
            print(f"TypeError: {e}")
            part_info = None
       
        relevant_images = []

        #make path to dir with images
        paths = os.getcwd()
        dir_list = os.listdir(f'{paths}\static\images')

        #checks to see if part number is in image names, if yes added to list
        for file in dir_list:
            if self.part_num in file:
                relevant_images.append(file)
    
        return relevant_images
    



    
    def heat_treat(self):
        if self.conn is None:
            print("Error: Not connected to the database")
            return False
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
            SELECT part_id, field_note_id
            FROM nacelle_5003_field_notes_ref
            WHERE part_id = %s
            """, (self.part_num,))

            field_notes = []

            for row in cursor.fetchall():
                field_notes.append(row[1])
                
            if field_notes:
                print(f"field notes created: {field_notes}")
                
                if 2 in field_notes:
        
                    try:   
                        cursor.execute("""
                        SELECT *
                        FROM nacelle_5003_field_notes
                        WHERE field_note_id = %s
                        LIMIT 1
                        """, (2,))

                        result = cursor.fetchone()
                        print(result)

                        if result:
                        
                            return result
                        
                    except psycopg2.Error as e:
                
                        print(f"Error: unable to find part. {e}")
                        return False

                        
        except psycopg2.Error as e:
            print(f"Error: unable to applicable field notes. {e}")
            return False

  
   
                  

    



class Exception:
    def __init__(self, part_number):
        self.part_number = part_number

    def find_execption (self):

        #Extract target part dict
        db = PostgresDB(
                dbname="portal_data_base",
                user="postgres",
                password="123",
                host="",
                port="5000",
                part_num=self.part_number
                )
        try:
            db.connect()

            part_info = db.find_part()

            #Make list of all assemblies with exceptions
            ex = exception_dict.keys()

            #Loop through all assembly exceptions
            for key in ex:
                    
                    #for assembly with exception get dict
                ex_part = exception_dict.get(key)
                    #If target part is in assembly with an exception AND said assembly exception has the same material listed as target part
                if key in self.part_number and ex_part.get(part_info.get("material")) != None:
                        
                        #return the dict of the material that target part has from exception dictonary
                    ex_val = ex_part.get(part_info.get("material"))
                    return ex_val
                
            return ""
        finally:
            db.disconnect()

        


# db.conect()

# data = {
#     'part_id': part_id,
#     'part_name': part_name,
#     'zone_': zone,
#     'stock_size': stock_size,
#     'material': material,
#     'heat_treat': heat_treat,
#     'finish': finish,
#     'part_mark': part_mark,
#     'formed': formed,
#     'tooling': tooling,
#     'mirror_part': mirror_part,
#     '"mirror_part_#"': mirror_part_num,
#     'machined': machined

# }

# success = db.insert_part("parts", data)
# if success:
#     print("Part inserted successfully")
# else:
#     print("Failed to isnert part")

# db.disconnect()