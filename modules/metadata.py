import os
from PIL import Image, ExifTags
from PyPDF2 import PdfReader
from modules.base_module import BaseModule
from utils.logger import log

class MetadataExtractor(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Metadata Extractor"
        self.description = "Extracts EXIF and metadata from Images and PDFs"

    async def run(self, target: str):
        if not os.path.exists(target):
            log.error(f"File not found: {target}")
            return None

        log.info(f"Analyzing metadata for: {target}")
        file_ext = target.split('.')[-1].lower()
        
        try:
            if file_ext in ['jpg', 'jpeg', 'png']:
                return self._analyze_image(target)
            elif file_ext == 'pdf':
                return self._analyze_pdf(target)
            else:
                log.warning(f"Unsupported file type: .{file_ext}")
                return None
        except Exception as e:
            log.error(f"Failed to extract metadata: {str(e)}")
            return None

    def _convert_to_degrees(self, value):
        """
        Helper function to convert GPS coordinates from 
        Degrees/Minutes/Seconds (DMS) to Decimal format.
        """
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)

    def _analyze_image(self, path):
        meta_data = {}
        try:
            img = Image.open(path)
            exif_raw = img.getexif()
            
            if not exif_raw:
                log.info("No EXIF data found in image.")
                return None

            log.info("EXIF Data Found!")
            
            # 1. Process Standard Tags
            for tag_id, value in exif_raw.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                
                # Skip the GPSInfo tag here (it's just a pointer number)
                if tag_name == "GPSInfo":
                    continue
                    
                if tag_name in ['Model', 'Make', 'DateTime', 'Software']:
                    log.info(f"  [+] {tag_name}: {value}")
                meta_data[tag_name] = str(value)

            # 2. Process GPS Tags Separately (This is the part we updated)
            gps_raw = exif_raw.get_ifd(0x8825)
            
            if gps_raw:
                log.info("  [!] GPS Directory found. Analyzing...")
                gps_data = {}
                
                # Loop through whatever data IS there
                for t, value in gps_raw.items():
                    sub_tag = ExifTags.GPSTAGS.get(t, t)
                    gps_data[sub_tag] = value
                    # Log it so you can see partial data (like 'GPSVersionID')
                    log.debug(f"      Found GPS Tag: {sub_tag} -> {value}")

                # Check specifically for Coordinates
                if 'GPSLatitude' in gps_data and 'GPSLongitude' in gps_data:
                    try:
                        lat = self._convert_to_degrees(gps_data['GPSLatitude'])
                        lon = self._convert_to_degrees(gps_data['GPSLongitude'])
                        
                        if gps_data.get('GPSLatitudeRef') == 'S': lat = -lat
                        if gps_data.get('GPSLongitudeRef') == 'W': lon = -lon
                        
                        link = f"https://www.google.com/maps?q={lat},{lon}"
                        log.info(f"  [+] GPS Location: {lat}, {lon}")
                        log.info(f"  [+] Google Maps: {link}")
                        meta_data['GoogleMapsLink'] = link
                    except Exception as e:
                        log.warning(f"Could not convert GPS math: {e}")
                else:
                    # This handles the "canon.jpg" case where data is stripped
                    log.warning("  [!] GPS Directory exists, but Latitude/Longitude keys are missing.")

            return meta_data
        except Exception as e:
            log.error(f"Image processing error: {str(e)}")
            return None
        
    def _analyze_pdf(self, path):
        """Extracts Author/Creator data from PDFs."""
        meta_data = {}
        try:
            reader = PdfReader(path)
            doc_info = reader.metadata
            if not doc_info:
                log.info("No PDF metadata found.")
                return None
            log.info("PDF Metadata Found!")
            for key, value in doc_info.items():
                clean_key = key.replace('/', '')
                meta_data[clean_key] = str(value)
                log.info(f"  [+] {clean_key}: {value}")
            return meta_data
        except Exception as e:
            log.error(f"PDF processing error: {str(e)}")
            return None