from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bookmarks.models import Bookmark
from apps.bookmarks.permissions import BookmarkEditPermissions
from apps.bookmarks.serializers import BookmarkSerializer


def _add(a, b):
    return int(a[0]) + int(b[0])


class AddViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return Response({"result": _add(**request.data)}, status=status.HTTP_200_OK)


class BookmarksViewSet(viewsets.ModelViewSet):
    """ Supports list, create, update and delete actions"""
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = []
    lookup_field = "id"
    lookup_url_kwarg = "bookmark_id"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            qs = qs.filter(Q(created_by=self.request.user) | Q(is_private=False))
        else:
            qs = qs.filter(is_private=False)
        return qs.order_by("-created_at")

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ("partial_update", "destroy"):
            self.permission_classes = [IsAuthenticated, BookmarkEditPermissions]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, created_at=timezone.now())