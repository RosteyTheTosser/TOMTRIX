import logging
import os
import shutil

import requests
from tomtrix.plugins import tomtrixMessage, tomtrixPlugin
from tomtrix.utils import cleanup
from watermark import File, Watermark, apply_watermark


def download_image(url: str, filename: str = "image.png") -> bool :
    if filename in os.listdir() :
        logging.info( "Image for watermarking already exists." )
        return True
    try :
        logging.info( f"Downloading image {url}" )
        response = requests.get( url, stream=True )
        if response.status_code == 200 :
            logging.info( "Got Response 200" )
            with open( filename, "wb" ) as file :
                response.raw.decode_content = True
                shutil.copyfileobj( response.raw, file )
    except Exception as err :
        logging.error( err )
        return False
    else :
        logging.info( "File created image" )
        return True


class tomtrixMark( tomtrixPlugin ) :
    id_ = "mark"

    def __init__(self, data) -> None :
        self.data = data

    async def modify(self, tm: tomtrixMessage) -> tomtrixMessage :
        if not tm.file_type in ["gif", "video", "photo"] :
            return tm
        downloaded_file = await tm.get_file()
        base = File( downloaded_file )
        if self.data.image.startswith( "https://" ) :
            download_image( self.data.image )
            overlay = File( "image.png" )
        else :
            overlay = File( self.data.image )
        wtm = Watermark( overlay, self.data.position )
        tm.new_file = apply_watermark( base, wtm, frame_rate=self.data.frame_rate )
        cleanup( downloaded_file )
        tm.cleanup = True
        return tm
