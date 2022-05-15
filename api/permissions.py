from rest_framework import permissions


class PostCheck(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return int(request.headers['userId']) == obj.author_id


class ProfileCheck(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return int(request.headers['userId']) == obj.id


class FollowingCheck(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return int(request.headers['userId']) == request.data['following']


class LikingCheck(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'DELETE':
            return int(request.headers['userId']) == request.data['user']
        else:
            return True


class CommentCheck(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return int(request.headers['userId']) == request.data['user']
