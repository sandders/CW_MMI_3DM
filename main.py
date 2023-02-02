from pprint import pprint
from voice import take_command
from input_processing import figure_intentions, fill_action_data, find_objectives


from response import generate_response

menu_ingredients = {
    'burger': ['briosh bread', 'beef patty', 'pickles', 'chopped onions', 'special souse', 'salt', 'pepper'],
    'fries': ['potato', 'salt'],
    'lemonade': ['water', 'ice', 'sugar', 'lemon juice', 'mint'],
    'icecream': ['milk', 'sugar']
}
menu = menu_ingredients.keys()


def command_processing(command):
    print(command)
    action_data = []
    for i in ('and', '.', '!', '?'):
        command = command.replace(i, ',')
    particles = command.split(',')
    try:
        particles.remove('')
        particles.remove(' ')
    except:
        pass
    for particle in particles:
        action_data.append(figure_intentions(particle))
    action_data = fill_action_data(action_data)

    action_data, ORDER_DATA = find_objectives(action_data)

    pprint(action_data)
    pprint(ORDER_DATA)

    is_checkout = generate_response(action_data, ORDER_DATA)

    return is_checkout


def run_olexa():
    command = take_command()
    #command = "what is in the menu what are burger ingredients i will have two burgers three fries and a lemonade that's all"
    #command = model.restore_punctuation(command)
    is_checkout = command_processing(command)
    return is_checkout



if __name__ == "__main__":
    is_checkout = False
    while not is_checkout:
        is_checkout = run_olexa()
