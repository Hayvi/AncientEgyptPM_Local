# Ancient Egypt PM - Game Rebuild Session

## Objective
Rebuild the Ancient Egypt slot game from extracted assets without a loading screen.

## What Was Done

### 1. Asset Extraction from HAR File
- Used `extract_assets.py` to extract 182 assets from `demo.mortalsoft.net.har`
- Assets include: game textures, icons, sounds, fonts, and sprite sheets
- Extracted to `rebuild/assets/`

### 2. Sprite Analysis
- Created `rebuild/find_sprites.py` to analyze the HAR file and find sprite coordinates
- Identified 19 PNG texture files containing game graphics
- Found 972 sprite definitions with coordinates (x, y, width, height)

Key sprites identified:
- `s_bg` - Main game background (1777x999)
- `s_column` - Egyptian pillars (234x888)
- `s_reels_frame_normal` - Reels frame (1509x823)
- `s_title` - Game title (924x109)
- `s_symbol01` - Cleopatra/Pharaoh symbol (434x435)
- `s_symbol03-11` - Card symbols (Q, J, K, A, 10, 9)
- `s_fire_normal_00-14` - Fire animation frames (462x456 each)

### 3. Sprite Extraction
- Created `rebuild/extract_sprites.py` to crop individual sprites from sprite sheets
- Extracted sprites saved to `rebuild/sprites/`:
  - `bg.png` - Background
  - `column.png` - Egyptian column
  - `reels_frame.png` - Reels frame
  - `title.png` - Title
  - `symbol01.png` - Pharaoh/Cleopatra
  - `symbol_Q.png`, `symbol_J.png`, `symbol_K.png`, `symbol_A.png`, `symbol_10.png`, `symbol_9.png` - Card symbols
  - `fire_00.png`, `fire_01.png`, `fire_02.png` - Fire frames

### 4. Game HTML Rebuild
- Created `index.html` with:
  - Sidebar with game menu (Slots, Roulette, Crash, Plinko, Dice, Minesweeper, Tower)
  - Header with DEMO.GG logo, balance display, and login button
  - Game container using extracted background sprite
  - 5 reels with 3 symbols each
  - Spin button with animation
  - Controls (Bonus Game, Spin, Free Spins)
  - No loading screen - game loads immediately

### 5. Files Created/Modified
- `index.html` - Main game page
- `game-init.js` - Initial game initialization (later replaced)
- `rebuild/find_sprites.py` - Sprite coordinate finder
- `rebuild/extract_sprites.py` - Sprite extractor
- `rebuild/asset_viewer.html` - Asset preview tool
- `rebuild/sprites/` - Extracted sprite images

## How to Run
```bash
# Start HTTP server (from project root)
python3 -m http.server 8000

# Open in browser
http://localhost:8000
```

## Remaining Work
- Fine-tune symbol positioning to match original exactly
- Extract missing symbols (scarab, ankh, book) from correct sprite sheets
- Add proper spin animation with reel scrolling
- Add sound effects
- Implement game logic (wins, paylines, bonus features)

## Texture File Mapping
| File | Contains |
|------|----------|
| `efca029b5ef41654da3e3a712c28e506.png` | Main background (s_bg) |
| `835313e3eadfa7b4187f44724febc8c2.png` | Columns (s_column) |
| `a3eb2babeac67a04cb04c41f4ab1dae2.png` | Reels frame |
| `23bfabb9d5ef72343b051b518fe1a995.png` | Pharaoh symbol transforms |
| `20d7ad009ff2a804684180e437657b33.png` | Card symbols (Q, J, K, A, 10, 9) |
| `cdc881ba8688bc94fa31907e495e5db8.png` | Fire animation frames |
| `1adb931445255fa459f1947dbd64864d.png` | Fire animation frames (FS mode) |


---

## Can You Recreate Games from HAR Files?

Yes, to a degree.

### What Can Be Extracted from a HAR File
- Images, sprites, textures (PNG, JPG, SVG)
- Audio files (MP3, WAV, OGG)
- Fonts (WOFF, TTF)
- JSON configs (sprite coordinates, game settings)
- CSS styles
- JavaScript code (often minified/obfuscated)

### What Can Be Rebuilt
- Visual appearance (backgrounds, symbols, UI elements)
- Basic interactions (spin button, menu clicks)
- Layout and styling
- Simple animations

### Limitations
- Game logic is usually server-side or heavily obfuscated
- RNG (random number generation) for wins/payouts
- Backend communication protocols
- Complex animations tied to game engines (PIXI.js, Unity WebGL)
- Encrypted/protected assets
- Real money functionality (obviously)

### This Session's Result
We got ~70-80% of the visual appearance working. The game *looks* similar but doesn't have the actual slot mechanics, win calculations, or proper reel spinning logic.

### Best Use Cases
- Creating mockups/demos
- Learning how games are structured
- Offline previews
- UI/UX prototyping

For a fully functional game, you'd need to reverse-engineer the game logic from the JavaScript (if not obfuscated) or rebuild it from scratch based on the visual reference.

---

## Complex Animations Tied to Game Engines

### Animation System Analysis

The Ancient Egypt PM game uses **PIXI.js** with the **pixi_spine** extension for complex skeletal animations. Here's what we found:

