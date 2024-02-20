from flask import Flask, request, render_template, flash, session, redirect, url_for, g
from flask_debugtoolbar import DebugToolbarExtension
from data_search import material_flags, finishing_numbers, heat_treat_search, form_tool_search, fabricate, stamp, mirror_t_or_f, inplant
from image_reading_sand_box import ocr
from sql_access import PostgresDB, Exception
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

app.debug = True

toolbar = DebugToolbarExtension(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set the minimum log level

# Create a file handler and set the log level
file_handler = RotatingFileHandler('flask.log', maxBytes=10240, backupCount=10)
file_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the file handler
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logging.getLogger().addHandler(file_handler)

#ChatGPT
@app.before_request
def before_request(part_number=None):
    g.db = PostgresDB(
        dbname="db",
        user="postgres",
        password="123",
        host="",
        port="5000",
        part_num=part_number
    )
    g.db.connect()

@app.teardown_request
def teardown_request(exception=None):
    if hasattr(g, 'db'):
        g.db.disconnect()

# source: https://www.geeksforgeeks.org/retrieving-html-from-data-using-flask/

@app.route('/', methods=['GET', 'POST'])
def home():  
    """Home screen for engineering portal"""

    return render_template("index.html")


@app.route('/new_part_entry', methods=['GET', 'POST'])
def new_part():
    if request.method == "GET":
        flash(f"REACHED PAGE", 'success')
        return render_template("new_part_entry.html")
    
  
    
    elif request.method == "POST":
        print('entered data entry post')
       

        #Create stock size dimension
        stock_f_string = f"{request.form.get('stock_size_1')} X {request.form.get('stock_size_2')} X {request.form.get('stock_size_3')}"

        #Capture data from form to uploard to table
        data = {
            'part_id': request.form.get('part_number'),
            'part_name': request.form.get('part_name'),
            'zone_': request.form.get("Zone"),
            'stock_size': stock_f_string,
            'material': request.form.get("material"),
            'heat_treat': request.form.get("heat_treat"),
            'finish': request.form.get("finish"),
            'part_mark': request.form.get("part_mark"),
            'formed': request.form.get("formed"),
            'tooling': request.form.get("tooling"),
            'mirror_part': request.form.get("mirror_part"),
            '"mirror_part_#"': request.form.get("mirror_part_number"),
            'machined': request.form.get("machined") 
            }

        success = g.db.insert_part("parts", data)
        if success:
            flash("Part inserted successfully", "success")
        else:
            flash("Failed to insert part", "failure")
        
    return redirect(url_for(new_part))
    

      






@app.route('/search_database_for_', methods=['GET', 'POST'])
def post_data():
    #Shows return for search request, should have affiliated screenshots
    if request.method == "GET":
        return render_template(
            "search.html"
        )
    elif request.method == "POST":
        #Extract desired part number from html form
        part_number = request.form.get("part_id")

        #Add part_number as an argument to PostgresDB
        before_request(part_number)
        
     

        #Create object for target part
        part_data = g.db.find_part()
            

        #Finds any matching images for the part number
        images = g.db.find_image()
        print(images)

        #Extracts specific part dict for part number
        # part_data= part.find_part()

            
        print(part_data)
            
        session['part_num'] = part_number

        if part_data != None:
        #if there was a request for part return correlating part info
                
            flash(f"Found {part_number} in database", 'success')
              

            #render_template with part information
            return  render_template(          
            "search.html",
                
            #inplant is the function for jinja to put an image into html dynamically
            inplant = inplant,
                
            images = images,
            part_num= part_number,
            part_data=part_data,

            #key_set is the specific part dict for the searched for part
            key_set=part_data.keys(),
            )
        
        else:
            #return if part was not found in database
            flash(f"{part_number} was not found in database", 'failure')
            return  render_template(          
            "search.html",
            # image_file= '/images/' + "../images/35-8227-204.jpeg",
            part_num = "",
            part_data="",
            )
            






@app.route('/gen_traveler_for', methods=['GET', 'POST'])
def gen_trav():
    #Automatically filles required fields needed for word order travelers
    
    if request.method == "GET":
        return render_template('trav.html')
    
    elif request.method == "POST":
        part_number = request.form.get("gen_trav")
       
        #Add part_number as an argument to PostgresDB
        before_request(part_number)
        part_data= g.db.find_part()
       

        if part_data != None:

            if not g.db.determine_contract():
                    
                #create new instance of Exception object
                ex = Exception(part_number)
                    
                #Indicate trav was created
                flash(f"Generated traveler for {part_number}", 'success')
                    

                return render_template(
                    #each field is correlated value stored in part dict
                    "trav.html",
                    mirror = mirror_t_or_f(part_data.get("mirror_part")),
                    stock = part_data.get("stock_size"),
                    material = material_flags(part_number, part_data.get("material")),
                    fab = fabricate(part_data.get("machined")),
                    form = form_tool_search(part_data.get("formed"), part_data.get("tooling"), part_data.get("mirror_part"), part_data.get("mirror_part_num"), part_number, part_data.get("machined"), part_data.get("part_name")),
                    heat_treat = heat_treat_search(part_data.get("heat_treat"), ex.find_execption()),
                    finish = finishing_numbers(part_data.get("finish"), ex.find_execption()),
                    mark = stamp(part_data.get("part_mark"))
                )
            else:
                flash(f"Generated traveler for Nacelle part {part_number}", 'success')
                fab = "fab"
                debur_and_blend = "debur and blend"
                heat_treat = g.db.heat_treat()
                check_and_straighten = "check and straighten"
                finish = "finish"
                mark = "mark"

                return render_template(
                    "nacelle_trav.html",
                    stock = part_data.get("stock_size"),
                    material = part_data.get("material"),
                    fab = fab,
                    debur_and_blend = debur_and_blend,
                    heat_treat = heat_treat,
                    check_and_straighten = check_and_straighten,
                    finish = finish,
                    mark = mark

                )
        else:
            #return if part was not found in database
            flash(f"Failed to generated traveler for {part_number}", 'failure')
            return render_template(
                "index.html",
            )
       
    

   
    
@app.route('/blue_print_ocr', methods = ['GET', 'POST'])
def convert_text():
    if request.method== 'GET':
        ocr = ocr()
        return render_template(
            'blue_print_ocr',
            ocr = ocr
        )
    

if __name__ == "__main__":
    app.run(debug=True)
