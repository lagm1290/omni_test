from apps.shop.models import Product


class ShopQueries:
    @staticmethod
    def product_payment(status=None):
        return Product.objects.raw("""
                SELECT sp.id as id, so.number as order,sp.number as payment,
                   spo.value,sp.date_confirm 
                FROM shop_payment as sp inner join shop_payment_order as spo 
                    on sp.id=spo.payment_id inner join shop_order as so 
                    on spo.order_id = so.id 
                WHERE sp.status='{}'
                """.format(status)
                                   )

    @staticmethod
    def product_send(status=None):

        return Product.objects.raw(
            """
                  SELECT so.id as id, so.number as order,ss.number as shipment,
                   ss.name_received as name , ss.date_received as date, 
                   ss.mobile_phone_received as mobile_phone,
                   ss.direction_received as direction,
                   ss.city_received as city,
                   ss.postal_code_received as postal_code
                   FROM
                    shop_order as so inner join shop_shipment as ss
                    on so.id=ss.order_id
                   WHERE ss.status in ('{}')
            """.format("','".join(map(str,status)))
        )
