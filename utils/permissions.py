
from rest_framework import permissions
from main.models import *


class NotAllowed(permissions.BasePermission):

	def has_permission(self, request, view):
		return False
class IsSuperUser(permissions.BasePermission):
	"Custom permission that checks if a user is a SuperUser"

	def has_permission(self, request, view):
		return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

class IsOrganisationAdminOrSuperUser(permissions.BasePermission):
	"""
	Checks if a user is:
	• an admin or superadmin organisation member to that organisation or,
	• a SuperUser.
	"""
	def has_object_permission(self, request, view, obj):
		try: member_profile = obj.member_profiles.get(user=request.user)
		except: return False

		return bool(
			request.user and request.user.is_authenticated and (
				request.user.is_superuser or
				member_profile.is_organisation_admin or
				member_profile.is_organisation_superadmin
			)
		)

class IsOrganisationMemberOrSuperUser(permissions.BasePermission):
	"""
	Checks if a user is either:
	• a memmber of the target organisation or,
	• a SuperUser.
	"""
	def has_object_permission(self, request, view, obj):
		try:
			return bool(obj.member_profiles.get(user=request.user))
		except:
			return True if request.user.is_superuser else False