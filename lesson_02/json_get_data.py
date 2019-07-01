import json

inp_item = 'book'
inp_quantity = '5'
inp_price = '100'
inp_buyer = 'Petr'
inp_date = '15.08.2018'
tmp_dict = {
    'orders': [],
}


def write_order_to_json(item, quantity, price, buyer, date):
    tmp_dict['orders'].append(
        {
            'Item': item,
            'Quantity': quantity,
            'Price': price,
            'Buyer': buyer,
            'Date': date,
        }
    )
    with open('orders.json', 'w') as file:
        json.dump(tmp_dict, file, indent=4, sort_keys=True)
        print(json.dumps(tmp_dict, indent=4, sort_keys=True))


if __name__ == '__main__':
    write_order_to_json(inp_item, inp_quantity, inp_price, inp_buyer, inp_date)
    write_order_to_json('chair', 3, 15, 'Vasilij', '12.07.2018')
