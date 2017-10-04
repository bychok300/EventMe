from django.contrib import admin

from .models import Board, Post, Comments, Topic

# admin.py в нем можно регистрировать таблицы из базы
# которые будут отражены в админке

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Comments)
