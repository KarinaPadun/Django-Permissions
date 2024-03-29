from rest_framework import permissions

class IsChatUserOrSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_superuser

class IsChatSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
