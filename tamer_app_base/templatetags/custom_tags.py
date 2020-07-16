import json

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import escape
from django.utils.safestring import mark_safe, SafeData
from django.utils.text import normalize_newlines

from tamer import settings
import plotly.figure_factory as ff

register = template.Library()


@register.simple_tag
def sidebar_settings(*args, **kwargs):
    sidebar = ''
    view = args[0]
    active = ''
    # for item in view.menu['menu']:
    #     if view.request.path.strip('/') == item['link'].strip('/'):
    #         active = item['sidebar_link']
    active = view.sidebar_link

    for key, value in settings.APPLICATION_SIDEBAR_SETTINGS.items():
        if view.request.path.strip('/') == value['sidebar_link'] or active == value['sidebar_link']:
            sidebar += '<a href="/%s" class ="active" >%s</a>' % (value['sidebar_link'], key)
        else:
            sidebar += '<a href="/%s">%s</a>' % (value['sidebar_link'], key)

    return mark_safe(sidebar)


def navbar_set(request_path, navbar, item):
    active = False
    if item['link'].strip('/') in request_path:
        navbar += '<a href="%s" class ="active" >%s</a>' % (
            item['link'], item['title'])
        active = True
    else:
        navbar += '<a href="%s">%s</a>' % (
            item['link'], item['title'])
    return navbar, active


@register.simple_tag
def navebar_settings(*args, **kwargs):
    navbar = ''
    view = args[0]
    # request_path = [view.request.path.strip('/') + '?' + ', '.join(['%s=%s' % (key, value) for key, value in view.request.GET.items()])]
    if len(view.request.GET.keys()):
        request_path = ['?' + ', '.join(['%s=%s' % (key, value) for key, value in view.request.GET.items()])]
    else:
        request_path = [view.request.path.strip('/'), '.']
        # request_path = [view.request.path.strip('/')]
    for item in view.menu['menu']:
        # title_len = [len(i) for i in item['title'].split('<br/>')]
        # if len(title_len) > 1:
        #     additional_letter = 4
        # elif title_len[0]:
        #     additional_letter = 6
        # else:
        #     continue
        # if view.request.path.strip('/') == item['link'].strip('/'):
        #     navbar += '<div class="vertical-container" style="width:%dch"><div class="vertical-center"><span href="/%s" class ="active bg-dark" >%s</span></div></div>' % (
        #         max(title_len) + additional_letter, item['link'], item['title'])
        # else:
        #     navbar += '<div class="vertical-container" style="width:%dch"><div class="vertical-center"><a href="/%s" class="bg-dark">%s</a></div></div>' % (
        #         max(title_len) + additional_letter, item['link'], item['title'])
        if item.get('subnav', None) is not None:
            submenu = ''
            active_css = ''
            for sub_item in item['subnav']:
                submenu, active = navbar_set(request_path, submenu, sub_item)
                if active:
                    active_css = 'active'

            navbar += '''<div class="tamer-subnav">
            <button class="tamer-subnavbtn %s">%s
              <i class="fa fa-caret-down"></i>
            </button>
            <div class="tamer-subnav-content">
                    ''' % (active_css, item['title'])
            navbar += submenu
            navbar += '</div></div>'
        elif item.get('submenu', None) is not None:
            submenu = ''
            active_css = ''
            for sub_item in item['submenu']:
                submenu, active = navbar_set(request_path, submenu, sub_item)
                if active:
                    active_css = 'active'

            navbar += '''<div class="tamer-dropdown">
    <button class="tamer-dropbtn %s">%s
      <i class="fa fa-caret-down"></i>
    </button>
    <div class="tamer-dropdown-content">
            ''' % (active_css, item['title'])
            navbar += submenu
            navbar += '</div></div>'
        else:
            navbar, active = navbar_set(request_path, navbar, item)
    return mark_safe(navbar)


@register.simple_tag
def gantt(*args, **kwargs):
    df = view = args[0]
    if len(df):
        fig = ff.create_gantt(df, title='', colors=['#333F44', '#93e4c1'], index_col='Complete')
        html = fig.to_html(full_html=False)
        return mark_safe(html)
    else:
        return ''


@register.simple_tag
def detail_view(*args, **kwargs):
    target = ''
    raw_row = '''
    <div class ="row">
        <div class ="col-sm-4 col-form-label">%s</div>
        <div class ="col-sm-8 col-form-label">%s</div>
    </div>'''
    fields = dir(args[0])
    for item in args[0]._meta.fields:
        if item.column in fields:
            try:
                value = args[0].__getattribute__(item.name)
                if type(value) == str:
                    value = value.replace('\n', '<br/>')
                elif type(value) == bool:
                    if value:
                        value = '<i class="fas fa-check"></i>'
                    else:
                        value = ''
                elif value is None:
                    value = 'Отсутствует'
                target += raw_row % (item.verbose_name, value)
            except Exception as e:
                target += raw_row % (item.verbose_name, 'Отсутствует')
    return mark_safe(target)


@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def linebreaksext(value, autoescape=True):
    if value!= '' and value[0] != '<':
        return mark_safe(value.replace('\n', '<br />'))
    return mark_safe(value)


@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def linebreaks_remove(value, autoescape=True):
    autoescape = autoescape and not isinstance(value, SafeData)
    value = normalize_newlines(value)
    if autoescape:
        value = escape(value)
    return mark_safe(value.replace('\\n', ' '))


@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def utf(value, autoescape=True):
    if value != '':
        value = json.loads(value)
    return value

@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def linebreakslink(value, autoescape=True):
    """
    Convert all newlines in a piece of plain text to HTML line breaks
    (``<br />``).
    """
    autoescape = autoescape and not isinstance(value, SafeData)
    value = normalize_newlines(value)
    # if autoescape:
    #     value = escape(value)
    item_list = []
    for item in value.split('\n'):
        start_index = item.find('link<')
        if start_index != -1:
            file_record = item[0:start_index].split(' ')[1]
            start_file_record = item.find(file_record) + 6
            link_str = item[start_index:]
            close_index = link_str.index('>')
            link = link_str[5:close_index]
            replace_string = item[start_file_record:start_index]
            item = item.replace(link, '')
            item = item.replace(replace_string, '<a href="/static/%s">%s</a>' % (link, replace_string)).replace('link<', '').replace('>>', '>')
        item_list.append(item)
    value = '<br>'.join(item_list)

    return mark_safe(value.replace('\\n', ''))