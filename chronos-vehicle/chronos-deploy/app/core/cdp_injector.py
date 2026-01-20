class CDPInjector:
    def __init__(self, driver):
        self.driver = driver
    
    def apply_stealth(self):
        # Advanced Injection: WebGL, AudioContext, ClientRects
        js = '''
        // 1. WebGL Spoofing (NVIDIA Signature)
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(p) {
            if (p===37445) return 'Google Inc. (NVIDIA)';
            if (p===37446) return 'ANGLE (NVIDIA GeForce GTX 1080 Ti Direct3D11 vs_5_0 ps_5_0)';
            return getParameter.apply(this, arguments);
        };

        // 2. AudioContext Noise (Anti-Fingerprint)
        const originalGetChannelData = AudioBuffer.prototype.getChannelData;
        AudioBuffer.prototype.getChannelData = function(channel) {
            const results = originalGetChannelData.apply(this, arguments);
            for (let i = 0; i < results.length; i += 100) {
                results[i] += Math.random() * 0.0000001; 
            }
            return results;
        };

        // 3. Navigator Overrides
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
        Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
        '''
        try:
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
        except:
            pass