import constructors
import fire

if __name__ == '__main__':
    fire.Fire({
        'setup_project': constructors.setup_project
    })