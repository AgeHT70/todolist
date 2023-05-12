from django.contrib import admin

from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    """This class provides configuration for the telegram user section of the admin panel"""

    list_display = ('chat_id', 'db_user')
    readonly_fields = ('verification_code',)

    @staticmethod
    def db_user(obj: TgUser) -> str | None:
        return obj.user.username if obj.user else None
