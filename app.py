from flask import Flask, request, render_template, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from data_search import find_part, material_flags, finishing_numbers, heat_treat_search, form_tool_search, fabricate, stamp, mirror_t_or_f, find_execption, find_image, inplant
from data_search_class import DataSearchclass


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

app.debug = True

toolbar = DebugToolbarExtension(app)



# source: https://www.geeksforgeeks.org/retrieving-html-from-data-using-flask/

@app.route('/', methods=['GET', 'POST'])
def home():  
    """Home screen for engineering portal"""

    return render_template("index.html")


@app.route('/search_database_for_', methods=['GET', 'POST'])
def post_data():
    #Shows return for search request, should have affiliated screenshots
    
    #Extract desired part number from html form
    part_number = request.form.get("part_id")

    #Create class for target part
    part = DataSearchclass(part_number)

    #Finds any matching images for the part number
    images = part.find_image()

    #Extracts specific part dict for part number
    part_data= part.find_part()


    if request.method == "POST" and part_data != None:
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
        part_num = "",
        part_data="",
        )
    


@app.route('/gen_traveler_for', methods=['GET', 'POST'])
def gen_trav():
    #Automatically filles required fields needed for word order travelers
    part_number = request.form.get("part_id")
    part_data= find_part(part_number)

    if request.method == "POST" and part_data != None:

        flash(f"Generated traveler for {part_number}", 'success')
        
        return render_template(
            #each field is correlated value stored in part dict
            "trav.html",
            mirror = mirror_t_or_f(part_data.get("Mirror Part", "")),
            stock = part_data.get("Stock Size"),
            material = material_flags(part_number, part_data.get("Material")),
            fab = fabricate(part_data.get("Machined Part")),
            form = form_tool_search(part_data.get("Formed"), part_data.get("Tooling"), part_data.get("Mirror Part"), part_data.get("Mirror Part #"), part_number, part_data.get("Machined Part"), part_data.get("Part Name")),
            heat_treat = heat_treat_search(part_data.get("Heat Treat"), find_execption(part_number)),
            finish = finishing_numbers(part_data.get("Finish"), find_execption(part_number)),
            mark = stamp(part_data.get("Part Mark"))
        )

    else:
        #return if part was not found in database
        flash(f"Failed to generated traveler for {part_number}", 'failure')
        return render_template(
            "index.html"
        )

if __name__ == "__main__":
    app.run(debug=True)