### 1. PIXI.js Framework
- **Version**: PIXI.js v4.x (bundled in `desktop/build.js`)
- **Purpose**: WebGL/Canvas 2D rendering engine
- **Features used**:
  - Sprite rendering with texture atlases
  - Container hierarchy for scene management
  - Ticker system for animation loops (`requestAnimationFrame`)
  - Filters and blend modes

### 2. Spine Animation System (pixi_spine)
The game uses **Spine** for skeletal animations. Spine is a 2D skeletal animation tool that allows:

- **Bone-based animations**: Characters/symbols are rigged with bones
- **Timeline animations**: Rotate, translate, scale, shear, color changes over time
- **Bezier curves**: Smooth easing between keyframes
- **Attachment swapping**: Change visual parts during animation

**Key Spine Components Found in build.js:**
```
- Animation (name, timelines, duration)
- CurveTimeline (bezier interpolation)
- RotateTimeline (bone rotation)
- TranslateTimeline (bone position)
- ScaleTimeline (bone scaling)
- ShearTimeline (bone shearing)
- ColorTimeline (color/alpha changes)
- TwoColorTimeline (tint + dark color)
- AttachmentTimeline (sprite swapping)
- DrawOrderTimeline (z-index changes)
- EventTimeline (trigger events)
- IkConstraintTimeline (inverse kinematics)
- PathConstraintTimeline (path following)
```

### 3. Animation Types in the Game

| Animation | Type | Description |
|-----------|------|-------------|
| Reel Spin | Sprite sequence + easing | Symbols blur/scroll vertically |
| Symbol Win | Spine skeletal | Symbols animate when part of winning line |
| Fire Effects | Sprite sequence | 15-frame fire animation (`s_fire_normal_00-14`) |
| Pharaoh Transform | Spine skeletal | Expanding wild symbol animation |
| UI Transitions | Tween/Timeline | Buttons, panels sliding in/out |
| Particle Effects | PIXI particles | Sparkles, coins, etc. |

### 4. What's Needed to Recreate Animations

#### A. For Simple Sprite Animations (Fire, etc.)
We CAN recreate these with CSS or JavaScript:
```javascript
// Example: Fire animation with extracted frames
const fireFrames = ['fire_00.png', 'fire_01.png', ..., 'fire_14.png'];
let frame = 0;
setInterval(() => {
    fireElement.style.backgroundImage = `url(${fireFrames[frame]})`;
    frame = (frame + 1) % fireFrames.length;
}, 66); // ~15fps
```

#### B. For Spine Skeletal Animations
We CANNOT easily recreate these because:

1. **Missing Spine Data Files**:
   - `.json` skeleton data (bone hierarchy, slots, skins)
   - `.atlas` texture atlas mapping
   - These are typically embedded/encrypted in the game bundle

2. **Runtime Requirements**:
   - Need `pixi-spine` library loaded
   - Need skeleton data parsed and loaded
   - Need animation state machine

3. **Complexity**:
   - Spine animations are authored in Spine Editor ($$$)
   - Export format is proprietary
   - Runtime playback requires specific libraries

#### C. For Reel Spinning
We CAN approximate this with CSS/JS:
```javascript
// Simplified reel spin
function spinReel(reelElement, duration) {
    const symbols = ['pharaoh', 'scarab', 'ankh', 'Q', 'J', 'K', 'A', '10', '9'];
    let speed = 50;
    const decelerate = setInterval(() => {
        // Scroll symbols
        reelElement.scrollTop += speed;
        speed *= 0.98; // Decelerate
        if (speed < 1) {
            clearInterval(decelerate);
            // Snap to final position
        }
    }, 16);
}
```

### 5. Workarounds for Missing Animations

| Original | Workaround |
|----------|------------|
| Spine symbol animations | CSS keyframe animations (scale, rotate, glow) |
| Reel blur during spin | CSS blur filter + rapid symbol changes |
| Win line highlights | CSS box-shadow or SVG overlays |
| Particle effects | CSS animations or canvas particles |
| Fire animations | Sprite sequence (we have the frames!) |

### 6. Tools to Help

- **PIXI.js**: Can be used standalone for rendering
- **GSAP/GreenSock**: Professional animation library
- **Anime.js**: Lightweight animation library
- **Lottie**: For After Effects animations (if you recreate them)
- **CSS Animations**: For simple transforms

### 7. Conclusion

The complex animations in this game are tied to:
1. **Spine runtime** (skeletal animations) - Hard to recreate without original data
2. **PIXI.js rendering** - Can be replicated with effort
3. **Custom game engine** - Proprietary logic in obfuscated JS

**Realistic Recreation Level:**
- Static visuals: ✅ 90% achievable
- Simple animations (fire, UI): ✅ 80% achievable  
- Reel spinning: ⚠️ 60% achievable (approximation)
- Spine skeletal animations: ❌ 10% achievable (would need to recreate from scratch)
- Full game logic: ❌ Requires reverse engineering or rebuilding

To get closer to the original, you'd need to either:
1. Extract Spine data files (if not encrypted)
2. Recreate animations in Spine Editor
3. Use simpler CSS/JS animations as approximations
