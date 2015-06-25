import tornado.web
import tornado.ioloop
import tornado.options
import destinyPlatform as destiny
import json
import logging
import argparse
import sys

from tornado.log import enable_pretty_logging
enable_pretty_logging()

#make use of the tornado loggers
#the following comments are stolen straight from the tornado documentation
"""
* ``tornado.access``: Per-request logging for Tornado's HTTP servers (and
  potentially other servers in the future)
* ``tornado.application``: Logging of errors from application code (i.e.
  uncaught exceptions from callbacks)
* ``tornado.general``: General-purpose logging, including any errors
  or warnings from Tornado itself.

These streams may be configured independently using the standard library's
`logging` module.  For example, you may wish to send ``tornado.access`` logs
to a separate file for analysis.
"""
logging.basicConfig(stream=sys.stdout)
access_log = logging.getLogger("tornado.access")
app_log = logging.getLogger("tornado.application")
gen_log = logging.getLogger("tornado.general")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class GameHandler(tornado.web.RequestHandler):
    def get(self):
        print(self.request)
        gamertag = self.get_argument("gamertag")
        characterId = self.get_argument('characterId')
        membershipId = destiny.getMembershipID(gamertag)

        recent = destiny.getMostRecentPvPGames(membershipId,characterId,count=5)

        #recent is a list of the count number of games represented as json objects
        out = {"Response":recent}
        return json.dumps(out)

class CharacterHandler(tornado.web.RequestHandler):
    def get(self):
        gamertag = self.get_argument("gamertag")
        
        baseURL = "http://www.bungie.net"
        try:
            membershipId = destiny.getMembershipID(gamertag)
        except destiny.NoDataError as e:
            self.write(e.message)

        character_info = destiny.getCharacterInfo(membershipId)
        characters = {c['characterBase']['characterId']:destiny.CLASS_HASH[c['characterBase']['classHash']]
                  for c in character_info['Response']['data']['characters']}
        
        levels = {c['characterBase']['characterId']:c['characterLevel']
                  for c in character_info['Response']['data']['characters']}

        emblems = {c['characterBase']['characterId']:(baseURL + c['emblemPath'])
                   for c in character_info['Response']['data']['characters']}

        out = {"characters":characters, "levels":levels, "emblems":emblems}

        self.write(json.dumps(out))

class RecentActivityHandler(tornado.web.RequestHandler):
    def get(self):
        gamertag = self.get_argument("gamertag")
        characterId = self.get_argument('characterId')
        membershipId = destiny.getMembershipID(gamertag)

        recent = destiny.getMostRecentPvPGames(membershipId,characterId,count=5)

        #recent is a list of the count number of games represented as json objects
        out = {"Response":recent}
        self.write(json.dumps(out))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8888, type=int, help="Set port for application")
    parser.add_argument('--debug', default=True, type=bool, help="Turn debug on or off.  If debug is on, then the server will automatically restart when a source file is changed.")

    args = parser.parse_args()

    application = tornado.web.Application(handlers = [
        (r"/index.html",MainHandler),
        (r"/get_characters/",CharacterHandler),
        (r"/get_games/",GameHandler),
        (r"/postgamestats/",RecentActivityHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static/"})
    ], debug = args.debug)


    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()  
    access_log.info('Ready to receive requests on {0}'.format(args.port))
if __name__ == "__main__":
    main()