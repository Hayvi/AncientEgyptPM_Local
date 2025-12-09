/**
 * 888 Dragons - Game Initialization
 * Direct game startup without loading screen
 */

(function() {
    'use strict';

    const GameInit = {
        config: {
            gameId: 'AncientEgyptPM',
            width: 1024,
            height: 768,
            fps: 60,
            debug: false
        },

        init: function() {
            console.log('Initializing 888 Dragons...');
            this.setupCanvas();
            this.setupGame();
            this.start();
        },

        setupCanvas: function() {
            const container = document.getElementById('game-container');
            const canvas = document.createElement('canvas');
            
            canvas.id = 'game-canvas';
            canvas.width = this.config.width;
            canvas.height = this.config.height;
            canvas.style.display = 'block';
            canvas.style.margin = '0 auto';
            
            container.appendChild(canvas);
            this.canvas = canvas;
            this.ctx = canvas.getContext('2d');

            // Handle responsive sizing
            window.addEventListener('resize', () => this.handleResize());
        },

        setupGame: function() {
            // Initialize game state
            this.gameState = {
                isRunning: true,
                isPaused: false,
                balance: 1000,
                bet: 10,
                lastUpdate: Date.now()
            };

            // Load game assets
            this.loadAssets();
        },

        loadAssets: function() {
            // Load sounds if available
            if (typeof UHT_SOUNDS_SIZES !== 'undefined') {
                console.log('Sound assets available:', UHT_SOUNDS_SIZES);
            }

            // Load game files
            if (typeof UHT_GAME_FILES !== 'undefined') {
                console.log('Game files:', UHT_GAME_FILES);
            }
        },

        start: function() {
            console.log('Starting game loop...');
            this.gameLoop();
        },

        gameLoop: function() {
            const now = Date.now();
            const deltaTime = (now - this.gameState.lastUpdate) / 1000;
            this.gameState.lastUpdate = now;

            this.update(deltaTime);
            this.render();

            requestAnimationFrame(() => this.gameLoop());
        },

        update: function(deltaTime) {
            // Update game logic
            if (this.gameState.isRunning && !this.gameState.isPaused) {
                // Game update logic here
            }
        },

        render: function() {
            // Clear canvas
            this.ctx.fillStyle = '#1a1a2e';
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

            // Draw game title
            this.ctx.fillStyle = '#ffd700';
            this.ctx.font = 'bold 48px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('888 Dragons', this.canvas.width / 2, 100);

            // Draw game info
            this.ctx.fillStyle = '#ffffff';
            this.ctx.font = '20px Arial';
            this.ctx.fillText(`Balance: $${this.gameState.balance}`, this.canvas.width / 2, 200);
            this.ctx.fillText(`Bet: $${this.gameState.bet}`, this.canvas.width / 2, 250);

            // Draw placeholder for game area
            this.ctx.strokeStyle = '#ffd700';
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(100, 300, this.canvas.width - 200, this.canvas.height - 400);

            this.ctx.fillStyle = '#b0b0b0';
            this.ctx.font = '16px Arial';
            this.ctx.fillText('Game Area', this.canvas.width / 2, this.canvas.height / 2);
        },

        handleResize: function() {
            // Handle window resize if needed
            console.log('Window resized');
        }
    };

    // Start game when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => GameInit.init());
    } else {
        GameInit.init();
    }

    // Expose to global scope
    window.GameInit = GameInit;
})();
