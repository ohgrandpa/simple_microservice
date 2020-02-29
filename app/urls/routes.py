from app.views import main


def add_routes(app):
    app.add_url_rule('/populate_database',
                     'populate_database',
                     view_func=main.populate_database,
                     methods=['POST'])

    app.add_url_rule('/',
                     'index',
                     view_func=main.index,
                     methods=['GET'])

    app.add_url_rule('/add_item',
                     'add_item',
                     view_func=main.add_item_to_order,
                     methods=['POST'])

    app.add_url_rule('/total',
                     'total',
                     view_func=main.get_order_total,
                     methods=['GET'])