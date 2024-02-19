from import_export import resources

from accounts.models import AgentLic

class AgentLicResource(resources.ModelResource):
    class Meta:
        model = AgentLic