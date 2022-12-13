from django.contrib import admin
from gestor.models import *

admin.site.register(Producto)
# Register your models here.
@admin.register(Evento)
class EventAdmin(admin.ModelAdmin):
    model = Evento
    list_display = [
        "id",
        "titulo",
        "usuario",
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
    list_filter = ["is_active", "is_deleted"]
    search_fields = ["titulo"]


@admin.register(EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    model = EventMember
    list_display = ["id", "evento", "usuario", "created_at", "updated_at"]
    list_filter = ["evento"]
