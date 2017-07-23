class PostsPermission:
    def has_permission(self, request, view):

        if view.action in ("list", "retrieve", "update", "partial_update", "destroy"):
            return True

        if view.action == "create":
            return request.user.is_authenticated

        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' and obj.publish_at != None:
            return True
        else:
            return request.user.is_superuser or request.user == obj.owner