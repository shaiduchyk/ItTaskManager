from haystack import indexes
from .models import Task


class TaskIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    worker = indexes.CharField(model_attr="worker__name")
    position = indexes.CharField(model_attr="position__name")
    project = indexes.CharField(model_attr="project__project_name")

    def get_model(self):
        return Task

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
