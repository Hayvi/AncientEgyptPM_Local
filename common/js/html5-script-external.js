
// Mock Html5GameManager to satisfy index.html dependency
window.Html5GameManager = {
    init: function (config) {
        console.log("[Mock Html5GameManager] Initialized with config:", config);
        // We might need to store this config if other parts of the game look for it,
        // but for now, just existing is enough to stop the crash.
        window.UHT_GAME_CONFIG_SRC = config.gameConfig;
    }
};
console.log("Mock Html5GameManager loaded.");
