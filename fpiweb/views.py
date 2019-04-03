"""
views.py - establish the views (pages) for the F. P. I. web application.
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, \
    CreateView, UpdateView, DeleteView

from forms import ConstraintsForm
from fpiweb.models import Constraints


def index(request):
    """
    Build index.html web page.

    :param request:
    :return:
    """

    response = HttpResponse("Hello world from Food Pantry Inventory.")
    return response


class AboutView(TemplateView):
    """
    The About View for this application.
    """
    template_name = 'fpiweb/about.html'


class ConstraintsListView(ListView):
    """
    List of existing constraints.
    """
    model = Constraints
    template_name = 'fpiweb/constraints_list.html'
    context_object_name = 'constraints_list_content'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Add additional content to the context dictionary.

        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(ConstraintsListView, self).get_context_data()

        context['project_type'] = 'open source'

        # provide additional information
        INT_RANGE = Constraints.INT_RANGE
        CHAR_RANGE = Constraints.CHAR_RANGE
        range_list = [INT_RANGE, CHAR_RANGE]
        context['range_list'] = range_list

        return context


class ConstraintDetailView(DetailView):
    """
    Show details of a constraint using a generic DetailView.
    """
    model = Constraints
    template_name = 'fpiweb/constraint_detail.html'
    context_object_name = 'constraint_detail_context'
    constraint = 'ConstraintID'

    def get_context_data(self, **kwargs):
        """
        Add additional content to the context.

        :param kwargs:
        :return: context
        """
        context = super(ConstraintDetailView, self).get_context_data()

        # provide additional information
        # ConstraintID = context['id']
        constraint = context['object']

        # add puzzles
        constraint_info = Constraints.objects.filter(
            constraint_id__exact=Constraints.ConstraintID
        )

        # add stuff back to context
        context['constraint'] = constraint
        context['constraint_info'] = constraint_info

        return context


class ConstraintCreateView(CreateView):
    """
    Create an animal or daily quest using a generic CreateView.
    """
    model = Constraints
    template_name = 'fpiweb/constraint_edit.html'
    context_object_name = 'constraint_edit_context'

    formClass = ConstraintsForm

    # TODO Why are fields required here in the create - 1/18/17
    fields = ['ConstraintName', 'ConstraintDescr', 'ConstraintType',
              'ConstraintMin', 'ConstraintMax', 'ConstraintList', ]

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(ConstraintCreateView, self).get_context_data(**kwargs)
        context['action'] = reverse('fpiweb:constraint_new')
        return context

    def get_success_url(self):
        """
        Run once form is successfully validated.

        :return:
        """
        results = reverse('fpiweb:constraints_view')
        return results


class ConstraintUpdateView(UpdateView):
    """
    Update an animal or daily quest using a generic UpdateView.
    """

    model = Constraints
    template_name = 'fpiweb/constraints_edit.html'
    context_object_name = 'constraints_edit_context'

    form_class = ConstraintsForm

    # TODO Why are fields forbidden here in the update - 1/18/17
    # fields = ['category', 'constraints_order', 'constraints_name', 'date_started', ]

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(ConstraintsUpdateView, self).get_context_data(**kwargs)
        context['action'] = reverse('fpiweb:constraints_update',
                                    kwargs={'pk': self.get_object().id})
        return context

    def get_success_url(self):
        """
        Set the next URL to use once the edit is successful.
        :return:
        """

        results = reverse('fpiweb:constraints_view')
        return results


class ConstraintDeleteView(DeleteView):
    """
    Delete an animal or daily quest using a generic DeleteView.
    """
    model = Constraints
    template_name = 'fpiweb/constraints_delete.html'
    context_object_name = 'constraints_delete_context'

    def get_success_url(self):
        """
        Set the next URL to use once the delete is successful.
        :return:
        """

        results = reverse('fpiweb:constraints_view')
        return results

# EOF
