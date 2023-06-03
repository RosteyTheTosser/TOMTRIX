import logging

from tomtrix.plugins import tomtrixMessage, tomtrixPlugin


class tomtrixCaption( tomtrixPlsugin ) :
    id_ = "caption"

    def __init__(self, data) -> None :
        self.caption = data
        logging.info( self.caption )

    def modify(self, tm: tomtrixMessage) -> tomtrixMessage :
        tm.text = f"{self.caption.header}{tm.text}{self.caption.footer}"
        return tm
