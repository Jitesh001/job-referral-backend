from rest_framework.pagination import PageNumberPagination as DefaultPagination
from rest_framework.response import Response


class PageNumberPagination(DefaultPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response(
            {
                "pagination": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "count": self.page.paginator.count,
                    "current": self.page.number,
                    "total": self.page.paginator.num_pages,
                },
                "results": data,
            }
        )
