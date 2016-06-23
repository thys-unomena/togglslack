import time
import requests
import datetime
import json

from django.conf import settings


def get_toggl_post_slack():
    today = datetime.datetime.today().strftime("%Y-%m-%d")

    r = requests.get(
        'https://toggl.com/reports/api/v2/details?user_agent=%s&workspace_id=601029&since=%s' % (settings.USER_AGENT, today),
        auth=(settings.TOGGL_USER_TOKEN, 'api_token'))

    json_dict = r.json()

    total_sec_today = json_dict['total_grand']/1000

    total_time_today = time.strftime('%H:%M:%S', time.gmtime(total_sec_today))
    slack_text = ['Total time tracked today: %s\n' % total_time_today]

    time_entries = {}
    for time_entry in json_dict['data']:
        if time_entry['description'] in time_entries:
            time_entries[time_entry['description']] += time_entry['dur']/1000
        else:
            time_entries[time_entry['description']] = time_entry['dur']/1000

    for description, duration in time_entries.iteritems():
        task_time_today = time.strftime('%H:%M:%S', time.gmtime(duration))
        slack_text.append('Description: %s\nTime tracked: %s\n' % (description, task_time_today))

    requests.post(
        'https://hooks.slack.com/services/%s'
        % settings.SLACK_INCOMING_HOOK_TOKEN,
        headers={'Content-type': 'application/json'},
        data=json.dumps({
            'text': "\n".join(slack_text),
            'icon_emoji': ':cubimal_chick:',
            'username':  'toggl-bot'
        })
    )
