#
# @command create session
#
# @synopsis Establish a session with the Redfish Service (using mcip, username, and password)
#
# @description-start
#
# This command attempts to establish a session with the Redfish Service. It will use the
# mcip, username, and password that are defined in the configuration settings. Use '!dump' to
# view all configuration settings. Use '!setting value' to update the setting and value.
#
# Example:
# 
# (redfish) create session
# 
# ++ Establish Redfish session: (/redfish/v1/SessionService/Sessions)...
# [] Redfish session established (key=5ecff24c0259db2b810327047538dc9f)
# 
# @description-end
#

import json

from commands.commandHandlerBase import CommandHandlerBase
from trace import TraceLevel, Trace
from urlAccess import UrlAccess, UrlStatus

################################################################################
# CommandHandler
################################################################################
class CommandHandler(CommandHandlerBase):
    """Command - create session """
    name = 'create session'

    def prepare_url(self, command):
        return ('/redfish/v1/SessionService/Sessions')

    @classmethod
    def process_json(self, config, url):

        config.sessionValid = False

        Trace.log(TraceLevel.INFO, '')
        Trace.log(TraceLevel.INFO, '++ Establish Redfish session: ({})...'.format(url))
        
        authenticationData = {'UserName' : config.get_value('username'), 'Password' : config.get_value('password') }
        link = UrlAccess.process_request(config, UrlStatus(url), 'POST', False, json.dumps(authenticationData, indent=4))
        
        Trace.log(TraceLevel.TRACE, '   -- urlStatus={} urlReason={}'.format(link.urlStatus, link.urlReason))

        # HTTP 201 Created
        if (link.urlStatus == 201):

            if (link.jsonData != None):
                Trace.log(TraceLevel.TRACE, '   -- {0: <12}: {1}'.format('Id', link.jsonData['Id']))
                Trace.log(TraceLevel.TRACE, '   -- {0: <12}: {1}'.format('Name', link.jsonData['Name']))
                Trace.log(TraceLevel.TRACE, '   -- {0: <12}: {1}'.format('Description', link.jsonData['Description']))
                Trace.log(TraceLevel.TRACE, '   -- {0: <12}: {1}'.format('UserName', link.jsonData['UserName']))
            else:
                Trace.log(TraceLevel.TRACE, '   -- JSON data was (None)')
            
            link.sessionKey = link.response.getheader('x-auth-token', '')
            config.sessionKey = link.sessionKey
            if (config.sessionKey != ''):
                config.sessionValid = True

    @classmethod
    def display_results(self, config):

        if (config.sessionValid == True):            
            Trace.log(TraceLevel.INFO, '[] Redfish session established (key={})'.format(config.sessionKey))
        else:            
            Trace.log(TraceLevel.ERROR, 'Unable to establish a Redfish session, connection, check ip address, username and password')