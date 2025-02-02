
from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
	"Custom permission that checks if a user is a SuperUser"

	def has_permission(self, request, view):
		return bool(request.user and request.user.is_authenticated and request.user.is_superuser)