from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views    import APIView
from rest_framework.parsers  import FileUploadParser

from .models import Deal
from .serializers import DealSerializer, \
                         DealGetSerializer 
from services.deal_logic import deals_from_csv, \
                                save_deals_to_db, \
                                get_deals


class DealView(APIView):
    parser_classes = [FileUploadParser]
    
    def post(self, request):
        '''
        Принимает с помощью запроса файл CSV, преобразует его и сохраняет в БД.
        '''
        try:
            csv_table = deals_from_csv(request)
            save_deals_to_db(csv_table)

            return Response({ 'Status': 'OK' })
        except Exception as e:
            return Response({ 
                'Status': 'Error',
                'Desc': f'{e} - в процессе обработки файла произошла ошибка'
            })

    @method_decorator(cache_page(60*60*2))
    def get(self, request):
        '''
        Вывод списка из 5 клиентов, потративших наибольшую сумму за весь период.
        '''
        try:
            query_set = get_deals()
            serializer = DealGetSerializer(query_set, many=True)
            return Response({ 'response': serializer.data })
        except Exception as e:
            return Response({ 
                'Status': 'Error',
                'Desc': f'{e} - в процессе обработки произошла ошибка'
            })