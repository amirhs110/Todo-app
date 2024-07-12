from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class TaskPagination(PageNumberPagination):
    page_size = 6

    def get_paginated_response(self, data):
        return Response({
            'total_tasks': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'links': {
                # 'first': 'http://127.0.0.1:8000/blog/api/v1/post/?page=1',
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'results': data
        })