from data_set import part_dictonary, material_dictonary, finishing_dictonary, exception_dict, heat_treat_dict
import os
from flask import Flask, url_for
import doctest

# Contains all functions used for processing requests and sorting through data. 

def material_flags(input, number):
    '''
    Find Material number in specific part dictonary, use said number to search in material_dictonary and return string containing material information

    >>>material_flags("123", 3)
    'metal'
    
    '''

# return a list of all assembly numbers in material_dictonary
    tech_drawing_numbers = material_dictonary.keys()

# Loop through all numbers in list
    for drawing_number in tech_drawing_numbers:

# If desired part numbers first to set of numbers match the assemlby number
        if drawing_number in input: 

# Access dict of matched assembly number
            selected_drawing = material_dictonary.get(drawing_number)

# Access values of material number (flag) from arguments 
            selected_flag = selected_drawing.get(number)

            return (selected_flag)

        

        
def finishing_numbers(input, ex_val):
    '''
    Accepts arguments of a finishig code and if part has an exception value (ex_val). Returns a string for traveler with instructions for said finish, including new finish if part is an exceptoin.

    >>>finishing_numbers("abc", "")
    ''

    >>> finishing_numbers("cba", {'fake': "fake, 'fake': 'fake'})
    'made up finishing process'

    '''
# If the argument given for exception value ("ex_val") is not an empty string
    if ex_val != "":

# Search in finishing dictonary with the finish code stored in the ex_val dict, and reutrn finishing instructions
        return finishing_dictonary.get(ex_val.get('Finish'))
    
# If the finishing code correlates to no finish, return empty string
    elif input == "1" or input == "2":
        return ""

#If the code does not mean no finish and the input in not an empty string, return finishing instructions from input argument
    elif input != "1" and input != "2" and input != "NA":
        return (f'{finishing_dictonary.get(input)}  PRODUCTION STAMP/DATE:___________________________')
    else:
        return ""
    

def heat_treat_search(input, ex_val):
    """
    Accepts arguments of heat treat name and if part has an exception value (ex_val). Returns a string for traveler with instrucitons for said heat treat, includes new heat treat if part is an exception.

    """
    keys = heat_treat_dict.keys()
    if ex_val != "":
        return ex_val.get("HEAT TREAT")
    elif ex_val == "":
        if input in keys:
           
            heat_treat = heat_treat_dict.get(input)
          
            return heat_treat
    else:
        return ''

def form_tool_search(form, tool, mirror, num_mirror, part_number, machined, name):
    """
    Accepts True/False arguments for if the part is machined, formed, tooling, a mirror part, has a mirror number as well as the part number or if it has a part name "SKIN". Returns a string with instructions
    for how to make the part.

 
    """

    if machined == False:
        if form == True and tool == False and mirror == False:
            if name == "NAME":
                return "FORM PART PER 123 DURING INSTALLATION. PRODUCTION STAMP/DAT:____________________"
            else:
                return "FORM PART PER 123. PRODUCTION STAMP/DATE:___________________________"
        if form == True and tool == False and mirror == True:
            return "FORM PART PER 123. PRODUCTION STAMP/DATE:___________________________"
        elif form == True and tool == True and mirror == False:
            return f"FORM PART PER 123. USING TOOLING T-{part_number} PRODUCTION STAMP/DATE:___________________________"
        elif form == True and tool == True and mirror == True:
            return f"FORM PART PER 123. USING TOOLING T-{part_number} (OPP- T-{num_mirror}) PRODUCTION STAMP/DATE:___________________________"
        elif form == False:
            return ""
    elif machined == True:
        return "MACHINE FEATURES TO PRINT: PRODUCTION STAMP/DATE:____________________ "
    else:
        return ""
    

def fabricate(machined):
    """
    Accepts argument of True/False if part is machined. Returns string instructions for how to fabricate if part is not machined.


    """
    
    if machined == False:
        return "FABRICATE PART TO PRINT REQUIREMENTS.  PRODUCTION STAMP/DATE:___________________________"
    else:
        return ""

def stamp(input):
    """
    Accepts argument of part marking, typically abc, rarley 123, and returns string instruction of how to mark part.


    """

    if input == "abc":
        return "MARK LOT NUMBER PER 123.  QA STAMP/DATE:___________________________ "
    elif input == "123":
        return "123D PART MARKING.  QA STAMP/DATE:___________________________ "
    else:
        return ""

def mirror_t_or_f(input):
    """
    Accepts argument of wether part is has a mirror image part or not, and returns a string to include more than one part for in traveler instructions.

  
    """

    if input == True:
        return "PART NUMBER:________________ "
    elif input == False:
        return ""

  
 

    
    
