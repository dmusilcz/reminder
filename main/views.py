from django.shortcuts import render, redirect, reverse, get_object_or_404
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from users.widgets import FengyuanChenDatePickerInput
from .models import Category, Document, ReminderChoices
# from .filters import DocFilter
from .forms import SearchForm

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
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Document.objects.filter(author=user).order_by('name')

    # def get_context_data(self, **kwargs):
    #     kwargs['reminders'] = self.get_
    #     return super().get_context_data(**kwargs)

# @login_required
# def search(request):
#     user = get_object_or_404(User, username=request.user)
#     doc_list = Document.objects.filter(author=user).order_by('name')
#     doc_filter = DocFilter(request.GET, queryset=doc_list, request=request)
#     return render(request, 'main/docs_filter.html', {'docs': doc_filter})


@login_required
def search(request):
    user = get_object_or_404(User, username=request.user)
    doc_list = Document.objects.filter(author=user).order_by('name')
    data = dict()
    if request.method == 'POST':
        form = SearchForm(data=request.POST, request=request)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            desc = form.cleaned_data.get("desc")
            categories = form.cleaned_data.get("category")
            reminders = form.cleaned_data.get('reminder')
            expiry_date_from = form.cleaned_data.get("expiry_date_from")
            expiry_date_to = form.cleaned_data.get("expiry_date_to")

            doc_list = doc_list.filter(name__icontains=name).filter(desc__icontains=desc)
            if categories:
                if '0' in categories:
                    null_cats = doc_list.filter(category__isnull=True)
                    categories.remove('0')
                    if categories:
                        doc_list = doc_list.filter(category__in=categories) | null_cats
                    else:
                        doc_list = null_cats
                else:
                    doc_list = doc_list.filter(category__in=categories)

            if reminders:
                if '0' in reminders:
                    null_rems = doc_list.filter(reminder__isnull=True)
                    reminders.remove('0')
                    if reminders:
                        doc_list = doc_list.filter(reminder__in=reminders) | null_rems
                    else:
                        doc_list = null_rems
                else:
                    doc_list = doc_list.filter(reminder__in=reminders)

            if expiry_date_from and expiry_date_to:
                doc_list = doc_list.filter(expiry_date__gte=expiry_date_from).filter(expiry_date__lte=expiry_date_to)
            elif expiry_date_from:
                doc_list = doc_list.filter(expiry_date__gte=expiry_date_from)
            elif expiry_date_to:
                doc_list = doc_list.filter(expiry_date__lte=expiry_date_to)

            page = request.GET.get('page', 1)
            paginator = Paginator(doc_list, 10)
            try:
                doc_list = paginator.page(page)
            except PageNotAnInteger:
                doc_list = paginator.page(1)
            except EmptyPage:
                doc_list = paginator.page(paginator.num_pages)

            context = {'docs': doc_list}
            data['form_is_valid'] = True
            data['html_docs_list'] = render_to_string('main/includes/partial_docs_list.html', context, request=request)

        else:
            context = {'form': form}
            data['html_form'] = render_to_string('main/includes/search_form.html', context, request=request)
    else:
        form = SearchForm(request=request)
        context = {'form': form}
        data['html_form'] = render_to_string('main/includes/search_form.html', context, request=request)
    return JsonResponse(data)


@login_required
def search2(request):
    user = get_object_or_404(User, username=request.user)
    doc_list = Document.objects.filter(author=user).order_by('name')
    if request.method == 'POST':
        form = SearchForm(data=request.POST, request=request)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            desc = form.cleaned_data.get("desc")
            categories = form.cleaned_data.get("category")
            reminders = form.cleaned_data.get('reminder')
            expiry_date_from = form.cleaned_data.get("expiry_date_from")
            expiry_date_to = form.cleaned_data.get("expiry_date_to")

            doc_list = doc_list.filter(name__icontains=name).filter(desc__icontains=desc)
            if categories:
                if '0' in categories:
                    null_cats = doc_list.filter(category__isnull=True)
                    categories.remove('0')
                    if categories:
                        doc_list = doc_list.filter(category__in=categories) | null_cats
                    else:
                        doc_list = null_cats
                else:
                    doc_list = doc_list.filter(category__in=categories)

            if reminders:
                if '0' in reminders:
                    null_rems = doc_list.filter(reminder__isnull=True)
                    reminders.remove('0')
                    if reminders:
                        doc_list = doc_list.filter(reminder__in=reminders) | null_rems
                    else:
                        doc_list = null_rems
                else:
                    doc_list = doc_list.filter(reminder__in=reminders)

            if expiry_date_from and expiry_date_to:
                doc_list = doc_list.filter(expiry_date__gte=expiry_date_from).filter(expiry_date__lte=expiry_date_to)
            elif expiry_date_from:
                doc_list = doc_list.filter(expiry_date__gte=expiry_date_from)
            elif expiry_date_to:
                doc_list = doc_list.filter(expiry_date__lte=expiry_date_to)

            render(request, 'main/docs_filter2.html', {'form': form, 'docs': doc_list})
    else:
        form = SearchForm(request=request)
    return render(request, 'main/docs_filter2.html', {'form': form, 'docs': doc_list})


class DocCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['name', 'desc', 'category', 'expiry_date', 'reminder']

    def get_form(self, *args, **kwargs):
        ids = [choice.id for choice in ReminderChoices.objects.filter(author=self.request.user).order_by('id')]
        form = super(DocCreateView, self).get_form(*args, **kwargs)
        form.fields['category'].queryset = Category.objects.filter(author=self.request.user)
        form.fields['expiry_date'] = forms.DateField(input_formats=['%m/%d/%Y'], widget=FengyuanChenDatePickerInput(), required=False, help_text='Reminders can be chosen once this field is not empty')
        form.fields['reminder'] = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=((id, time) for id, time in zip(ids, ('1 day', '3 days', '1 week', '2 weeks', '1 month', '3 months', '6 months'))))

        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        # form.save()
        return super().form_valid(form)


class DocDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Document
    fields = ['name', 'desc', 'category', 'expiry_date', 'reminder']
    template_name = 'main/document_detail.html'
    context_object_name = 'doc'

    def get(self, request, **kwargs):
        try:
            self.model.objects.get(pk=kwargs['pk'])
            return super(DocDetailView, self).get(request, **kwargs)
        except self.model.DoesNotExist:
            return redirect(reverse('docs'))

    def test_func(self):
        try:
            document = self.get_object()
        except:
            return redirect(reverse('docs'))
        if self.request.user == document.author:
            return True
        return False


class DocUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Document
    fields = ['name', 'desc', 'category', 'expiry_date', 'reminder']
    template_name = 'main/document_update_form.html'
    context_object_name = 'doc'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_form(self, *args, **kwargs):
        ids = [choice.id for choice in ReminderChoices.objects.filter(author=self.request.user).order_by('id')]
        form = super(DocUpdateView, self).get_form(*args, **kwargs)
        form.fields['category'].queryset = Category.objects.filter(author=self.request.user)
        form.fields['expiry_date'] = forms.DateField(input_formats=['%m/%d/%Y'], widget=FengyuanChenDatePickerInput(), required=False, help_text='Reminders can be chosen once this field is not empty')
        # form.fields['reminder'] = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=((id, time) for id, time in zip(ids, ('1 day', '3 days', '1 week', '2 weeks', '1 month', '3 months', '6 months'))))
        form.fields['reminder'].widget = forms.CheckboxSelectMultiple()
        # form.fields['reminder'] = forms.MultipleChoiceField(required=False)
        # form.fields['reminder'] = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple(attrs={}, ), choices=((1, '1 day'),
        #             (2, '3 days'),
        #             (3, '1 week'),
        #             (4, '2 weeks'),
        #             (5, '1 month'),
        #             (6, '3 months'),
        #             (7, '6 months')),)
        # form.fields['reminder'] = forms.ModelMultipleChoiceField(required=False, queryset=self.get_object().reminder.all(), )
        # form.fields['reminder'] = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple(attrs={}, ), queryset=self.get_object().reminder.all(), )
        # form.fields['reminder'] = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple())
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        document = self.get_object()
        if self.request.user == document.author:
            return True
        return False

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        if request.POST['expiry_date'] == '' and 'reminder' in request.POST:
            request.POST.pop('reminder')
        return super(DocUpdateView, self).post(request, **kwargs)


@login_required
def doc_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    data = dict()
    view = request.GET.get('view', 'D')
    if request.method == 'POST' and request.user == doc.author:
        doc_id = str(pk)
        doc.delete()
        # user = get_object_or_404(User, username=request.user)
        # docs = Document.objects.filter(author=user).order_by('name')
        data['form_is_valid'] = True
        data['doc_id'] = '#doc_' + doc_id
        data['view'] = view
        # redirect('home')
    else:
        context = {'doc': doc,
                   'view': view}
        data['html_form'] = render_to_string('main/includes/partial_doc_delete.html', context, request=request)
    return JsonResponse(data)


class UserCategoriesView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'cats'
    paginate_by = 20

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Category.objects.filter(author=user).order_by('name')


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'desc']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Category
    fields = ['name', 'desc']
    template_name = 'main/category_detail.html'
    context_object_name = 'cat'

    def get(self, request, **kwargs):
        try:
            self.model.objects.get(pk=kwargs['pk'])
            return super(CategoryDetailView, self).get(request, **kwargs)
        except self.model.DoesNotExist:
            return redirect(reverse('categories'))

    def test_func(self):
        try:
            cat = self.get_object()
        except:
            return redirect(reverse('categories'))
        if self.request.user == cat.author:
            return True
        return False


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name', 'desc']
    template_name = 'main/category_update_form.html'
    context_object_name = 'cat'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        cat = self.get_object()
        if self.request.user == cat.author:
            return True
        return False


@login_required
def cat_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    data = dict()
    if request.method == 'POST' and request.user == cat.author:
        cat_id = str(pk)
        cat.delete()
        # user = get_object_or_404(User, username=request.user)
        # docs = Document.objects.filter(author=user).order_by('name')
        data['form_is_valid'] = True
        data['cat_id'] = '#cat_' + cat_id
        # redirect('home')
    else:
        context = {'cat': cat}
        data['html_form'] = render_to_string('main/includes/partial_cat_delete.html', context, request=request)
    return JsonResponse(data)

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