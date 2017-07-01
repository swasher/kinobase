from django.db.models import Count


# def tags(request):
#
#     # Получаем список всех тегов юзера в виде списка кортежей:
#     # <QuerySet [{'active': 2, 'name': 'tag2', 'pk': 11}, {'active': 1, 'name': 'tag5', 'pk': 4}]>
#     # Каждый кортеж содержит имя pk, имя тега и кол-во игр с данным тегом
#     if not request.user.is_anonymous:
#         tag_list = Tag.objects \
#             .filter(user=request.user) \
#             .annotate(total=Count('games')) \
#             .values('pk', 'name', 'total')
#     else:
#         tag_list = None
#
#     return {'context_tags': tag_list}
