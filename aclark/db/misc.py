from hashlib import md5


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
