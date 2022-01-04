from django.contrib import admin

# Register your models here.

from .models import Player, Club, OnlyBattle, GroupBattle, PlayerOnlyBattle, PlayerGroupBattle

admin.site.register(Player)
admin.site.register(Club)
admin.site.register(OnlyBattle)
admin.site.register(GroupBattle)
admin.site.register(PlayerOnlyBattle)
admin.site.register(PlayerGroupBattle)