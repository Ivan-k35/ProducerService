import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from confluent_kafka import Producer
from loguru import logger

from .serializers import PurchaseCheckSerializer


def send_to_kafka(data):
    p = Producer({'bootstrap.servers': 'kafka:9092'})

    def delivery_report(err, msg):
        if err is not None:
            logger.error('Сбой доставки сообщения: {}'.format(err))
        else:
            logger.info('Сообщение успешно доставлено в {} [{}]'.format(msg.topic(), msg.partition()))

    try:
        topic = 'purchase_checks'
        p.produce(topic, json.dumps(data).encode('utf-8'), callback=delivery_report)
        p.flush()
        logger.info("Сообщение успешно отправлено в Kafka.")
    except Exception as e:
        logger.exception(f"Ошибка при обработке сообщения Kafka: {e}")

    p.flush()


class PurchaseCheckView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
            Создает новую запись о проверке чеков покупок и отправляет данные в Kafka.

            Пример тела запроса:
            {
                "transaction_id": "unique_transaction_id247",
                "timestamp": "2024-02-07T12:34:56",
                "place_id": "unique_place_id7",
                "place_name": "Store ABCS",
                # Другие поля
            }

            Пример успешного ответа:
            HTTP 201 Created

            {
                "id": 1,
                "transaction_id": "unique_transaction_id247",
                "timestamp": "2024-02-07T12:34:56+03:00",
                # Другие поля
            }

            Пример ответа с ошибкой:
            HTTP 400 Bad Request
            {
                "error": "Некорректные данные"
            }
        """
        serializer = PurchaseCheckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'serializer.data send {serializer.data}')
            send_to_kafka(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
