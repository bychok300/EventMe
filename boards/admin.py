from django.contrib import admin

from .models import Board, Post, Comments, Topic

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Comments)
