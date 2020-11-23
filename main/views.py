from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.mail import send_mail
from operator import itemgetter
from datetime import datetime, timedelta, tzinfo
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from users.widgets import FengyuanChenDatePickerInput
from .models import Category, Document, ReminderChoice, ReminderThrough
# from .filters import DocFilter
from .forms import SearchForm, DocumentUpdateForm, CategoryUpdateForm, ContactForm
from django.utils.translation import get_language, gettext_lazy as _

# Create your views here.


def home(request):
    print(f'ACTIVE: {request.user.is_active}')
    if request.user.is_authenticated:
        print(f'ACTIVE: {request.user.is_active}')
        if request.user.is_active:
            documents = Document.objects.filter(author=request.user)
            categories = Category.objects.filter(author=request.user)
            today = timezone.localdate()
            documents_count = documents.count()
            categories_count = categories.count()
            next_doc_expiring = documents.order_by('expiry_date').filter(expiry_date__gte=today).first()
            docs_with_sent_reminder = documents.exclude(last_reminder_sent__isnull=True).order_by('-last_reminder_sent')

            reminder_throughs = ReminderThrough.objects.filter(document__in=documents)

            if reminder_throughs.first():
                reminder_dates = [(reminder_throughs.get(id=reminder.id).document, reminder.document.expiry_date - timedelta(days=reminder.get_days_by_id())) for reminder in reminder_throughs]
                future_reminder_dates = sorted([(document, date) for document, date in reminder_dates if date >= today and document not in docs_with_sent_reminder], key=itemgetter(1))
                closest_date = future_reminder_dates[0] if future_reminder_dates else None
                next_reminder_sent_on = [(date, document) for document, date in future_reminder_dates if date == closest_date[1]] if closest_date else None
            else:
                next_reminder_sent_on = None

            last_reminder_sent_on = docs_with_sent_reminder.first().get_last_reminder_sent() if docs_with_sent_reminder else None
            documents_expired = documents.filter(expiry_date__lt=today).count()
            docs_expired_in_1_month = documents.filter(expiry_date__range=(today, today + timedelta(days=30))).count()
            docs_expired_in_6_months = documents.filter(expiry_date__range=(today, today + timedelta(days=183))).count()
            docs_uncategorized = documents.filter(category__isnull=True).count()

            context = {'documents_count': documents_count,
                       'categories_count': categories_count,
                       'next_doc_expiring': next_doc_expiring,
                       'next_reminder_sent_on': next_reminder_sent_on,
                       'last_reminder_sent_on': last_reminder_sent_on,
                       'documents_expired': documents_expired,
                       'docs_expired_in_1_month': docs_expired_in_1_month,
                       'docs_expired_in_6_months': docs_expired_in_6_months,
                       'docs_uncategorized': docs_uncategorized}

            return render(request, 'main/home_user.html', context)
        else:
            return redirect('user_denied')
    else:
        return render(request, 'main/home.html')


# class UserDocsView(LoginRequiredMixin, ListView):
#     model = Document
#     context_object_name = 'docs'
#     paginate_by = 3
#
#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.request.user)
#         searched = self.request.GET.get('searched', None)
#         if searched:
#             doc_pk_list = self.request.session.get('searched_docs_pks', None)
#             return Document.objects.filter(author=user).filter(pk__in=doc_pk_list).order_by('name')
#
#         self.request.session['searched_docs_pks'] = None
#         return Document.objects.filter(author=user).order_by('name')
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         searched = self.request.GET.get('searched', None)
#         if searched:
#             data['searched'] = True
#         return data


@login_required
def user_docs(request):
    print(f'ACTIVE: {request.user.is_active}')
    if request.user.is_active:
        user = get_object_or_404(User, username=request.user)
        searched = request.GET.get('searched', None)
        order, label_sort_by = get_order(request)
        print(order)

        if searched:
            doc_pk_list = request.session.get('searched_docs_pks', None)
            doc_list = Document.objects.filter(author=user).filter(pk__in=doc_pk_list).order_by(order)
        else:
            if request.session.get('searched_docs_pks', None):
                request.session.pop('searched_docs_pks')
            doc_list = Document.objects.filter(author=user).order_by(order)

        print(f'Searched: {searched}')
        print(request.session.get('searched_docs_pks', None))
        page = request.GET.get('page', 1)
        paginator = Paginator(doc_list, 3)
        try:
            doc_list = paginator.page(page)
        except PageNotAnInteger:
            doc_list = paginator.page(1)
        except EmptyPage:
            doc_list = paginator.page(paginator.num_pages)

        context = {'docs': doc_list,
                   'searched': searched,
                   'order': order,
                   'label_sort_by': label_sort_by}

        return render(request, 'main/docs.html', context)
    else:
        return redirect('user_denied')



