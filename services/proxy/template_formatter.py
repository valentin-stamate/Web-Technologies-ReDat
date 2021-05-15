# TEMPLATE RENDERING WITH CONTEXT
def render_template(template_content: str, context: {}):
    template_content = template_content.format(**context)

    return template_content
