import pytesseract
from PIL import Image

from tomtrix.plugins import tomtrixMessage, tomtrixPlugin
from tomtrix.utils import cleanup


class tomtrixOcr( tomtrixPlugin ) :
    id_ = "ocr"

    def __init__(self, data) -> None :
        pass

    async def modify(self, tm: tomtrixMessage) -> tomtrixMessage :
        if not tm.file_type in ["photo"] :
            return tm

        file = await tm.get_file()
        tm.text = pytesseract.image_to_string( Image.open( file ) )
        cleanup( file )
        return tm
