from request.renderer import render_template


def home(environ):
    return render_template(template_name='index.html', context={"data": "ana are mere"})


def page_not_found(environ):
    return render_template(template_name='404.html')
