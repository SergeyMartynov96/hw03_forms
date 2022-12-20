from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Автор проекта'
        context['header'] = ('Привет, я автор')
        context['text'] = (
            'Информация обо мне'
        )
        return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Технологии'
        context['header'] = ('Мои умения')
        context['text'] = ('Текст страницы "Технологии"')
        return context
