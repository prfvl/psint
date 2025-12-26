import re
import aiohttp
from modules.base_module import BaseModule
from utils.logger import log

class FootprintTracker(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Footprint Tracker"
        self.description = "Validates UPI, Checks Socials, and Generates Dorks"
        
        self.upi_pattern = re.compile(r"^[a-zA-Z0-9.\-_]+@[a-zA-Z]+$")
        
        self.upi_handles = {
            "okaxis": "Google Pay (Axis)",
            "oksbi": "Google Pay (SBI)",
            "okicici": "Google Pay (ICICI)",
            "ybl": "PhonePe",
            "paytm": "Paytm"
        }

        # 1. Active Scan (API/Direct Check)
        self.active_sites = {
            "GitHub": "https://api.github.com/users/{}", 
            "Reddit": "https://www.reddit.com/user/{}/about.json", 
        }
        
        # 2. Dork Templates (Used for Passive Recon OR Fallback)
        self.dork_templates = {
            "LinkedIn": "linkedin.com/in/{}",
            "Facebook": "facebook.com/{}",
            "Instagram": "instagram.com/{}",
            "GitHub": "github.com/{}",  # <--- Added for fallback
            "Reddit": "reddit.com/user/{}" # <--- Added for fallback
        }

    async def run(self, target: str):
        log.info(f"Analyzing footprint for: {target}")
        
        username = target
        if "@" in target:
            username = target.split('@')[0]
            if self.upi_pattern.match(target):
                self._analyze_upi(target)

        # Phase 1: Active Scanning
        log.info(f"  [?] Phase 1: Active Scanning for '{username}'...")
        await self._check_socials(username)
        
        # Phase 2: Passive Recon (Manual Checks)
        log.info(f"  [?] Phase 2: Generating Google Dorks (Walled Gardens)...")
        # We only auto-print these because we CANNOT check them via API
        for site in ["LinkedIn", "Facebook", "Instagram"]:
            self._print_dork(site, username)

    def _analyze_upi(self, upi_id):
        handle = upi_id.split("@")[-1].lower()
        provider = self.upi_handles.get(handle, "Unknown Provider")
        log.info(f"  [+] Valid UPI Handle: {provider}")

    async def _check_socials(self, username):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            for site, url_template in self.active_sites.items():
                url = url_template.format(username)
                try:
                    async with session.get(url, timeout=5) as response:
                        if response.status == 200:
                            log.info(f"  [!] FOUND: {site} Profile -> {url}")
                        
                        elif response.status == 404:
                            # FALLBACK LOGIC: If API says no, ask Google.
                            if site in ["GitHub", "Reddit"]:
                                log.warning(f"  [-] {site} API said 404. Generating Fallback Dork...")
                                self._print_dork(site, username)
                            else:
                                log.debug(f"  [-] {site}: Not found")
                                
                except Exception:
                    pass

    def _print_dork(self, site, username):
        """Helper to print a clean Google Dork link."""
        query_fmt = self.dork_templates.get(site)
        if query_fmt:
            dork = query_fmt.format(username)
            # Create clickable link
            link = f"https://www.google.com/search?q={dork}"
            log.info(f"  [>] Manual Check {site}: {link}")