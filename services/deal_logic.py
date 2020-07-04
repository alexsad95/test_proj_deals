import csv
from json import loads 
import dateutil.parser
from django.db.models import Aggregate, CharField, Sum
from rest_framework.renderers import JSONRenderer
from deals.models import Deal


class Concat(Aggregate):
    '''
    Реализация Group_concat для ORM БД SQLite.
    '''
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)


def deals_from_csv(request):
    '''
    Обработка файла deals.csv с запроса в объект.
    '''
    content_type = request.content_type.split(';')[0].strip()
    media_type_params = dict([param.strip().split('=') for param in content_type.split(';')[1:]])
    
    charset = media_type_params.get('charset', 'utf-8')
    dialect = media_type_params.get('dialect', 'excel')

    file_from_field = request.data.get('file', None)
    txt = file_from_field.read().decode(charset)

    csv_table = list(csv.reader(txt.splitlines(), dialect=dialect))
    csv_table = [ line for i, line in enumerate(csv_table) if i > 4 and i < len(csv_table) - 2 ]

    return csv_table


def save_deals_to_db(lst):
    '''
    Сохранение в БД с списка. 
    В идеале сделать её асинхронной или в поток.
    '''
    try: 
        Deal.objects.all().delete()
        for line in lst:
            Deal.objects.create(
                username=line[0],
                item=line[1],
                total=int(line[2]),
                quantity=int(line[3]),
                date=dateutil.parser.isoparse(line[4])
            )
    except Exception as e:
        raise e


def search_gems(lst):
    '''
    Преобразование в список каменей, 
    которые купили как минимум двое из списка 5  клиентов, 
    потративших наибольшую сумму за весь период.
    '''
    copy_lst  = lst[:]
    lst_of_gems = []
    for line in lst:
        for copy_line in copy_lst:
            if copy_line['username'] == line['username']:
                continue
            for gem in line['gems']:
                if gem in copy_line['gems']:
                    lst_of_gems.append(gem)
    for copy_line in copy_lst:
        copy_line['gems'] = list(set(lst_of_gems) & set(copy_line['gems']))

    return copy_lst


def get_deals():
    '''
    Обработка результатов при GET запросе.
    '''
    '''
    Думаю лучше было бы сделать group_concat через raw запрос, так как не нужно делать свой и не качать модули.

    deals = Deal.objects.raw("""
        SELECT id, 
                username,
                sum(total) as sum_total, 
                sum(quantity) as sum_quantity, 
                GROUP_CONCAT(item) as item 
        FROM deals_deal 
        GROUP BY username
        ORDER BY sum_total DESC
        LIMIT 5 """) 
    '''
    try:
        query_set = Deal.objects.values('username').annotate(
            spent_money=Sum('total'),
            gems=Concat('item')
        ).order_by('-spent_money')[:5]
    except Exception as e:
        raise e

    lst_of_result = loads(JSONRenderer().render(query_set).decode())

    for some_dict in lst_of_result:
        some_dict['gems'] = list(set(some_dict['gems'].split(',')))

    lst_of_result = search_gems(lst_of_result)
    return lst_of_result
