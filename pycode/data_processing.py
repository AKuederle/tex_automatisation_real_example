import pandas as pd
import re
from utils import get_template, compile_pdf_from_template


def get_options_from_file(path):
    """Read a parameters configuration file. The pattern in the file is '<key>=<value>'
    """
    with open(path, encoding='utf-8') as f:
        content = f.read()
        keys = re.findall(r"(.*?)=.*", content)
        values = re.findall(r".*=(.*?)\s+", content)

    options = dict(zip(keys, values))
    return options


def get_cover_abstract_data(path):
    data = pd.read_excel(path, index_col='index')
    data['icons list'] = data['icons list'].str.split(',')
    data['icons list'] = data['icons list'].fillna('[]')

    ### For Cover page
    blue_items = data[data.color == 'blue'][['item name']].T.to_dict()
    yellow_items = data[data.color == 'yellow'][['item name']].T.to_dict()

    ### For abstract
    categories = data.category.unique()
    abstract_list = {k:data[data.category == k].T.to_dict() for k in categories}
    ordered_abstract_keys = ['languages', 'veggies', 'sports', 'fruits', 'systems', 'planets']
    return {'blue_items': blue_items, 'yellow_items': yellow_items, 'abstract_list': abstract_list, 'ordered_abstract_keys': ordered_abstract_keys}

def get_main_data(path):
    def filter_items(key):
        items = data[data.index == key]
        items_dict = items[['item name', 'item alias', 'brief', 'definition']].iloc[0].to_dict()
        items_dict['subentries'] = list(items.reset_index()[['start', 'icons short list', 'specific description', 'collapse', 'rate']].T.to_dict().values())
        return items_dict

    def filter_categories(key):
        items = data[data.category == key]
        new_keys = items.index.unique()
        return {k:filter_items(k) for k in new_keys}

    data = pd.read_excel(path, index_col='index')
    data['icons short list'] = data['icons short list'].str.split(',')
    data['icons short list'] = data['icons short list'].fillna('[]')
    data['brief'] = data['brief'].fillna('')
    data['definition'] = data['definition'].fillna('')

    ### For main
    categories = data.category.unique()
    # when checked with Lint, line 53 treated as useless. Get the same layout when removing line 53
    items = data.index.unique()
    main_list = {k:filter_categories(k) for k in categories}

    return {'main_list': main_list}


all_variables = {}

customer_data = get_options_from_file('./parameters_config.txt')
all_variables =  {**all_variables, **customer_data}

cover_abstract_data = get_cover_abstract_data('./cover+abstract.xlsx')
all_variables = {**all_variables, **cover_abstract_data}

main_data = get_main_data('./main.xlsx')
all_variables = {**all_variables, **main_data}

compile_pdf_from_template('./template/everything.tex', insert_variables=all_variables, out_path='./out.pdf')
