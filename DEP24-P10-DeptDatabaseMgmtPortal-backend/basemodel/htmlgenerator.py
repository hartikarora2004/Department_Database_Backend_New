import json

def json_to_html(json_obj):
    if isinstance(json_obj, str):
        json_obj = json.loads(json_obj)

    html_string = ""

    if isinstance(json_obj, dict):
        html_string += "<ul>"

        for key, value in json_obj.items():
            html_string += f"<li><strong>{key}:</strong>"

            if isinstance(value, (str, int, float)):
                html_string += f" {value}</li>"

            elif isinstance(value, (dict, list)):
                html_string += json_to_html(value)

        html_string += "</ul>"

    elif isinstance(json_obj, list):
        html_string += "<ul>"

        for item in json_obj:
            html_string += "<li>"

            if isinstance(item, (str, int, float)):
                html_string += f"{item}</li>"

            elif isinstance(item, (dict, list)):
                html_string += json_to_html(item)

        html_string += "</ul>"

    return html_string

def init_html_table(json_obj):
    str = ""
    str+= "<html>"
    str+= "<head>"
    str+= "<style>"
    str+= "table {"
    str+= "  border-collapse: collapse;"
    str+= "  width: 100%;"
    str+= "}"
    str+= "th, td {"
    str+= "  padding: 8px;"
    str+= "  text-align: left;"
    str+= "  border-bottom: 1px solid #DDD;"
    str+= "}"
    str+= "tr.heading {"
    str+= "  font-weight: bold;"
    str+= "  background-color: #FF0000;"
    str+= "}"
    str+= "tr:hover {background-color: #D6EEEE;}"
    str+= "</style>"
    str+= "</head>"
    str+= "<body>"
    str+= json_to_html_table(json_obj)
    str+= "</body>"
    str+= "</html>"
    return str

def json_to_html_table(json_obj):
    if isinstance(json_obj, str):
        json_obj = json.loads(json_obj)

    html_string = "<table>"
    html_string+="<tr class='heading'>"
    html_string+="<th>attribute</th><th>value</th></tr>"


    if isinstance(json_obj, dict):

        for key, value in json_obj.items():
            html_string+= "<tr>"
            html_string += f"<th><strong>{key}:</strong></th>"

            if isinstance(value, (str, int, float)):
                html_string += f"<td>{value}</td>"

            elif isinstance(value, (dict, list)):
                html_string += f"<td>{json_to_html(value)}</td>"
            html_string+= "</tr>"



    # Check if the JSON object is a list
    elif isinstance(json_obj, list):

        for item in json_obj:
            html_string += "<tr>"

            # If the item is a string or number, add it to the HTML string
            if isinstance(item, (str, int, float)):
                html_string += f"<td>{item}</td>"

            # If the item is a dictionary or list, recursively call the function
            elif isinstance(item, (dict, list)):
                html_string += f"<td>{json_to_html(item)}</td>"
            
            html_string += "</tr>"

    html_string += "</table>"

    return html_string