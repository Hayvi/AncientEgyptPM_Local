// Ancient Egypt PM - PIXI.js Slot Engine
// ========================================

const CONFIG = {
    // Game dimensions
    width: 900,
    height: 600,
    
    // Reel configuration
    reels: 5,
    rows: 3,
    symbolSize: 120,
    reelWidth: 130,
    reelSpacing: 10,
    
    // Spin settings
    spinDuration: 2000,      // Base spin time in ms
    reelDelay: 150,          // Delay between each reel stopping
    spinSpeed: 50,           // Pixels per frame during spin
    bounceAmount: 20,        // Bounce effect when stopping
    
    // Game settings
    betAmounts: [0.10, 0.25, 0.50, 1.00, 2.00, 5.00, 10.00],
    startingBalance: 1000,
};

// Symbol definitions with payouts (multipliers for 3, 4, 5 of a kind)
// Using correctly extracted sprites from the texture sheets
const SYMBOLS = [
    { id: 'pharaoh', file: 'symbol01.png', payouts: [5, 20, 100], weight: 5 },    // Cleopatra/Pharaoh
    { id: 'symbol03', file: 'symbol03.png', payouts: [3, 10, 50], weight: 8 },    // High value symbol
    { id: 'symbol04', file: 'symbol04.png', payouts: [2, 8, 40], weight: 10 },    // High value symbol
    { id: 'symbol05', file: 'symbol05.png', payouts: [1, 5, 20], weight: 15 },    // A
    { id: 'symbol06', file: 'symbol06.png', payouts: [1, 4, 15], weight: 15 },    // K
    { id: 'symbol07', file: 'symbol07.png', payouts: [0.5, 3, 10], weight: 18 },  // Q
    { id: 'symbol08', file: 'symbol08.png', payouts: [0.5, 2, 8], weight: 18 },   // J
    { id: 'symbol09', file: 'symbol09.png', payouts: [0.25, 1.5, 5], weight: 20 },// 10
    { id: 'symbol10', file: 'symbol10.png', payouts: [0.25, 1, 4], weight: 20 },  // 9
];

// Paylines (row indices for each reel: 0=top, 1=middle, 2=bottom)
const PAYLINES = [
    [1, 1, 1, 1, 1],  // Middle row
    [0, 0, 0, 0, 0],  // Top row
    [2, 2, 2, 2, 2],  // Bottom row
    [0, 1, 2, 1, 0],  // V shape
    [2, 1, 0, 1, 2],  // Inverted V
    [0, 0, 1, 2, 2],  // Diagonal down
    [2, 2, 1, 0, 0],  // Diagonal up
    [1, 0, 0, 0, 1],  // U shape top
    [1, 2, 2, 2, 1],  // U shape bottom
    [0, 1, 1, 1, 0],  // Slight V
];

class SlotGame {
    constructor() {
        this.app = null;
        this.textures = {};
        this.reelContainers = [];
        this.reelStrips = [];
        this.spinning = false;
        this.balance = CONFIG.startingBalance;
        this.betIndex = 3; // Start at $1.00
        this.currentWin = 0;
        
        this.init();
    }
    
    async init() {
        // Create PIXI Application
        this.app = new PIXI.Application({
            width: CONFIG.width,
            height: CONFIG.height,
            backgroundColor: 0x1a0a2e,
            resolution: window.devicePixelRatio || 1,
            autoDensity: true,
        });
        
        document.getElementById('game-container').prepend(this.app.view);
        
        // Load textures
        await this.loadTextures();
        
        // Build game
        this.createBackground();
        this.createReels();
        this.createMask();
        this.setupControls();
        
        // Initial display
        this.updateUI();
    }
    
    async loadTextures() {
        const basePath = 'rebuild/sprites/';
        
        // Load background
        this.textures.bg = await PIXI.Assets.load(basePath + 'bg.png');
        
        // Load symbols
        for (const sym of SYMBOLS) {
            this.textures[sym.id] = await PIXI.Assets.load(basePath + sym.file);
        }
        
        console.log('Textures loaded:', Object.keys(this.textures));
    }
    
    createBackground() {
        const bg = new PIXI.Sprite(this.textures.bg);
        bg.width = CONFIG.width;
        bg.height = CONFIG.height;
        this.app.stage.addChild(bg);
        
        // Dark overlay for reels area
        const overlay = new PIXI.Graphics();
        overlay.beginFill(0x000000, 0.3);
        overlay.drawRoundedRect(
            this.getReelAreaX() - 20,
            this.getReelAreaY() - 20,
            CONFIG.reels * CONFIG.reelWidth + 40,
            CONFIG.rows * CONFIG.symbolSize + 40,
            10
        );
        overlay.endFill();
        this.app.stage.addChild(overlay);
    }
    
