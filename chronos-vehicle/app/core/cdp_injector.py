class CDPInjector:
    def __init__(self, driver):
        self.driver = driver
    
    def apply_stealth(self):
        # Stealth JS to spoof WebGL and Navigator properties
        js = """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(p) {
            if (p===37445) return 'Google Inc. (NVIDIA)';
            if (p===37446) return 'ANGLE (NVIDIA GeForce GTX 1080 Ti)';
            return getParameter.apply(this, arguments);
        };
        """
        try:
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
        except Exception:
            pass
