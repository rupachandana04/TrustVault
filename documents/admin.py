from django.contrib import admin
from .models import Document, DocumentPermission, AuditLog


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'uploaded_at')
    search_fields = ('title', 'owner__username', 'category')


@admin.register(DocumentPermission)
class DocumentPermissionAdmin(admin.ModelAdmin):
    list_display = ('document', 'user', 'permission', 'granted_at')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_title', 'action', 'timestamp')
    readonly_fields = ('user', 'document_title', 'action', 'timestamp', 'details')

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# Register your models here.
