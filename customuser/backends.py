# from django.contrib.auth import get_user_model
# User = get_user_model()
#
#
# class EmailBackend(object):
#     def authenticate(self, email=None, password=None):
#         UserModel = get_user_model()
#         try:
#             user = UserModel.objects.get(email=email)
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if getattr(user, 'is_active', False) and user.check_password(password):
#                 return user
#         return None
#
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None