from django.db.models.query import QuerySet


class ImageQuerySet(QuerySet):
    def confirmed(self):
        return self.filter(annotation__meta__confirmed=True)
