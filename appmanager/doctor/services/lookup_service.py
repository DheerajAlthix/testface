from ..models import Lookup
from ..schemas import LookupSchema

class LookupService:
    def list(self):
        lookups = Lookup.objects.all()
        return [LookupSchema.from_orm(lookup).dict() for lookup in lookups]