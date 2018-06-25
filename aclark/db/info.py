from hashlib import md5


def get_setting(request, setting, settings_model=None, page_size=None):
    """
    Return appropriate setting from user profile model or singleton settings
    model based on args
    """
    if not request.user.is_authenticated:
        return
    if setting == 'icon_size':
        if has_profile(request.user):
            user_pref = request.user.profile.icon_size
        if user_pref:
            return user_pref
    elif setting == 'icon_color':
        if has_profile(request.user):
            user_pref = request.user.profile.icon_color
        if user_pref:
            return user_pref
    elif setting == 'page_size':
        if has_profile(request.user):
            user_pref = request.user.profile.page_size
        if user_pref:
            return user_pref
    elif setting == 'dashboard_choices':
        if has_profile(request.user):
            user_pref = request.user.profile.dashboard_choices
        if user_pref:
            return user_pref
    elif setting == 'exclude_hidden':
        app_settings = settings_model.get_solo()
        return app_settings.exclude_hidden


def has_profile(user):
    return hasattr(user, 'profile')


def gravatar_url(email):
    """
    MD5 hash of email address for use with Gravatar. Return generic
    if none exists.
    """
    try:
        return gravatar_url % md5(email.lower()).hexdigest()
    except AttributeError:
        # https://stackoverflow.com/a/7585378/185820
        return gravatar_url % md5('db@aclark.net'.encode('utf-8')).hexdigest()