def find_execption (part_number):
    """
    Accepts argument target part number, finds if this part has an engineering order exception. Finds assemblys with exceptions, compares if this parts material has an exception and returns dic with instrucitons
    if said material has exceptions.

   
    """

    #Extract target part dict
    part_info = part_dictonary.get(part_number)

    #Make list of all assemblies with exceptions
    ex = exception_dict.keys()

    #Loop through all assembly exceptions
    for key in ex:
            
            #for assembly with exception get dict
        ex_part = exception_dict.get(key)

            #If target part is in assembly with an exception AND said assembly exception has the same material listed as target part
        if key in part_number and ex_part.get(part_info.get("Material")) != None:
                
                #return the dict of the material that target part has from exception dictonary
            ex_val = ex_part.get(part_info.get("Material"))
            return ex_val
        
    return ""
    

    

def find_part(part_number):
    """
    Accepts argument of target part number, finds if target is in part_dictonary. Returns dict for target part. Else returns a string that part was not found.
    


    """

    if part_number in part_dictonary:
        part_info = part_dictonary.get(part_number)
       # ex_val = find_execption(part_number)
        # print_traveler(part_info, part_number, ex_val) 
        return part_info
    else:
        print("did not find search_number")



def find_image(part_number):
    """
    Accepts argument of part number, creats an empty list of that will store the names of all screenshots with target part name in them. os is find the path to where the images are stored. All images are looped through to find if part 
    number is in their names. If they are they are added to list. returns list of relevent part images.
    

    """
    relevant_images = []

    #make path to dir with images
    paths = os.getcwd()
    dir_list = os.listdir(f'{paths}\static\images')

    #checks to see if part number is in image names, if yes added to list
    for file in dir_list:
        if part_number in file:
            relevant_images.append(file)
   
    return relevant_images

def inplant(input):
    """
    Works in conjunction with find_images. addes needed url_for feature for flask to be able to pull image name in a scr feature in html. Looped over when multiple relevent images are found.

    Having difficulty testing with doctest, will try to confirm with flask testing
    """
    return url_for('static', filename=f'images/{input}')



# print_traveler CURRENTLY NOT IN USE, FLASK/JINJA IS BYPASSING THE NEED FOR ONE WHOLE FUNCTION
#*************************************************************************************************************************************************************************************************************
def print_traveler (parts_info, part_number, ex_val): 
    """
    Accepts arguments of the target part info dictonary, target part number, and wether the part has a exception. 
    
    Extracts values from parts_info: Mirror Part,
                                     Part Mark,
                                     Stock Size,
                                     Heat Treat,
                                     Finish,
                                     Material,
                                     Formed,
                                     Tooling,
                                     Mirror Part #,
                                     Machined Part,
                                     Part Name
    
    Calls functions: mirror_t_or_f, 
                     heat_treat_search, 
                     finishing_number, 
                     material_flags, 
                     form_tool_search,
                     fabricate,
                     stamp

    Builds work instruction for traveler from above information depending on what the part requires.


    Currently not in use, the jinja template trav.html calls funcitons inidividually and inserts them into html. 
    """



    mirror = mirror_t_or_f(parts_info.get("Mirror Part", ""))
    stamped = parts_info.get("Part Mark")
    stock = parts_info.get("Stock Size")
    ht = heat_treat_search(parts_info.get("Heat Treat"), ex_val)
    finish_number = parts_info.get("Finish")
    finish_info = finishing_numbers(finish_number, ex_val)
    material_flag_number = parts_info.get("Material")
    material_info = material_flags(part_number, material_flag_number)
    form_and_tool = form_tool_search(parts_info.get("Formed"), parts_info.get("Tooling"), parts_info.get("Mirror Part"), parts_info.get("Mirror Part #"),
    part_number, parts_info.get("Machined Part"), parts_info.get("Part Name"))
    fab = fabricate(parts_info.get("Machined Part"))
    mark = stamp(stamped)
    
    
    trav = (f"\n\
ASSIGNED LOT NUMBER:___________________________ PART QTY:________ {mirror}CONTRACT___________\n\
\n\
\n\
\n\
\n\
MATERIAL: {stock}, {material_info} LOT #:___________________________\n\
\n\
\n\
\n\
\n\
{fab}\n\
\n\
\n\
\n\
\n\
{form_and_tool}\n\
\n\
\n\
\n\
\n\
{ht}\n\
\n\
\n\
\n\
\n\
{finish_info}\n\
\n\
\n\
\n\
\n\
QA FINAL INSPECTION, QA STAMP/DATE:___________________________\n\
\n\
\n\
\n\
\n\
{mark}")
  #  print(trav)
    

#**************************************************************************************************************************************************************************************************************************
