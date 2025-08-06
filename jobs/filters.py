import django_filters
from django.db.models import Q
from django.utils.dateparse import parse_date

from .models import JobPost


class JobPostFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="get_search_results", label="search")
    start_date = django_filters.CharFilter(
        method="filter_start_date", label="start_date"
    )
    end_date = django_filters.CharFilter(method="filter_end_date", label="end_date")

    def get_search_results(self, queryset, _, value):
        return (
            queryset.filter(
                Q(job_title__icontains=value)
                | Q(company_name__icontains=value)
                | Q(job_type__icontains=value)
                | Q(job_mode__icontains=value)
                | Q(job_location__icontains=value)
                | Q(job_description__icontains=value)
            )
            .order_by("-created")
            .distinct()
        )

    def filter_start_date(self, queryset, _, value):
        parsed_date = parse_date(value)
        if parsed_date:
            return queryset.filter(created__date__gte=parsed_date)
        return queryset

    def filter_end_date(self, queryset, _, value):
        parsed_date = parse_date(value)
        if parsed_date:
            return queryset.filter(created__date__lte=parsed_date)
        return queryset

    class Meta:
        model = JobPost
        fields = ["search", "start_date", "end_date"]
