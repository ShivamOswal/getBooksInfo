from django.db.models import Q

from rest_framework import exceptions as drf_exceptions, viewsets

from .models import *
from .serializers import *


class BookViewSet(viewsets.ModelViewSet):
    """ This is an API endpoint that allows books to be viewed. """

    lookup_field = 'gutenberg_id'

    queryset = Book.objects.exclude(download_count__isnull=True)
    queryset = queryset.exclude(title__isnull=True)

    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = self.queryset

        queryset = queryset.order_by('-download_count')

        id_string = self.request.GET.get('ids')
        if id_string is not None:
            ids = id_string.split(',')

            try:
                ids = [int(id) for id in ids]
            except ValueError:
                pass
            else:
                queryset = queryset.filter(gutenberg_id__in=ids)

        language_string = self.request.GET.get('languages')
        if language_string is not None:
            language_codes = [code.lower() for code in language_string.split(',')]
            queryset = queryset.filter(languages__code__in=language_codes)

        mime_type = self.request.GET.get('mime_type')
        if mime_type is not None:
            queryset = queryset.filter(format__mime_type__startswith=mime_type)

        topic = self.request.GET.get('topic')
        if topic is not None:
            queryset = queryset.filter(
                Q(bookshelves__name__icontains=topic) | Q(subjects__name__icontains=topic)
            )

        author = self.request.GET.get('authorName')
        if author is not None:
            queryset = queryset.filter(
                authors__name__icontains=author
            )

        title = self.request.GET.get('title')
        if title is not None:
            queryset = queryset.filter(
                title__icontains=title
            )

        return queryset.distinct()
