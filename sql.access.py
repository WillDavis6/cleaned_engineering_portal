

# Establish a connection to PostgeSQL database


# cursor = conn.cursor()

# primary_key_value = 'part_id'

# query = "SELECT * FROM parts WHERE part_id = %s;"

# cursor.execute(query, (primary_key_value,))

# row = cursor.fetchone()

# print(type(row))

# cursor.close()
# conn.close()
import psycopg2

class PartDataObj:
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

class PostgresDB:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        try:
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
        
    def find_part(self, part_num):
        if self.conn is None:
            print("Error: Not connected to the database")
            return False
        
        try: 
            cursor = self.conn.cursor()
            
            find = """
            SELECT part_id, part_name,  zone_, stock_size, material, heat_treat, finish, part_mark, formed, tooling, mirror_part, "mirror_part_#", machined
            FROM parts
            WHERE part_id = %s;
            """

            part_id = part_num
            cursor.execute(find, (part_id,))

            results = cursor.fetchone()

            cursor.close()
            

            if results is not None:
                part_data = PartDataObj(*results)
                print(part_data.get('part_id'))
                return part_data
            else:
                print(f"Part with part_id {part_id} not found")

        except psycopg2.Error as e:
            print(f"Error: unable to find part. {e}")
            return False

        


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
         