# @login_required
# def search(request):
#     user = get_object_or_404(User, username=request.user)
#     doc_list = Document.objects.filter(author=user).order_by('name')
#     doc_filter = DocFilter(request.GET, queryset=doc_list, request=request)
#     return render(request, 'main/docs_filter.html', {'docs': doc_filter})


@login_required
def search(request):
    user = get_object_or_404(User, username=request.user)
    if request.user.is_active:
        order, label_sort_by = get_order(request)
        doc_list = Document.objects.filter(author=user).order_by(order)
        data = dict()
        print(order)
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

                request.session['searched_docs_pks'] = [doc.pk for doc in doc_list]

                page = request.GET.get('page', 1)
                paginator = Paginator(doc_list, 3)
                try:
                    doc_list = paginator.page(page)
                except PageNotAnInteger:
                    doc_list = paginator.page(1)
                except EmptyPage:
                    doc_list = paginator.page(paginator.num_pages)

                searched = True
                context = {'docs': doc_list,
                           'searched': searched,
                           'order': order,
                           'label_sort_by': label_sort_by}
                data['form_is_valid'] = True
                data['action'] = 'search'
                data['html_items_list'] = render_to_string('main/includes/partial_docs.html', context, request=request)

            else:
                context = {'form': form,
                           'order': order,
                           'label_sort_by': label_sort_by}
                data['modal_content'] = render_to_string('main/includes/search_form.html', context, request=request)
        else:
            form = SearchForm(request=request)
            context = {'form': form,
                       'order': order,
                       'label_sort_by': label_sort_by}
            data['modal_content'] = render_to_string('main/includes/search_form.html', context, request=request)
        return JsonResponse(data)
    else:
        return redirect('user_denied')

# @login_required
# def search2(request):
#     user = get_object_or_404(User, username=request.user)
#     doc_list = Document.objects.filter(author=user).order_by('name')
#     if request.method == 'POST':
#         form = SearchForm(data=request.POST, request=request)
#         if form.is_valid():
#             name = form.cleaned_data.get("name")
#             desc = form.cleaned_data.get("desc")
#             categories = form.cleaned_data.get("category")
#             reminders = form.cleaned_data.get('reminder')
#             expiry_date_from = form.cleaned_data.get("expiry_date_from")
#             expiry_date_to = form.cleaned_data.get("expiry_date_to")
#
#             doc_list = doc_list.filter(name__icontains=name).filter(desc__icontains=desc)
#             if categories:
#                 if '0' in categories:
#                     null_cats = doc_list.filter(category__isnull=True)
#                     categories.remove('0')
#                     if categories:
#                         doc_list = doc_list.filter(category__in=categories) | null_cats
#                     else:
#                         doc_list = null_cats
#                 else:
#                     doc_list = doc_list.filter(category__in=categories)
#
#             if reminders:
#                 if '0' in reminders:
#                     null_rems = doc_list.filter(reminder__isnull=True)
#                     reminders.remove('0')
#                     if reminders:
#                         doc_list = doc_list.filter(reminder__in=reminders) | null_rems
#                     else:
#                         doc_list = null_rems
#                 else:
#                     doc_list = doc_list.filter(reminder__in=reminders)
#
#             if expiry_date_from and expiry_date_to:
#                 doc_list = doc_list.filter(expiry_date__gte=expiry_date_from).filter(expiry_date__lte=expiry_date_to)
#             elif expiry_date_from:
#                 doc_list = doc_list.filter(expiry_date__gte=expiry_date_from)
#             elif expiry_date_to:
#                 doc_list = doc_list.filter(expiry_date__lte=expiry_date_to)
#
#             render(request, 'main/docs_filter2.html', {'form': form, 'docs': doc_list})
#     else:
#         form = SearchForm(request=request)
#     return render(request, 'main/docs_filter2.html', {'form': form, 'docs': doc_list})


class DocCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Document
    fields = ['name', 'desc', 'category', 'expiry_date', 'reminder']

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return super(DocCreateView, self).get(request, *args, **kwargs)
        else:
            return redirect('user_denied')

    def get_form(self, *args, **kwargs):
        reminder_choices = [(choice.id, choice.field) for choice in ReminderChoice.objects.all().order_by('id')]
        form = super(DocCreateView, self).get_form(*args, **kwargs)
        form.fields['category'].queryset = Category.objects.filter(author=self.request.user)
        form.fields['expiry_date'] = forms.DateField(
            # widget=FengyuanChenDatePickerInput(attrs={'oninput': "verifyDate()",
            #                                                                                    'onload': "verifyDate()",
            #                                                                                    'autocomplete': 'off',}),
                                                     required=False,
                                                     help_text='Reminders can be chosen once this field is not empty'
        )
        form.fields['reminder'] = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                                            choices=reminder_choices)

        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Document added')
        # form.save()
        return super().form_valid(form)

    def test_func(self):
        return Document.objects.filter(author=self.request.user).count() < 100

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        lang = get_language()
        data['lang'] = lang
        data['placeholder'] = {'cs': 'dd.mm.rrrr',
                               'en': 'mm/dd/yyyy'}.get(lang)
        return data


