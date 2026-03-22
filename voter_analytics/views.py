# File: views.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: views for the voter_analytics app

from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.db.models.functions import Trim
import plotly.graph_objects as go
from plotly.offline import plot
from .models import Voter


ELECTION_FIELDS = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
ELECTION_LABELS = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']


def filter_voters(qs, params):
    '''Apply GET param filters to a Voter queryset'''

    party = params.get('party', '').strip()
    if party:
        qs = qs.annotate(party_trimmed=Trim('party')).filter(party_trimmed=party)

    min_dob = params.get('min_dob', '')
    if min_dob:
        qs = qs.filter(dob__year__gte=int(min_dob))

    max_dob = params.get('max_dob', '')
    if max_dob:
        qs = qs.filter(dob__year__lte=int(max_dob))

    score = params.get('voter_score', '')
    if score:
        qs = qs.filter(voter_score=int(score))

    for field in ELECTION_FIELDS:
        if params.get(field):
            qs = qs.filter(**{field: True})

    return qs


def form_context():
    '''Return shared filter form context'''
    raw_parties = Voter.objects.values_list('party', flat=True).distinct()
    return {
        'parties': sorted(set(p.strip() for p in raw_parties)),
        'years': range(1900, 2026),
        'scores': range(0, 6),
    }


class VoterListView(ListView):
    '''Show all voters with optional filtering'''

    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        return filter_voters(Voter.objects.all(), self.request.GET)

    # called internally, populates filter data!
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(form_context())
        ctx['params'] = self.request.GET
        return ctx


class VoterDetailView(DetailView):
    '''Show a single voter record'''

    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class VoterGraphView(ListView):
    '''Show aggregate graphs of voter data with optional filtering'''

    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        return filter_voters(Voter.objects.all(), self.request.GET)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(form_context())
        ctx['params'] = self.request.GET

        qs = self.get_queryset()

        # birth year histogram
        birth_data = (
            qs.values('dob__year')
            .annotate(count=Count('id'))
            .order_by('dob__year')
        )
        years = [d['dob__year'] for d in birth_data]
        year_counts = [d['count'] for d in birth_data]
        fig1 = go.Figure(go.Bar(x=years, y=year_counts))
        fig1.update_layout(title='Distribution of Voters by Birth Year',
                           xaxis_title='Year', yaxis_title='Count')
        ctx['birth_year_graph'] = plot(fig1, output_type='div', include_plotlyjs=False)

        # party pie chart
        party_data = (
            qs.annotate(party_trimmed=Trim('party'))
            .values('party_trimmed')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        party_labels = [d['party_trimmed'] for d in party_data]
        party_counts = [d['count'] for d in party_data]
        fig2 = go.Figure(go.Pie(
            labels=party_labels,
            values=party_counts,
            textinfo='percent',
            textposition='inside',
        ))
        pie_height = max(500, len(party_labels) * 22 + 120)
        fig2.update_layout(
            title='Distribution of Voters by Party Affiliation',
            height=pie_height,
            legend=dict(
                orientation='v',
                x=1.0, xanchor='left',
                y=1.0, yanchor='top',
                font=dict(size=11),
                tracegroupgap=0,
            ),
            margin=dict(l=20, r=180, t=50, b=20),
        )
        ctx['party_graph'] = plot(fig2, output_type='div', include_plotlyjs=False)

        # election participation histogram
        election_counts = [qs.filter(**{f: True}).count() for f in ELECTION_FIELDS]
        fig3 = go.Figure(go.Bar(x=ELECTION_LABELS, y=election_counts))
        fig3.update_layout(title='Voter Participation by Election',
                           xaxis_title='Election', yaxis_title='Count')
        ctx['election_graph'] = plot(fig3, output_type='div', include_plotlyjs=False)

        return ctx