    getReelAreaX() {
        return (CONFIG.width - CONFIG.reels * CONFIG.reelWidth) / 2;
    }
    
    getReelAreaY() {
        return (CONFIG.height - CONFIG.rows * CONFIG.symbolSize) / 2 - 30;
    }
    
    createReels() {
        const startX = this.getReelAreaX();
        const startY = this.getReelAreaY();
        
        for (let i = 0; i < CONFIG.reels; i++) {
            // Container for each reel
            const reelContainer = new PIXI.Container();
            reelContainer.x = startX + i * CONFIG.reelWidth;
            reelContainer.y = startY;
            
            // Create reel strip (extra symbols for scrolling)
            const strip = [];
            const numSymbols = CONFIG.rows + 4; // Extra for smooth scrolling
            
            for (let j = 0; j < numSymbols; j++) {
                const symbolData = this.getRandomSymbol();
                const sprite = new PIXI.Sprite(this.textures[symbolData.id]);
                sprite.width = CONFIG.symbolSize - 10;
                sprite.height = CONFIG.symbolSize - 10;
                sprite.x = 5;
                sprite.y = (j - 1) * CONFIG.symbolSize;
                sprite.symbolId = symbolData.id;
                
                reelContainer.addChild(sprite);
                strip.push(sprite);
            }
            
            this.app.stage.addChild(reelContainer);
            this.reelContainers.push(reelContainer);
            this.reelStrips.push(strip);
        }
    }
    
    createMask() {
        // Mask to hide symbols outside reel area
        const mask = new PIXI.Graphics();
        mask.beginFill(0xFFFFFF);
        mask.drawRect(
            this.getReelAreaX(),
            this.getReelAreaY(),
            CONFIG.reels * CONFIG.reelWidth,
            CONFIG.rows * CONFIG.symbolSize
        );
        mask.endFill();
        
        // Apply mask to all reel containers
        this.reelContainers.forEach(container => {
            container.mask = mask;
        });
        
        this.app.stage.addChild(mask);
        
        // Reel frame/border
        const frame = new PIXI.Graphics();
        frame.lineStyle(4, 0xFFD700, 1);
        frame.drawRoundedRect(
            this.getReelAreaX() - 5,
            this.getReelAreaY() - 5,
            CONFIG.reels * CONFIG.reelWidth + 10,
            CONFIG.rows * CONFIG.symbolSize + 10,
            8
        );
        this.app.stage.addChild(frame);
    }
    
    getRandomSymbol() {
        // Weighted random selection
        const totalWeight = SYMBOLS.reduce((sum, s) => sum + s.weight, 0);
        let random = Math.random() * totalWeight;
        
        for (const symbol of SYMBOLS) {
            random -= symbol.weight;
            if (random <= 0) return symbol;
        }
        return SYMBOLS[SYMBOLS.length - 1];
    }
    
