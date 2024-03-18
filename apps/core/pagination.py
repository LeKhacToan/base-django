from rest_framework.pagination import LimitOffsetPagination


class DefaultLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 200

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.count = self.get_count(queryset)
        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return view.repository_class.paginate_queryset(queryset, self)

    def get_limit(self, request):
        limit = super().get_limit(request)
        try:
            if int(request.query_params[self.limit_query_param]) == -1:
                return self.max_limit
        except Exception:
            return limit

        return limit
