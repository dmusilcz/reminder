from django.shortcuts import render, get_object_or_404
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from users.widgets import FengyuanChenDatePickerInput
from .models import Category, Document

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        documents = Document.objects.filter(author=request.user)
        return render(request, 'main/home.html', {'doc_num': len(documents)})
    else:
        return render(request, 'main/home.html')
    # return render(request, 'main/home.html')


def calendar(request):
    return render(request, 'main/calendar.html')


class UserDocsView(LoginRequiredMixin, ListView):
    model = Document
    context_object_name = 'docs'
    paginate_by = 20

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Document.objects.filter(author=user).order_by('name')

    # def get_context_data(self, **kwargs):
    #     kwargs['reminders'] = self.get_
    #     return super().get_context_data(**kwargs)


class UserCategoriesView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Category.objects.filter(author=user).order_by('name')


class DocCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['name', 'desc', 'category', 'expiry_date', 'reminder']

    def get_form(self, *args, **kwargs):
        form = super(DocCreateView, self).get_form(*args, **kwargs)
        form.fields['category'].queryset = Category.objects.filter(author=self.request.user)
        #form.fields['expiry_date'].widget = forms.SelectDateWidget()
        form.fields['expiry_date'] = forms.DateField(input_formats=['%d/%m/%Y'], widget=FengyuanChenDatePickerInput(), required=False)
        form.fields['reminder'] = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=((1, '1 day'),
                    (2, '3 days'),
                    (3, '1 week'),
                    (4, '2 weeks'),
                    (5, '1 month'),
                    (6, '3 months'),
                    (7, '6 months')))
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'desc']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# @login_required
# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     if request.method == 'POST':
#         form = NewTopicForm(request.POST)
#         if form.is_valid():
#             topic = form.save(commit=False)
#             topic.board = board
#             topic.starter = request.user
#             topic.save()
#             Post.objects.create(
#                 message=form.cleaned_data.get('message'),
#                 topic=topic,
#                 created_by=request.user
#             )
#             return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
#     else:
#         form = NewTopicForm()
#     return render(request, 'new_topic.html', {'board': board, 'form': form})