    setupControls() {
        const spinBtn = document.getElementById('spin-btn');
        const betUp = document.getElementById('bet-up');
        const betDown = document.getElementById('bet-down');
        
        spinBtn.addEventListener('click', () => this.spin());
        betUp.addEventListener('click', () => this.changeBet(1));
        betDown.addEventListener('click', () => this.changeBet(-1));
        
        // Keyboard support
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space') this.spin();
        });
    }
    
    changeBet(direction) {
        if (this.spinning) return;
        
        this.betIndex = Math.max(0, Math.min(CONFIG.betAmounts.length - 1, this.betIndex + direction));
        this.updateUI();
    }
    
    getCurrentBet() {
        return CONFIG.betAmounts[this.betIndex];
    }
    
    updateUI() {
        document.getElementById('balance').textContent = `🪙 $${this.balance.toFixed(2)}`;
        document.getElementById('bet-display').textContent = `$${this.getCurrentBet().toFixed(2)}`;
        document.getElementById('win-display').textContent = `$${this.currentWin.toFixed(2)}`;
    }
    
    async spin() {
        if (this.spinning) return;
        
        const bet = this.getCurrentBet();
        if (this.balance < bet) {
            alert('Insufficient balance!');
            return;
        }
        
        this.spinning = true;
        this.balance -= bet;
        this.currentWin = 0;
        this.updateUI();
        
        const spinBtn = document.getElementById('spin-btn');
        spinBtn.classList.add('spinning');
        spinBtn.disabled = true;
        
        // Generate final results
        const results = this.generateResults();
        
        // Spin each reel
        const spinPromises = this.reelContainers.map((container, i) => {
            return this.spinReel(i, results[i], CONFIG.spinDuration + i * CONFIG.reelDelay);
        });
        
        await Promise.all(spinPromises);
        
        // Check wins
        const winAmount = this.checkWins(results);
        if (winAmount > 0) {
            this.currentWin = winAmount;
            this.balance += winAmount;
            this.showWin(winAmount);
        }
        
        this.updateUI();
        spinBtn.classList.remove('spinning');
        spinBtn.disabled = false;
        this.spinning = false;
    }
    
    generateResults() {
        // Generate random symbols for each reel position
        const results = [];
        for (let i = 0; i < CONFIG.reels; i++) {
            const reelResult = [];
            for (let j = 0; j < CONFIG.rows; j++) {
                reelResult.push(this.getRandomSymbol().id);
            }
            results.push(reelResult);
        }
        return results;
    }
    
    spinReel(reelIndex, finalSymbols, duration) {
        return new Promise((resolve) => {
            const container = this.reelContainers[reelIndex];
            const strip = this.reelStrips[reelIndex];
            
            const startTime = Date.now();
            let speed = CONFIG.spinSpeed;
            
            const animate = () => {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // Easing - slow down near the end
                if (progress > 0.7) {
                    speed = CONFIG.spinSpeed * (1 - (progress - 0.7) / 0.3) * 0.8 + 5;
                }
                
                // Move all symbols down
                strip.forEach(sprite => {
                    sprite.y += speed;
                    
                    // Wrap around
                    if (sprite.y > CONFIG.rows * CONFIG.symbolSize + CONFIG.symbolSize) {
                        sprite.y -= (CONFIG.rows + 4) * CONFIG.symbolSize;
                        
                        // Change to random symbol during spin
                        if (progress < 0.8) {
                            const newSymbol = this.getRandomSymbol();
                            sprite.texture = this.textures[newSymbol.id];
                            sprite.symbolId = newSymbol.id;
                        }
                    }
                });
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    // Snap to final positions with correct symbols
                    this.setReelResult(reelIndex, finalSymbols);
                    
                    // Bounce effect
                    this.bounceReel(reelIndex).then(resolve);
                }
            };
            
            animate();
        });
    }
    
    setReelResult(reelIndex, symbols) {
        const strip = this.reelStrips[reelIndex];
        
        // Set the visible symbols (indices 1, 2, 3 are visible)
        for (let i = 0; i < CONFIG.rows; i++) {
            const sprite = strip[i + 1];
            sprite.texture = this.textures[symbols[i]];
            sprite.symbolId = symbols[i];
            sprite.y = i * CONFIG.symbolSize;
        }
        
        // Reset other sprites
        strip[0].y = -CONFIG.symbolSize;
        for (let i = CONFIG.rows + 1; i < strip.length; i++) {
            strip[i].y = i * CONFIG.symbolSize;
        }
    }
    
    bounceReel(reelIndex) {
        return new Promise((resolve) => {
            const container = this.reelContainers[reelIndex];
            const originalY = container.y;
            const bounceDistance = CONFIG.bounceAmount;
            
            let frame = 0;
            const totalFrames = 15;
            
            const bounce = () => {
                frame++;
                const progress = frame / totalFrames;
                
                // Bounce curve
                const offset = Math.sin(progress * Math.PI) * bounceDistance * (1 - progress);
                container.y = originalY + offset;
                
                if (frame < totalFrames) {
                    requestAnimationFrame(bounce);
                } else {
                    container.y = originalY;
                    resolve();
                }
            };
            
            bounce();
        });
    }
    
    checkWins(results) {
        let totalWin = 0;
        const bet = this.getCurrentBet();
        
        for (const payline of PAYLINES) {
            const lineSymbols = payline.map((row, reel) => results[reel][row]);
            
            // Count consecutive matching symbols from left
            const firstSymbol = lineSymbols[0];
            let count = 1;
            
            for (let i = 1; i < lineSymbols.length; i++) {
                if (lineSymbols[i] === firstSymbol) {
                    count++;
                } else {
                    break;
                }
            }
            
            // Check for win (3+ matching)
            if (count >= 3) {
                const symbolData = SYMBOLS.find(s => s.id === firstSymbol);
                if (symbolData) {
                    const multiplier = symbolData.payouts[count - 3];
                    totalWin += bet * multiplier;
                }
            }
        }
        
        return totalWin;
    }
    
    showWin(amount) {
        const bigWin = document.getElementById('big-win');
        bigWin.textContent = `WIN $${amount.toFixed(2)}!`;
        bigWin.classList.remove('show');
        
        // Trigger reflow
        void bigWin.offsetWidth;
        
        bigWin.classList.add('show');
        
        // Highlight winning symbols (simple glow effect)
        this.reelStrips.forEach(strip => {
            strip.forEach(sprite => {
                // Could add glow filter here
            });
        });
    }
}

// Start the game
const game = new SlotGame();
