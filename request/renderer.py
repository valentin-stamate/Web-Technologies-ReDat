# TEMPLATE RENDERING WITH CONTEXT
def render_template(template_name='', context={}):
    template_name = f"templates/{template_name}"
    html_string = ""

    print(context)

    with open(template_name, 'r') as f:
        html_string = f.read()
        html_string = html_string.format(**context)

    return html_string


# RENDERING FILES SUCH AS IMAGES, CSS, ETC
def render_file(file_name):
    file_name = file_name[1:len(file_name)]
    file_string = ""

    with open(file_name, 'r') as f:
        file_string = f.read()

    return file_string

