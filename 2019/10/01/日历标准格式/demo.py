#!/usr/bin/python
# -*- coding: UTF-8 -*-

import BaseHTTPServer
import httplib2
import urlparse

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

clientID = '295995113385-nu8em9928itnt7fa92dc5ab1tv710ojs.apps.googleusercontent.com'
apiKey = 'YFzGsExw6fURfmysfxr1lvpF'
authUrl = 'https://www.googleapis.com/auth/calendar'

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """Child class of BaseHTTPRequestHandler that only handles GET request."""
    flow = OAuth2WebServerFlow(clientID, apiKey, authUrl, redirect_uri='http://localhost:8080/')

    def do_GET(self):
        """Handler for GET request."""
        print '\n\nNEW REQUEST, Path: %s' % (self.path)

        if self.path.startswith('/?fake_user='):
            self.handle_initial_url()
        # When you redirect to the authorization server below, it redirects back
        # to to http://localhost:8080/?code=<some_code> after the user grants access
        # permission for your application.
        elif self.path.startswith('/?code='):
            self.handle_redirected_url()
        else:
            self.respond_ignore() # Either an error from auth server or bad user entered URL.

    def handle_initial_url(self):
        """Handles the initial path."""
        parsed = urlparse.urlparse(self.path)
        fake_user = urlparse.parse_qs(parsed.query)['fake_user'][0]
        self.respond_redirect_to_auth_server(fake_user)

    def respond_redirect_to_auth_server(self, fake_user):
        """Respond to the current request by redirecting to the auth server."""
        uri = RequestHandler.flow.step1_get_authorize_url()
        print 'Redirecting %s to %s' % (fake_user, uri)

        self.send_response(301)
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Location', uri)
        self.end_headers()

    def handle_redirected_url(self):
        """Handles the redirection back from the authorization server."""
        # The server should have responded with a "code" URL query parameter. This is needed to acquire credentials.
        parsed = urlparse.urlparse(self.path)
        code = urlparse.parse_qs(parsed.query)['code'][0]
        credentials = RequestHandler.flow.step2_exchange(code)
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('calendar', 'v3', http=http)

        event = {
            'summary': '腾讯会议日历测试',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': '2019-08-18T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2019-08-18T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'recurrence': [
                # 'RRULE:FREQ=DAILY;COUNT=2' # 按天重复, 重复两次
                # 'RRULE:FREQ=WEEKLY' # 每周重复
            ],
            'attendees': [
                {'email': 'lpage@example.com'},
                {'email': 'sbrin@example.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 15}, # 提前 15 分钟提醒
                ],
            },
        }

        res = service.events().insert(calendarId='primary', body=event).execute()
        parsed = urlparse.urlparse(res.get('htmlLink'))
        eidCode = urlparse.parse_qs(parsed.query)['eid'][0]
        eventeditUrl = 'https://calendar.google.com/calendar/r/eventedit/' + eidCode
        print '>>> eventeditUrl: %s' % (eventeditUrl)
        self.send_response(301)
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Location', eventeditUrl)
        self.end_headers()

    def respond_ignore(self):
        """Responds to the current request that has an unknown path."""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(
            'This path is invalid or user denied access:\n%s\n\n' % self.path)
        self.wfile.write(
            'User entered URL should look like: http://localhost:8080/?fake_user=johndoe')

def main():
    try:
        server = BaseHTTPServer.HTTPServer(('', 8080), RequestHandler)
        print 'Starting server. Use Control+C to stop.'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Shutting down server.'
        server.socket.close()


if __name__ == '__main__':
    main()