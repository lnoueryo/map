class MapRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'map':
            return 'db2'
 
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'map':
            return 'db2'
 
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'map' or \
           obj2._meta.app_label == 'map':
           return True
 
    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == 'map':
            return db == 'db2'

# class MapRouter:
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label == 'map' or model._meta.app_label == 'management':
#             return 'db2'
 
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'map' or model._meta.app_label == 'management':
#             return 'db2'
 
#     def allow_relation(self, obj1, obj2, **hints):
#         if obj1._meta.app_label == 'map' or obj2._meta.app_label == 'map' or obj1._meta.app_label == 'management' or obj2._meta.app_label == 'management':
#            return True
 
#     def allow_migrate(self, db, app_label, model=None, **hints):
#         if app_label == 'map' or app_label == 'management':
#             return db == 'db2'
