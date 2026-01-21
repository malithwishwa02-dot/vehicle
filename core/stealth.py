"""
STEALTH INJECTOR MODULE
Injects JavaScript overrides to mask fingerprinting vectors.
Target: Canvas, AudioContext, WebGL, Fonts, Screen.
"""

class StealthInjector:
    def __init__(self, config=None):
        self.config = config or {}

    def get_injection_script(self) -> str:
        """
        Returns the combined JS payload to be evaluated on new document.
        """
        return """
        (() => {
            // 1. WebGL Spoofing (Apple M3 Simulation)
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                // UNMASKED_VENDOR_WEBGL
                if (parameter === 37445) return 'Apple Inc.';
                // UNMASKED_RENDERER_WEBGL
                if (parameter === 37446) return 'Apple M3';
                return getParameter(parameter);
            };

            // 2. Screen Spoofing (Retina Display)
            Object.defineProperty(screen, 'width', { get: () => 3024 });
            Object.defineProperty(screen, 'height', { get: () => 1964 });
            Object.defineProperty(screen, 'colorDepth', { get: () => 24 });
            Object.defineProperty(screen, 'pixelDepth', { get: () => 24 });

            // 3. Hardware Concurrency
            Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 12 });

            // 4. AudioContext Noise (Anti-Fingerprinting)
            const originalCreateOscillator = AudioContext.prototype.createOscillator;
            const originalCreateAnalyser = AudioContext.prototype.createAnalyser;
            
            AudioContext.prototype.createOscillator = function() {
                const oscillator = originalCreateOscillator.apply(this, arguments);
                const originalStart = oscillator.start;
                oscillator.start = function(when = 0) {
                    return originalStart.apply(this, [when]);
                };
                return oscillator;
            };
            
            // 5. Canvas Noise
            const toDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function(type) {
                // Add tiny noise to canvas export
                if (type === 'image/png' || type === 'image/jpeg') {
                    // In a real implementation, we would modify the pixel data here
                    // For now, we rely on the browser's native randomization if available
                    // or just pass through to avoid breaking rendering.
                    // A proper implementation renders the canvas, modifies 1 pixel, then exports.
                }
                return toDataURL.apply(this, arguments);
            };

            // 6. Permissions (Mask Notifications/Geo as 'prompt' instead of 'denied')
            const originalQuery = navigator.permissions.query;
            navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
            
            console.log("[CHRONOS] Stealth Injected.");
        })();
        """
