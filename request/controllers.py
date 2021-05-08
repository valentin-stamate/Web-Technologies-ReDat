from request.renderer import render_template


def home_renderer(environ):
    return render_template(template_name='index.html',
                           context={'top_bar': render_template('top_bar.html'),
                                    'footer': render_template('footer.html')})


def login_renderer(environ):
    return render_template(template_name='login.html', context={})


def register_renderer(environ):
    return render_template(template_name='register.html', context={})


def topics_renderer(environ):
    return render_template(template_name='topics_of_interest.html')


def confirm_account_renderer(environ):
    return render_template(template_name='confirm_account.html')


def user_profile_renderer(environ):
    return render_template(template_name='user_profile.html',
                           context={'top_bar': render_template('top_bar.html'),
                                    'footer': render_template('footer.html')})


def documentation_renderer(environ):
    return render_template(template_name='documentation.html',
                           context={'top_bar': render_template('top_bar.html'),
                                    'footer': render_template('footer.html')})


def doc_renderer(environ):
    return render_template(template_name='doc.html')


def page_not_found_renderer(environ):
    return render_template(template_name='404.html')
