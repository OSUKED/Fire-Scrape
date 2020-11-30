"""
Imports
"""


"""
Creating Environment.yml
"""
def format_lists(list_a, list_b=None):
    if list_b is not None:
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
    
def create_environment_yml(env_name, python_version='3.7', dependencies=None, pip=None, channels=None):
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
    
    with open('environment.yml', 'w') as out:
        out.write(yml_str)
    
    return 