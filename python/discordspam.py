#!/usr/bin/python

"""
MIT License

Copyright (c) 2017 5kyc0d3r

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import json
import time
import getopt
import requests
from requests.exceptions import ConnectionError


version = '1.0.1'
usage = """\

Discord Message Tool %s - (C) 2017 5kyc0d3r

usage: ./discordspam.py --auth <auth-token> --channel <channel-id> --message <custom-message> [options]

Required:

  -a, --auth <auth-token>           specify your discord login authorization token
  -c, --channel <channel-id>        specify the channel's id to use
  -m, --message <custom-message>    your custom message to send to specified channel

Options:

  -h, --help                        print this help menu and exit
  -V, --version                     print program version number and exit
  -v, --verbose                     enable verbose output mode
  -s, --spam                        enable message spam send mode
  -t, --timeout <num>               set time to wait before sending each message in seconds
""" % version


def send_message(auth, channel, message, spam, timeout, verbose):
    try:
        timeout = float(timeout)
    except ValueError:
        print usage
        print '-t or --timeout must be a numeric value in seconds.\n'
        exit(1)


    if verbose:
        print
        print 'Authorization: ' + str(auth)
        print 'Channel ID: ' + str(channel)
        print 'Message: ' + str(message)
        print 'Timeout (s): ' + str(timeout)
        print

    chat_url = 'https://discordapp.com/api/v6/channels/{}/messages'.format(channel)
    headers = {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)', 'Authorization': auth}
    data = {'content': message}

    while True:
        try:
            if verbose:
                print 'Sending message...'

            r = requests.post(chat_url, data=data, headers=headers)

            if verbose:
                author = json.loads(r.text)['author']
                print 'Message sent as {}#{}.'.format(author['username'], author['discriminator'])

            if not spam:
                break
            time.sleep(timeout)

        except ConnectionError:
            if verbose:
                print 'Connection error. Retrying...'

            if not spam:
                print 'Message was not sent due to a connection error.'
                break

            continue


def main(auth=None, channel=None, message=None, spam=False, timeout=1, verbose=False):
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hVvsa:c:m:t:', ['help', 'version', 'verbose',
                                                                    'spam', 'auth=', 'channel=',
                                                                    'message=', 'timeout='])

    except getopt.GetoptError as e:
        print usage
        print str(e) + '\n'
        exit(1)

    for opt, arg in opts:

        if opt in ('-h', '--help'):
            print usage
            exit(0)

        elif opt in ('-V', '--version'):
            print 'Discord Message Tool %s' % version
            exit(0)

        elif opt in ('-v', '--verbose'):
            verbose = True

        elif opt in ('-a', '--auth'):
            auth = arg

        elif opt in ('-c', '--channel'):
            channel = arg

        elif opt in ('-m', '--message'):
            message = arg

        elif opt in ('-s', '--spam'):
            spam = True

        elif opt in ('-t', '--timeout'):
            timeout = arg

    if not auth or not channel or not message:
        print usage
        exit(1)

    send_message(auth, channel, message, spam, timeout, verbose)


if __name__ == "__main__":
    main()

