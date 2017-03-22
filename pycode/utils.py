import re
import jinja2
import os
import shutil

def get_template(template_file):
    """Get a jinja template with latex tags.

    modified from http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
    """
    latex_jinja_env = jinja2.Environment(
    	block_start_string = '\BLOCK{',
    	block_end_string = '}',
    	variable_start_string = '\VAR{',
    	variable_end_string = '}',
    	comment_start_string = '\#{',
    	comment_end_string = '}',
    	line_statement_prefix = '%%',
    	line_comment_prefix = '%#',
    	trim_blocks = True,
    	autoescape = False,
    	loader = jinja2.FileSystemLoader(['/',os.path.abspath('./template')])
    )
    template = latex_jinja_env.get_template(os.path.abspath(template_file))
    return template

def compile_pdf_from_template(template_file, insert_variables, out_path):
    """Render a template file and compile it to pdf"""
    out_path = os.path.abspath(out_path)
    template_file = os.path.abspath(template_file)

    # Get and render the template based on the path to the tempalte file.
    template = get_template(template_file)
    rendered_template = template.render(**insert_variables)

    # Save the rendered_template in the same folder as the template file as tmp.tex
    temp_d = os.path.dirname(template_file)
    temp_out = os.path.join(temp_d, "tmp")
    with open(temp_out+'.tex', "w") as f:  # saves tex_code to output file
        f.write(rendered_template)

    # Call latex to compile tmp.tex
    os.chdir(temp_d) # change directory into the template folder to fix relative path issues inside the latex file
    os.system('pdflatex {}'.format(temp_out+'.tex'))
    shutil.copy2(temp_out+".pdf", out_path)
