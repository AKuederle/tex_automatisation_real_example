import pandas as pd
from utils import get_template, compile_pdf_from_template


def get_cover_abstract_data(path):
    data = pd.read_excel(path, index_col='index')

    ### For Cover page
    blue_items = data[data.color == 'blue'][['item name']]
    yellow_items = data[data.color == 'yellow'][['item name']]

    ### For abstract
    categories = data.category.unique()
    abstract_list = {k:data[data.category == k].T.to_dict() for k in categories}

    return {'blue_items': blue_items, 'yellow_items': yellow_items, 'abstract_list': abstract_list}


all_variables = {}

cover_abstract_data = get_cover_abstract_data('./cover+abstract.xlsx')
all_variables = {**all_variables, **cover_abstract_data}

compile_pdf_from_template('./template/everything.tex', insert_variables=all_variables, out_path='./out.pdf')
