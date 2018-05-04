from aclarknet.db.models import Profile


def create_profile(user, request=None):
    profile_obj, _ = Profile.objects.get_or_create(user=user)
    profile_obj.save()


# https://stackoverflow.com/a/6109366
def login_receiver(sender, user, request, **kwargs):
    """
    """
    create_profile(user, request=request)
