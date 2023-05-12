from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment, BoardParticipant, Board
from goals.permissions import BoardPermission, GoalCategoryPermission, GoalPermission, GoalCommentPermission
from goals.serializers import (
    GoalCategoryCreateSerializer,
    GoalCategorySerializer,
    GoalCreateSerializer,
    GoalSerializer,
    GoalCommentCreateSerializer,
    GoalCommentSerializer,
    BoardSerializer,
    BoardWithParticipantsSerializer,
)


class BoardCreateView(generics.CreateAPIView):
    """This view is used to create a new board"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer

    def perform_create(self, serializer: BoardSerializer) -> None:
        with transaction.atomic():
            board = serializer.save()
            BoardParticipant.objects.create(user=self.request.user, board=board)


class BoardListView(generics.ListAPIView):
    """The BoardListView provides logic to display a list of all available boards"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self) -> QuerySet[Board]:
        return Board.objects.filter(participants__user_id=self.request.user.id).exclude(is_deleted=True)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """This view is used to show, update and delete a single board"""

    permission_classes = [BoardPermission]
    serializer_class = BoardWithParticipantsSerializer

    def get_queryset(self) -> QuerySet[Board]:
        return Board.objects.prefetch_related('participants__user').exclude(is_deleted=True)

    def perform_destroy(self, instance: Board) -> None:
        with transaction.atomic():
            Board.objects.filter(id=instance.id).update(is_deleted=True)
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)


class GoalCategoryCreateView(generics.CreateAPIView):
    """This view is used to create a category"""

    permission_classes = [GoalCategoryPermission]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    """The CategoryListView provides logic to display a list of categories"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['board']
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self) -> QuerySet[GoalCategory]:
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    """This view is used to show, update and delete a single category"""

    permission_classes = [GoalCategoryPermission]
    serializer_class = GoalCategorySerializer

    def get_queryset(self) -> QuerySet[GoalCategory]:
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)


class GoalCreateView(generics.CreateAPIView):
    """This view is used to create a goal"""

    permission_classes = [GoalPermission]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    """The GoalListView provides logic to display a list of goals"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = GoalDateFilter
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self) -> QuerySet[Goal]:
        return Goal.objects.filter(
            category__is_deleted=False, category__board__participants__user_id=self.request.user.id
        ).exclude(status=Goal.Status.archived)


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    """This view is used to show, update and delete a single goal"""

    permission_classes = [GoalPermission]
    serializer_class = GoalSerializer

    def get_queryset(self) -> QuerySet[Goal]:
        return Goal.objects.filter(
            category__is_deleted=False, category__board__participants__user_id=self.request.user.id
        ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance: Goal) -> None:
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentCreateView(generics.CreateAPIView):
    permission_classes = [GoalCommentPermission]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    """The CommentListView provides logic to display a list of comments"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('goal',)
    ordering_fields = ['created', 'updated']
    ordering = ['-created']

    def get_queryset(self) -> QuerySet[GoalComment]:
        return GoalComment.objects.filter(goal__category__board__participants__user_id=self.request.user.id).exclude(
            goal__status=Goal.Status.archived
        )


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    """This view is used to show, update and delete a single comment"""

    permission_classes = [GoalCommentPermission]
    serializer_class = GoalCommentSerializer

    def get_queryset(self) -> QuerySet[GoalComment]:
        return GoalComment.objects.filter(goal__category__board__participants__user_id=self.request.user.id).exclude(
            goal__status=Goal.Status.archived
        )
