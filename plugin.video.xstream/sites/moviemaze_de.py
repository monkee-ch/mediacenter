from resources.lib.util import cUtil
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from xbmc import log

SITE_IDENTIFIER = 'moviemaze_de'
SITE_NAME = 'MovieMaze.de'

URL_MAIN = 'http://www.moviemaze.de'
URL_ARCHIV = 'http://www.moviemaze.de/media/trailer/archiv.phtml'
URL_UPDATES_ALL = 'http://www.moviemaze.de/media/trailer/'
URL_UPDATES_HD = 'http://www.moviemaze.de/media/trailer/index.phtml?update=hd'
URL_TRAILER = 'http://www.moviemaze.de/media/trailer/'
URL_SEARCH = 'http://www.moviemaze.de/suche/result.phtml'

def load():
    oGui = cGui()
    __createMainMenuItem(oGui, 'Letzte Updates (Alle)', URL_UPDATES_ALL, 'listVideos', 'Letzte Updates')
    __createMainMenuItem(oGui, 'Letzte Updates (HD)', URL_UPDATES_HD, 'listVideos', 'Letzte Updates')
    __createMainMenuItem(oGui, 'User Top 10', URL_UPDATES_ALL, 'listVideos', 'User Top 10')
    __createMainMenuItem(oGui, 'Archive', URL_ARCHIV, 'showCharacters')
    __createMainMenuItem(oGui, 'Suche', URL_SEARCH, 'showSearch')

    oGui.setEndOfDirectory()

def __createMainMenuItem(oGui, sTitle, sUrl, sFunction = '', sHeader = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sTitle)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl', sUrl)
    oOutputParameterHandler.addParameter('sHeader', sHeader)   
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showCharacters():
    oGui = cGui()
    __createCharacters(oGui, 'A')
    __createCharacters(oGui, 'B')
    __createCharacters(oGui, 'C')
    __createCharacters(oGui, 'D')
    __createCharacters(oGui, 'E')
    __createCharacters(oGui, 'F')
    __createCharacters(oGui, 'G')
    __createCharacters(oGui, 'H')
    __createCharacters(oGui, 'I')
    __createCharacters(oGui, 'J')
    __createCharacters(oGui, 'K')
    __createCharacters(oGui, 'L')
    __createCharacters(oGui, 'N')
    __createCharacters(oGui, 'O')
    __createCharacters(oGui, 'Q')
    __createCharacters(oGui, 'R')
    __createCharacters(oGui, 'S')
    __createCharacters(oGui, 'T')
    __createCharacters(oGui, 'U')
    __createCharacters(oGui, 'V')
    __createCharacters(oGui, 'W')
    __createCharacters(oGui, 'XYZ')
    __createCharacters(oGui, '0-9')
    oGui.setEndOfDirectory()

def __createCharacters(oGui, sCharacter):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('showArchive')
    oGuiElement.setTitle(sCharacter)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl', URL_ARCHIV)
    oOutputParameterHandler.addParameter('sCharacter', sCharacter)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        __callSearch(sSearchText)
        
    oGui.setEndOfDirectory()

