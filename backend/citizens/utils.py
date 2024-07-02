from django.db.models import Q
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)

from citizens.models import Citizens


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Citizens.objects.filter(id=int(query))

    vector = SearchVector("family_name", "first_name", "second_name", "comment")
    query = SearchQuery(query)

    result = (
        Citizens.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    return result