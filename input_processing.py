from word2number import w2n
from nltk.tokenize import word_tokenize
import nltk

ORDER_DATA = {}

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def figure_intentions(particle):
    data = {'particle': particle}
    if ('do' in particle and 'have' in particle) or \
            'menu' in particle:
        data['intention'] = 'menu'
    elif 'have' in particle or \
            'add' in particle:
        data['intention'] = 'add'
    elif (('do not' in particle or "don't" in particle) and 'want' in particle) or \
            'remove' in particle or \
            'delete' in particle:
        data['intention'] = 'remove'
    elif ('what' in particle and 'is' in particle) or \
            'ingredients' in particle or \
            'consist' in particle:
        data['intention'] = 'ingredients'
    elif ('that' in particle and 'all' in particle) or \
            'receipt' in particle:
        data['intention'] = 'checkout'
    else:
        data['intention'] = None

    return data


def fill_none_values(lst):
    last_non_none = None
    for i, item in enumerate(lst):
        if item['intention'] is not None:
            last_non_none = item['intention']
        else:
            lst[i]['intention'] = last_non_none
    return lst


def fill_action_data(actions):
    actions = fill_none_values(actions)
    return actions


def extract_number_from_string(string):
    tokens = word_tokenize(string)
    tagged = nltk.pos_tag(tokens)
    for word, tag in tagged:
        if tag == 'CD':
            return w2n.word_to_num(word)
    return None


def find_objectives_add(action):
    from main import menu
    global ORDER_DATA
    number = extract_number_from_string(action['particle'])
    if not number:
        number = 1
    for i in menu:
        if i in action['particle']:
            ORDER_DATA[i] = number
            action['objective'] = i
            action['amount'] = number
            return action
    action['objective'] = None
    return action


def find_objectives_ingredients(action):
    from main import menu
    for i in menu:
        if i in action['particle']:
            action['objective'] = i
            return action
    action['objective'] = None
    return action


def find_objectives_menu(action):
    action['objective'] = 'menu'
    return action


def find_objectives_checkout(action):
    action['objective'] = 'checkout'
    return action


def find_objectives_remove(action):
    from main import menu
    global ORDER_DATA
    for i in menu:
        if i in action['particle']:
            ORDER_DATA.pop(i)
            action['objective'] = i
            return action
    action['objective'] = None
    return action


ACTION_MAPPING = {
    'add': find_objectives_add,
    'remove': find_objectives_remove,
    'ingredients': find_objectives_ingredients,
    'menu': find_objectives_menu,
    'checkout': find_objectives_checkout
}


def find_objectives(action_data):
    action_new_data = []
    for action in action_data:
        if action['intention'] and action['intention'] in ACTION_MAPPING.keys():
            action_new_data.append(ACTION_MAPPING[action['intention']](action))
        else:
            action_new_data.append(action)
    return action_new_data, ORDER_DATA