
from django.contrib.auth import get_user_model
from django.conf import settings
from django.dispatch import receiver

from allauth.account.utils import perform_login
from allauth.account.signals import user_signed_up, user_logged_in
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from user.models.user import User


class MyAccountAdapter(DefaultSocialAccountAdapter):

    # def get_extra_data(self,sociallogin):
    #     data = {'given_name': ('user','first_name'), 'family_name': ('user','last_name'), 'picture':('profile','avatar')}
    #     user = User.objects.get(email = sociallogin.user.email)
    #     profile = Profile.objects.get(user= user)
    #     breakpoint()
    #     for field in data.keys():
    #         try:
    #             if field in sociallogin.account.extra_data.keys():
    #                 model , model_field = data.values('given_name')
    #                 if model == 'user':
    #                     pass
    #         except:
    #             pass
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        # if user.id:
        #     return
        
        try:
            customer = User.objects.get(email=user.email)
            # self.get_extra_data(sociallogin)
            sociallogin.state['process'] = 'connect'                
            perform_login(request, customer, 'none')
        except User.DoesNotExist:
            pass
    
    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully
        connecting a social account.
        """
        assert request.user.is_authenticated
        url = settings.LOGIN_REDIRECT_URL
        return url
    
@receiver(user_signed_up)
def get_extra_data(request, user, **kwargs):
    
    profile = User.objects.get(user=user)
    data = SocialAccount.objects.filter(user=user, provider='facebook')
    if data:
        picture = data[0].get_avatar_url()
        profile.avatar = picture
# from django.conf import settings
# from allauth.account.adapter import DefaultAccountAdapter

# class MyAccountAdapter(DefaultAccountAdapter):

#     def get_login_redirect_url(self, request):
#         path = "/accounts/{username}/"
#         return path.format(username=request.user.username)
