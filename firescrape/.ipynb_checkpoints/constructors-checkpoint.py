"""
Imports
"""
import os
import git
import pandas as pd


"""
General Helpers
"""
def write_string_to_file(string, filepath):
    with open(filepath, 'w') as out:
        out.write(string)
        
    return
        

"""
File Constructors
"""
def format_lists(list_a, list_b=[]):
    if list_b != []:
        return sorted(list(set(list_a) + set(list_b)))
    else:
        return sorted(list(set(list_a)))
    
def construct_yml_str(env_name, env_yml_section_to_items, env_yml_section_to_offset):
    yml_str = f'name: {env_name}\n\n'

    for section in env_yml_section_to_items.keys():
        section_offset = env_yml_section_to_offset[section]
        separator = f"\n{section_offset*' '}- "

        if section_offset > 2:
            section_prefix = f"{(section_offset-4)*' '}- "
        else:
            section_prefix = ''

        section_str = f'{section_prefix}{section}:{separator}{separator.join(env_yml_section_to_items[section])}'
        yml_str += f'{section_str}\n\n'
        
    return yml_str
    
def create_environment_yml(env_name, python_version='3.7', dependencies=[], pip=[], channels=[]):
    # Defining section item defaults
    default_channels = ['conda-forge']
    default_dependencies = [f'python={python_version}', 'pip', 'pandas', 'matplotlib', 'jupyterlab', 'seaborn', 'lxml', 'xmltodict', 'beautifulsoup4', 'html5lib', 'python-dotenv']
    default_pip = ['ipypb', 'feautils']
    
    # Defining section whitespace offset
    env_yml_section_to_offset = {
        'channels': 2, 
        'dependencies': 2, 
        'pip': 6
    }
    
    # Adding any passed section items
    locals_ = locals()
    env_yml_section_to_items = {
        section: format_lists(locals_[f'default_{section}'], locals_[section]) 
        for section in env_yml_section_to_offset.keys()
    }
    
    # Creating and saving environment.yml file
    yml_str = construct_yml_str(env_name, env_yml_section_to_items, env_yml_section_to_offset)
    write_string_to_file(yml_str, 'environment.yml')
    
    return 

def create_readme_md(proj_name, 
                     dt_section=True,
                     dt_prefix='Last updated: ', 
                     dt_format='%Y-%m-%d %H:%M'):
    
    readme_text = f"# {proj_name.replace('-', ' ')}"
    
    if dt_section == True:
        readme_text += f'\n\n{dt_prefix}{pd.Timestamp.now().strftime(dt_format)}'
    
    with open('README.md', 'w') as readme:
        readme.write(readme_text)
        
    return

def create_gitignore(include_env_vars=False):
    default_ignores = ['.ipynb_checkpoints']
    
    if include_env_vars == True:
        default_ignores += ['.env']
    
    gitignore_text = '\n'.join(default_ignores)
    
    with open('.gitignore', 'w') as readme:
        readme.write(gitignore_text)
        
    return

def create_batch_scripts(env_name, batch_scripts_dir='batch_scripts'):
    script_name_to_commands = {
        'launch_lab': [
            'cd ..',
            f'conda activate {env_name}',
            'jupyter lab'
        ],
        'setup_env': [
            'cd ..',
            'conda env create -f environment.yml',
            f'conda activate {env_name}',
            f'ipython kernel install --user --name={env_name}'
        ],
        'update_env': [
            'cd ..',
            f'conda activate {env_name}',
            'conda env update --file environment.yml'
        ],
    }

    if not os.path.exists(batch_scripts_dir):
        os.makedirs(batch_scripts_dir)

    sep = '\ncall '

    for script_name, commands in script_name_to_commands.items():
        batch_commands_str = f"call {sep.join(commands)}" + '\npause'
        write_string_to_file(batch_commands_str, f'{batch_scripts_dir}/{script_name}.bat')
        
    return 

def create_dot_env(include_env_vars):
    if include_env_vars == True:
        write_string_to_file('', '.env')
        
    return


"""
Set-Up Wrapper
"""
def setup_project(proj_name, proj_path='.', env_name=None, include_env_vars=False, python_version='3.7', dependencies=[], pip=[], channels=[]):
    # Cleaning names
    proj_name = proj_name.replace(' ', '-')
    
    if env_name is None:
        env_name = proj_name.replace('-', '').replace(' ', '')
        
    # Creating and entering project directory
    proj_dir = f'{proj_path}/{proj_name}'
    
    if not os.path.exists(proj_dir):
        os.makedirs(proj_dir)
        
    os.chdir(proj_dir)
    
    # Creating files     
    create_environment_yml(env_name, python_version=python_version, dependencies=dependencies, pip=pip, channels=channels)
    create_readme_md(proj_name)
    create_gitignore(include_env_vars=include_env_vars)
    create_dot_env(include_env_vars)
    create_batch_scripts(env_name)
    
    # Returning to original directory
    os.chdir('/'.join(proj_dir.count('/')*['..']))
    
    # Initialising it as a Git repo
    git.Repo.init(proj_dir)
    
    return