from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
import re
import urlresolver

class cHosterHandler:

    def getUrl(self, oHoster):
        sUrl = oHoster.getUrl()
        if (oHoster.checkUrl(sUrl)):
            oRequest = cRequestHandler(sUrl)            
            sContent = oRequest.request()
            pattern = oHoster.getPattern()
            if type(pattern) == type(''):
                aMediaLink = cParser().parse(sContent, oHoster.getPattern())
                if (aMediaLink[0] == True):
                    logger.info('hosterhandler: ' + aMediaLink[1][0])
                    return True, aMediaLink[1][0]
            else:
                for p in pattern:
                    aMediaLink = cParser().parse(sContent, p)
                    if (aMediaLink[0] == True):
                        logger.info('hosterhandler: ' + aMediaLink[1][0])
                        return True, aMediaLink[1][0]
                        
        return False, ''

    def getHoster2(self, sHoster):    
        # if (sHoster.find('.') != -1):
            # Arr = sHoster.split('.')
            # if (Arr[0].startswith('http') or Arr[0].startswith('www')):
                # sHoster = Arr[1]
            # else:
                # sHoster = Arr[0]
        return self.getHoster(sHoster)        
        
    def getHoster(self, sHosterFileName):
        if sHosterFileName != '':
            source = [urlresolver.HostedMediaFile(url=sHosterFileName)]
            if (urlresolver.choose_source(source)):
                return source[0].get_host()
            # media_id hier nur als Dummy um zu testen ob es Resolver fuer den Hoster gibt
            source = [urlresolver.HostedMediaFile(host=sHosterFileName, media_id='ABC123XYZ')]            
            if (urlresolver.choose_source(source)):
                return source[0].get_host()
        return False   