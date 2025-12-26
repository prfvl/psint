import aiohttp
from modules.base_module import BaseModule
from config import Config
from utils.logger import log

class BreachChecker(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Breach Checker"
        self.description = "Checks public databases for compromised emails"
        self.api_url = "https://leakcheck.io/api/public"

    async def run(self, target: str):
        if not Config.LEAKCHECK_API_KEY:
            log.warning("No API Key. Using free tier (Source Name Only, No Passwords).")
        
        log.info(f"Scanning breach databases for: {target}")
        
        async with aiohttp.ClientSession() as session:
            try:
                # Prepare URL
                url = f"{self.api_url}?check={target}"
                if Config.LEAKCHECK_API_KEY:
                    url += f"&key={Config.LEAKCHECK_API_KEY}"

                async with session.get(url, timeout=Config.TIMEOUT) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if not data.get('success'):
                            log.info(f"Target {target} appears clean (no public hits).")
                            return None
                        
                        sources = data.get('sources', [])
                        log.info(f"  [!] CRITICAL: Found in {len(sources)} breaches!")
                        
                        for source in sources:
                            name = source.get('name', 'Unknown Source')
                            date = source.get('date', 'Unknown Date')
                            
                            # Check for specific leaked fields
                            fields = source.get('fields', []) 
                            if not fields:
                                compromised_data = "Email, Password (Implied)"
                            else:
                                compromised_data = ", ".join(fields)

                            log.info(f"      -> Source: {name}")
                            log.info(f"         Date:   {date}")
                            log.info(f"         Breached Items: {compromised_data}")
                            log.info(f"         --------------------------------")
                                
                        return data

                    elif response.status == 429:
                        log.error("Rate limit hit! Try again later.")
                    elif response.status == 404:
                         log.info("Target not found in database.")
                    else:
                        log.warning(f"API returned status: {response.status}")
                        
            except Exception as e:
                log.error(f"Network error: {str(e)}")
        return None