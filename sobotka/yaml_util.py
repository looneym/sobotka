import yaml


def load_local_conf():
    try:
        return yaml.safe_load(open(".local_conf.yaml")) 
    except:
        print( 
            "Sobotka expected a .local_conf.yaml file to link this directory " \
            "to an existing project but did not find one. " \
            "Try sobotka up to create a new project instead") 


def store_local_conf(project_id):
    local_conf = {}
    local_conf["project_id"] = project_id
    with open('.local_conf.yaml', 'w') as yaml_file:
        yaml.dump(local_conf, yaml_file, default_flow_style=False)


def load_manifest():
    try:
        return yaml.safe_load(open("manifest.yaml")) 
    except:
        print( 
            "Sobotka expected a manifest.yaml file to define " \
            "the Project. Create this file in the root of your " \
            "project or cd to a dorectory where one exists to begin") 
        