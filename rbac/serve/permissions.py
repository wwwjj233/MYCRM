

from django.conf import settings

def permission_in(request,user_obj):
    request.session['user_id'] = user_obj.id
    permission_list = user_obj.roles.values('permissions__pk',
                                            'permissions__url',
                                            'permissions__title',

                                            'permissions__parent_id',

                                            'permissions__menus__pk',
                                            'permissions__menus__weight',
                                            'permissions__menus__title',
                                            'permissions__menus__icon', ).distinct()
    menu_dict = {}
    for permission in permission_list:
        if permission.get('permissions__menus__pk'):
            if permission.get('permissions__menus__pk') in menu_dict:
                menu_dict[permission.get('permissions__menus__pk')]['children'].append(
                    {
                        'url':permission.get('permissions__url'),
                        'title':permission.get('permissions__title'),
                        'id': permission.get('permissions__pk'),
                    }
                )
            else:
                menu_dict[permission.get('permissions__menus__pk')]={
                        'title':permission.get('permissions__menus__title'),
                        'icon':permission.get('permissions__menus__icon'),
                        'weight':permission.get('permissions__menus__weight'),
                        'children':[{
                            'url': permission.get('permissions__url'),
                            'title':permission.get('permissions__title'),
                            'id':permission.get('permissions__pk'),
                        }]
                    }
    permission_list = list(permission_list)
    request.session[settings.MENU_KEY] = menu_dict
    request.session[settings.PERMISSION_KEY] = list(permission_list)