@login_required()
def doc_detail(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    data = dict()

    if request.user == doc.author and request.user.is_active:
        context = {'doc': doc}
        data['action'] = 'detail'
        data['modal_content'] = render_to_string('main/includes/partial_doc_detail.html', context, request=request)

    return JsonResponse(data)


@login_required()
def doc_update(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    order, label_sort_by = get_order(request)
    data = dict()
    lang = get_language()

    if request.user == doc.author and request.user.is_active:
        if request.method == 'POST':
            form = DocumentUpdateForm(request.POST, instance=doc, request=request)
            if form.is_valid():
                print('VALID')
                request.POST = request.POST.copy()
                if request.POST['expiry_date'] == '' and 'reminder' in request.POST:
                    request.POST.pop('reminder')
                form.save()
                data['form_is_valid'] = True

                doc_pk_list = request.session.get('searched_docs_pks', None)
                if doc_pk_list:
                    doc_list = Document.objects.filter(author=request.user).filter(pk__in=doc_pk_list).order_by(order)
                    searched = True
                else:
                    doc_list = Document.objects.filter(author=request.user).order_by(order)
                    searched = False

                page = request.GET.get('page', 1)
                paginator = Paginator(doc_list, 3)
                try:
                    doc_list = paginator.page(page)
                except PageNotAnInteger:
                    doc_list = paginator.page(1)
                except EmptyPage:
                    doc_list = paginator.page(paginator.num_pages)

                messages.success(request, 'Document updated')
                context = {'docs': doc_list,
                           'searched': searched,
                           'order': order,
                           'label_sort_by': label_sort_by}
                data['action'] = 'update'
                data['messages'] = render_to_string('main/includes/messages.html', context,
                                                          request=request)
                data['html_items_list'] = render_to_string('main/includes/partial_docs.html', context,
                                                          request=request)
                # print(data['messages'])
            else:
                print('NOT VALID')
                data['form_is_valid'] = False
        else:
            form = DocumentUpdateForm(instance=doc, request=request)
        placeholder = {'cs': 'dd.mm.rrrr',
                       'en': 'mm/dd/yyyy'}.get(lang)
        context = {'doc': doc,
                   'form': form,
                   'order': order,
                   'label_sort_by': label_sort_by,
                   'lang': lang,
                   'placeholder': placeholder,
                   # 'format': 'dd/mm/yyyy'
                   }
        data['action_update'] = True
        data['modal_content'] = render_to_string('main/includes/partial_doc_update.html', context, request=request)

    return JsonResponse(data)

@login_required
def doc_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    order, label_sort_by = get_order(request)
    data = dict()
    if request.user == doc.author and request.user.is_active:
        if request.method == 'POST':
            doc.delete()
            data['form_is_valid'] = True

            doc_pk_list = request.session.get('searched_docs_pks', None)
            if doc_pk_list:
                if pk in doc_pk_list:
                    doc_pk_list.pop(doc_pk_list.index(pk))
                    request.session['searched_docs_pks'] = doc_pk_list
                doc_list = Document.objects.filter(author=request.user).filter(pk__in=doc_pk_list).order_by(order)
                searched = True
            else:
                doc_list = Document.objects.filter(author=request.user).order_by(order)
                searched = False
            print(f'Searched: {searched}')
            print(len(doc_list))
            print(doc_list)
            page = request.GET.get('page', 1)
            paginator = Paginator(doc_list, 3)
            try:
                doc_list = paginator.page(page)
            except PageNotAnInteger:
                doc_list = paginator.page(1)
            except EmptyPage:
                doc_list = paginator.page(paginator.num_pages)

            context = {'docs': doc_list,
                       'searched': searched,
                       'order': order,
                       'label_sort_by': label_sort_by}
            messages.success(request, 'Document deleted')
            data['action'] = 'delete'
            data['messages'] = render_to_string('main/includes/messages.html', context,
                                                request=request)
            data['html_items_list'] = render_to_string('main/includes/partial_docs.html', context, request=request)
        else:
            context = {'doc': doc,
                       'order': order,
                       'label_sort_by': label_sort_by}
            data['modal_content'] = render_to_string('main/includes/partial_doc_delete.html', context, request=request)
    return JsonResponse(data)


class UserCategoriesView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'cats'
    template_name = 'main/categories.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return super(UserCategoriesView, self).get(request, *args, **kwargs)
        else:
            return redirect('user_denied')

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Category.objects.filter(author=user).order_by('name')


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    fields = ['name', 'desc']

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return super(CategoryCreateView, self).get(request, *args, **kwargs)
        else:
            return redirect('user_denied')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Category added')
        return super().form_valid(form)

    def test_func(self):
        return Category.objects.filter(author=self.request.user).count() < 30


# class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Category
#     fields = ['name', 'desc']
#     template_name = 'main/category_update_form.html'
#     context_object_name = 'cat'
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(author=self.request.user)
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
#
#     def test_func(self):
#         cat = self.get_object()
#         if self.request.user == cat.author:
#             return True
#         return False


@login_required()
def cat_update(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    data = dict()

    if request.user == cat.author and request.user.is_active:
        if request.method == 'POST':
            form = CategoryUpdateForm(request.POST, instance=cat)
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                cat_list = Category.objects.filter(author=request.user).order_by('name')
                context = {'cats': cat_list}
                messages.success(request, 'Category updated')
                data['action'] = 'update'
                data['messages'] = render_to_string('main/includes/messages.html', context, request=request)
                data['html_items_list'] = render_to_string('main/includes/partial_cats.html', context, request=request)
            else:
                data['form_is_valid'] = False
        else:
            form = CategoryUpdateForm(instance=cat)
        context = {'cat': cat,
                   'form': form}
        data['modal_content'] = render_to_string('main/includes/partial_cat_update.html', context, request=request)

    return JsonResponse(data)


@login_required
def cat_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    data = dict()
    if request.user == cat.author and request.user.is_active:
        if request.method == 'POST':
            cat.delete()
            data['form_is_valid'] = True
            cat_list = Category.objects.filter(author=request.user).order_by('name')
            context = {'cats': cat_list}
            messages.success(request, 'Category deleted')
            data['action'] = 'delete'
            data['messages'] = render_to_string('main/includes/messages.html', context, request=request)
            data['html_items_list'] = render_to_string('main/includes/partial_cats.html', context, request=request)
        else:
            context = {'cat': cat}
            data['modal_content'] = render_to_string('main/includes/partial_cat_delete.html', context, request=request)

    return JsonResponse(data)


def get_order(request):
    default_order = 'name'
    order = request.GET.get('o', default_order)
    if order not in ['expiry_date', '-expiry_date',
                     'name', '-name',
                     'category', '-category', ]:
        order = default_order

    sorting_labels = {
        'expiry_date': 'Expiry date increases',
        '-expiry_date': 'Expiry date decreases',
        'name': 'Name (A - Z)',
        '-name': 'Name (Z - A)',
        'category': 'Category name (A - Z)',
        '-category': 'Category name (Z - A)',
    }

    label_sort_by = sorting_labels[order]

    return order, label_sort_by


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request=request, data=request.POST)
        if form.is_valid():
            subject = f"NeverExpire contact form: {form.cleaned_data.get('subject')}"
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            text = f'Sender: User {request.user} ({email})\n\n{message}'
            email_from = settings.CONTACT_FORM_EMAIL
            recipient_list = [settings.ADMINS[0][1], ]

            send_mail(subject, text, email_from, recipient_list)
            messages.success(request, _('Your message was sent'))

            render(request, 'main/contact_form.html', {'form': form})
    else:
        form = ContactForm(request=request)
    return render(request, 'main/contact_form.html', {'form': form})


def terms(request):
    data = dict()
    data['modal_content'] = render_to_string('main/includes/terms_of_use.html', request=request)
    return JsonResponse(data)


def privacy(request):
    data = dict()
    data['modal_content'] = render_to_string('main/includes/privacy_policy.html', request=request)
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