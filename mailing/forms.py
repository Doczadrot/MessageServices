from django import forms
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple, ModelForm, widgets
from mailing.models import Message, Client, Mailing


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['topic_message', 'text_message']


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']


class MailingForm(ModelForm):
    """Форма для создания и редактирования рассылки."""
    # Используем ModelMultipleChoiceField для получения объектов и CheckboxSelectMultiple для их отображения
    message = forms.ModelChoiceField(queryset=None, label="Сообщение")
    abonent = ModelMultipleChoiceField(queryset=None, widget=CheckboxSelectMultiple, label="Получатели")

    class Meta:
        model = Mailing
        fields = ['title', 'start_time', 'end_time', 'periodicity', 'status', 'message', 'abonent']
        widgets = {
            # Используем виджеты для удобного выбора даты и времени
            'start_time': widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Динамически фильтруем QuerySet для полей message и abonent по текущему пользователю
        if user:
            self.fields['message'].queryset = Message.objects.filter(user=user)
            self.fields['abonent'].queryset = Client.objects.filter(user=user)

        # Добавляем классы Bootstrap к полям
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите Названия рассылки'})
        self.fields['periodicity'].widget.attrs.update({'class': 'form-select'})
        self.fields['status'].widget.attrs.update({'class': 'form-select'})
