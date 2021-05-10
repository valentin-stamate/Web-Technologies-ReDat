# TEMPLATE RENDERING WITH CONTEXT
def render_template(template_name='', context={}):
    template_path = f"/templates/{template_name}"

    html_string = render_file(template_path)
    html_string = html_string.format(**context)

    return html_string


# RENDERING FILES SUCH AS IMAGES, CSS, ETC
def render_file(file_path):
    print(f"Requested file {file_path}")

    file_path = file_path[1:len(file_path)]
    file_string = ""

    with open(file_path, 'r') as f:
        file_string = f.read()

    return file_string

