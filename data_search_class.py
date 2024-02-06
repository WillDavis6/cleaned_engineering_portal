from data_set import part_dictonary, material_dictonary, finishing_dictonary
import os



class DataSearchclass:
    def __init__(self, part_number):
        # You can initialize any class-specific variables in the constructor if needed
        self.part_number = part_number

    def __repr__(self):
        return f"Target part: {self.part_number}"

    def find_part(self):
        try:
            #Ensure part_number is a string
            if not isinstance(self.part_number, str):
                wrong_type = type(self.part_number)
                raise TypeError(f"WRONG TYPE ENTRY: part_number is a {wrong_type} should be a string ")
            
            #Attrmpt to get the part information using part_number
        except TypeError as e:
        #Handle TypeError 
            print(f"TypeError: {e}")
            part_info = None
      

        if self.part_number in part_dictonary:
            part_info = part_dictonary.get(self.part_number)
 
            return part_info
        else:
            print("did not find search_number")

    def find_image(self):
        try:
            #Ensure part_number is a string
            if not isinstance(self.part_number, str):
                wrong_type = type(self.part_number)
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
            if self.part_number in file:
                relevant_images.append(file)
    
        return relevant_images