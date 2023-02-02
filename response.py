from voice import talk


def generate_response(action_data, order_data):
    from main import menu, menu_ingredients
    response = ''
    is_checkout = False
    for action in action_data:
        if action.get('objective'):
            intention = action['intention']
            if intention == 'add':
                response += f"I've added {action['amount']} {action['objective']} to your order. \n"
            elif intention == 'remove':
                response += f"I've deleted {action['objective']} from your order. \n"
            elif intention == 'menu':
                response += f"Here is today's menu: {', '.join(menu)}. \n"
            elif intention == 'ingredients':
                response += f"Here are ingredients for {action['objective']}: {', '.join(menu_ingredients[action['objective']])}. \n"
            elif intention == 'checkout':
                is_checkout = True

    if is_checkout:
        response += "Here is your order: \n"
        for item, value in order_data.items():
            response += f"\t{item}: {value},\n"
        response = response[:-2]
        response += '.\n'
    else:
        response += '\nAnything else you want?\n'
    print('response = ', response)

    talk(response)

    return is_checkout