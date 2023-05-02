from django.contrib import admin


from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')
    list_filter = ('is_deleted',)


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')
    list_filter = ('status',)


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal', 'created', 'updated')
    search_fields = ('user', 'goal')



class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'created', 'updated')


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('board', 'user', 'role', 'created', 'updated')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardParticipant, BoardParticipantAdmin)
