import logging

from tomtrix.plugin_models import STYLE_CODES, Style
from tomtrix.plugins import tomtrixMessage, tomtrixPlugin


class tomtrixFmt( tomtrixPlugin ) :
    id_ = "fmt"

    def __init__(self, data) -> None :
        self.format = data
        logging.info( self.format )

    def modify(self, tm: tomtrixMessage) -> tomtrixMessage :
        if self.format.style is Style.PRESERVE :
            return tm
        msg_text: str = tm.raw_text
        if not msg_text :
            return tm
        style = STYLE_CODES.get( self.format.style )
        tm.text = f"{style}{msg_text}{style}"
        return tm
