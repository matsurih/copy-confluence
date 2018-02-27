import json
import requests

config_file_name = 'config.json'
get_query = {'expand': 'space,body.view,version,container'}
post_header = {"content-type": "application/json"}


def copy_page(conf):
    print("start copying a page...")
    content = get_base_content(conf)
    post_result = post_new_content(content, conf)
    print(post_result)


def read_config():
    with open(config_file_name) as config_raw:
        return json.load(config_raw)


def create_get_api_url(conf):
    protocol = "https://" if conf['access']['use_https'] else "http://"
    return f"{protocol}{conf['access']['domain']}/rest/api/content"


def get_base_content(conf):
    uri = create_get_api_url(conf) + "/" + conf['base_page']['id']
    auth = (conf['access']['username'], conf['access']['password'])
    response = requests.get(uri, auth=auth, params=get_query, verify=False)
    response.raise_for_status()
    js = json.loads(response.text)
    return js['body']['view']['value']


def post_new_content(body, conf):
    uri = create_get_api_url(conf)
    title = conf['new_page']['title']
    content = json.dumps(create_json_data(title, body, conf))
    auth = (conf['access']['username'], conf['access']['password'])
    verify = conf['access']['verify_ssl']
    return requests.post(uri, auth=auth, data=json.dumps(content), headers=post_header, verify=verify)


def create_json_data(title, body, conf):
    json_data = {
        "type": "page",
        "title": title,
        "ancestors": [
            {
                "id": conf['new_page']['parent_id']
            }
        ],
        "space": {
            "key": conf['new_page']['key']
        },
        "body": {
            "storage": {
                "value": body,
                "representation": "storage"
            }
        }
    }
    if conf['new_page']['ancestors'] is None or conf['new_page']['ancestors'] == "":
        json_data.pop("ancestors", None)
    return json_data


if __name__ == '__main__':
    copy_page(read_config())