def __callSearch(sSearchText):
    oGui = cGui()

    oRequest = cRequestHandler(URL_SEARCH)
    oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequest.addParameters('searchword', sSearchText)
    oRequest.addParameters('x', 0)
    oRequest.addParameters('y', 0)
    sHtmlContent = oRequest.request()

    sPattern = '<tr.+?<a href="([^"]+)"><b style="font-size:9pt;font-weight:bold;">(.*?)<nobr>.+?<a href="([^"]+)">Trailer</a></td>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showTrailerDetails')

            sTitle = str(aEntry[1])
            sTitle = sTitle.replace('<br />', ' ')
            sTitle = cUtil().removeHtmlTags(sTitle)
            oGuiElement.setTitle(sTitle)

            sTrailerUrl = URL_MAIN + str(aEntry[2])
                        
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sUrl', sTrailerUrl)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showArchive():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl') and oInputParameterHandler.exist('sCharacter')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        sCharacter = oInputParameterHandler.getValue('sCharacter')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
       
        sPattern = '<span class="h2">' + str(sCharacter) + '</span>.*?</tr>	<tr>.*?<table(.*?)</table>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            sHtmlContent = aResult[1][0]

            sPattern = '<a href="/media/trailer/([^"]+)">([^<]+)</a>'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                for aEntry in aResult[1]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('showTrailerDetails')
                    oGuiElement.setTitle(aEntry[1])

                    sTrailerUrl = URL_TRAILER + str(aEntry[0])
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', sTrailerUrl)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def listVideos():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        sHeader = oInputParameterHandler.getValue('sHeader')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = str(sHeader) + '</h2>.*?</table>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sHtmlContent = aResult[1][0]

            sPattern = '<td width=100% style="text-align:left;"><a href="/media/trailer/([^"]+)">([^<]+)</a> <span class="small_grey">([^<]+)</span></td>'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
                        
            if (aResult[0] == True):
                for aEntry in aResult[1]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('showTrailerDetails')
                    
                    sTitle = str(aEntry[1]) + ' ' + str(aEntry[2])
                    oGuiElement.setTitle(sTitle)

                    sTrailerUrl = URL_TRAILER + str(aEntry[0])
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', sTrailerUrl)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
                    
    oGui.setEndOfDirectory()


def showTrailerDetails():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
       
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = "clipxml\:'(http://www.moviemaze.de/media/trailer/data.phtml\?id=[^']+)'"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            oRequest = cRequestHandler(aResult[1][0])
            sHtmlContent = oRequest.request()
            
            sPattern = '<clip>\s*<title><\!\[CDATA\[([^\]]+)\]\]></title>.*?<thumbnail><\!\[CDATA\[([^\]]+)\]\]></thumbnail>\s*<overlayicon>lang-([^<]+)</overlayicon>\s*<downloadurl><\!\[CDATA\[(.*?)\?down=1\]\]></downloadurl>.*?</clip>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] == True:
                for aEntry in aResult[1]:
                    sThumbnail = aEntry[1]
                    sTitle = aEntry[0] + ' (' + aEntry[2].upper() + ')'
                    sTrailerUrl = aEntry[3]
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('showHoster')
                    oGuiElement.setTitle(sTitle)
                    oGuiElement.setThumbnail(sThumbnail)
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', sTrailerUrl)
                    oOutputParameterHandler.addParameter('sTitle', sTitle)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
            else:
                sPattern = '<clip>\s*<title><\!\[CDATA\[([^\]]+)\]\]></title>.*?<thumbnail><\!\[CDATA\[([^\]]+)\]\]></thumbnail>\s*<overlayicon>lang-([^<]+)</overlayicon>.*?<urllow><\!\[CDATA\[([^\]]+)\]\]></urllow>.*?</clip>'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0] == True:
                    for aEntry in aResult[1]:
                        sThumbnail = aEntry[1]
                        sTitle = aEntry[0] + ' (' + aEntry[2].upper() + ')'
                        sTrailerUrl = aEntry[3]
                        oGuiElement = cGuiElement()
                        oGuiElement.setSiteName(SITE_IDENTIFIER)
                        oGuiElement.setFunction('showHoster')
                        oGuiElement.setTitle(sTitle)
                        oGuiElement.setThumbnail(sThumbnail)
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('sUrl', sTrailerUrl)
                        oOutputParameterHandler.addParameter('sTitle', sTitle)
                        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHoster():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl') and oInputParameterHandler.exist('sTitle')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        sTitle = oInputParameterHandler.getValue('sTitle')
        oHoster = cHosterHandler().getHoster2('moviemaze')       
        oHoster.setDisplayName(sTitle)
        oHoster.setFileName(sTitle)
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sUrl)
    oGui.setEndOfDirectory()
        

def __createTitle(sTitle):    
    iPosition = sTitle.rfind('-')
    if (iPosition == -1):
        return sTitle
    
    return sTitle[0:iPosition]

def dummyFunction():
    oGui = cGui()
    oGui.setEndOfDirectory()