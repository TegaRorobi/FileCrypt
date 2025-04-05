from django.contrib import admin
from main.models import *

admin.site.register(EncryptedResource)
admin.site.register(ResourceAccess_User)
admin.site.register(EncryptionKey)

admin.site.register(Business)

admin.site.register(Organisation)
admin.site.register(OrganisationMember)
admin.site.register(ResourceAccess_Organisation)

admin.site.register(Workspace)
admin.site.register(WorkspaceMember)
admin.site.register(ResourceAccess_Workspace)

admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(ResourceAccess_Team)
