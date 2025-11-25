"""
Export mixin
"""

import csv
from django.http import HttpResponse
from typing import Any


class ExportMixin:
    """Mixin for data export"""

    @staticmethod
    def export_to_csv(queryset: Any, fields: list, filename: str):
        """Export queryset to CSV"""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow(fields)

        for obj in queryset:
            row = [getattr(obj, field) for field in fields]
            writer.writerow(row)

        return response
