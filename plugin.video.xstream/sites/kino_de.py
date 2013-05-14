from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

SITE_IDENTIFIER = 'kino_de'
SITE_NAME = 'Kino.de'

URL_MAIN = 'http://www.kino.de'
URL_TRAILERS = 'http://www.kino.de/trailer-und-bilder/trailer-und-clips/'


ENTRIES_PER_PAGE = 30

def load():    

    oGui = cGui()
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('showTrailers')
    oGuiElement.setTitle('neue Trailers')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl', URL_TRAILERS)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showTrailers():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        
        iPage = 0
        if (oInputParameterHandler.exist('page')):
            iPage = oInputParameterHandler.getValue('page')

        sTrailerUrl = sUrl
        if (iPage > 0):
            sTrailerUrl = sTrailerUrl + '/' + str(iPage)

        oRequest = cRequestHandler(sTrailerUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<li class="(?:even|)?">\s*<a href="[^"]+player\((\d+), \d+\)"[^>]+>\s*<img src="([^"]+)" alt="([^"]+)".*?<p>([^<]+)<a href="([^"]+)".*?</li>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
             for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showTrailerDetails')
                oGuiElement.setTitle(aEntry[2])
                oGuiElement.setThumbnail(aEntry[1])
                oGuiElement.setDescription(aEntry[3].strip())

                
                sTrailerDetailUrl = URL_MAIN + str(aEntry[4])
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sTrailerDetailUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

        if (iPage > 0):
            bShowNextButton = __checkForNextPage(iPage, sHtmlContent)
            if (bShowNextButton == True):
                iNextPage = int(iPage) + 1

                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showTrailers')
                oGuiElement.setTitle('mehr ..')                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGui.setEndOfDirectory()

def __checkForNextPage(iPage, sHtmlContent):
    sPattern = '<a href=\'.*?\'>(.{1,2})</a></span>    <span class="nextLink">'   

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        iLastPage = aResult[1][0]
        if (int(iPage) < int(iLastPage)):
            return True

    return False    

def showTrailerDetails():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = '(http://fpc.e-media.de/kinode/clip/\d+.xml)'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        i = 1
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sTitle = 'Clip ' + str(i)
                sUrl = aEntry
                
                oHoster = cHosterHandler().getHoster('kinode')
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHosterMenuDirect(oGui, oHoster, sUrl)
                i = i+1

    oGui.setEndOfDirectory()