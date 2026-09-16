/**
 * T-Rex Endless Runner - Procedural Canvas Engine & Web Audio Synthesizer
 * Built following AI-Native SDLC under DeepSeek Harness.
 */

(function () {
  'use strict';

  // --- Sound Synthesizer (Web Audio API) ---
  class SoundFX {
    constructor() {
      this.ctx = null;
      this.isMuted = localStorage.getItem('dino_muted') === 'true';
    }

    init() {
      if (!this.ctx) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) this.ctx = new AudioCtx();
      }
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
    }

    setMuted(muted) {
      this.isMuted = muted;
      localStorage.setItem('dino_muted', muted ? 'true' : 'false');
    }

    playJump() {
      if (!this.ctx || this.isMuted) return;
      try {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        const now = this.ctx.currentTime;
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.exponentialRampToValueAtTime(420, now + 0.12);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.12);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.13);
      } catch (e) {}
    }

    playScoreMilestone() {
      if (!this.ctx || this.isMuted) return;
      try {
        const now = this.ctx.currentTime;
        [587.33, 880.00].forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'triangle';
          const t = now + idx * 0.08;
          osc.frequency.setValueAtTime(freq, t);
          gain.gain.setValueAtTime(0.25, t);
          gain.gain.linearRampToValueAtTime(0.01, t + 0.08);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(t);
          osc.stop(t + 0.09);
        });
      } catch (e) {}
    }

    playHit() {
      if (!this.ctx || this.isMuted) return;
      try {
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(120, now);
        osc.frequency.linearRampToValueAtTime(40, now + 0.25);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.25);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.26);
      } catch (e) {}
    }
  }

  // --- Constants & Config ---
  const CANVAS_WIDTH = 800;
  const CANVAS_HEIGHT = 240;
  const GROUND_Y = 200; // Baseline height
  const GRAVITY = 1500; // px/s^2
  const JUMP_VELOCITY = -520; // px/s upward
  const BASE_SPEED = 360; // px/s

  // --- Game State ---
  const STATE = {
    IDLE: 'IDLE',
    RUNNING: 'RUNNING',
    PAUSED: 'PAUSED',
    GAMEOVER: 'GAMEOVER'
  };

  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');
  const startOverlay = document.getElementById('startOverlay');
  const pauseOverlay = document.getElementById('pauseOverlay');
  const gameOverOverlay = document.getElementById('gameOverOverlay');
  const scoreDisplay = document.getElementById('scoreDisplay');
  const hiScoreDisplay = document.getElementById('hiScoreDisplay');
  const restartBtn = document.getElementById('restartBtn');
  const resumeBtn = document.getElementById('resumeBtn');
  const pauseBtn = document.getElementById('pauseBtn');
  const muteBtn = document.getElementById('muteBtn');
  const jumpBtn = document.getElementById('jumpBtn');
  const duckBtn = document.getElementById('duckBtn');

  const sound = new SoundFX();

  let gameState = STATE.IDLE;
  let score = 0;
  let hiScore = parseInt(localStorage.getItem('dino_hi_score') || '0', 10);
  let speed = BASE_SPEED;
  let lastTime = 0;
  let groundOffset = 0;
  let obstacleTimer = 0;
  let nextObstacleDistance = 1.4; // seconds
  let isNight = false;
  let milestoneFlash = 0;

  // --- Dinosaur Player ---
  const dino = {
    x: 50,
    y: GROUND_Y,
    vy: 0,
    width: 42,
    height: 46,
    duckHeight: 28,
    isJumping: false,
    isDucking: false,
    stepCounter: 0,

    reset() {
      this.y = GROUND_Y;
      this.vy = 0;
      this.isJumping = false;
      this.isDucking = false;
      this.stepCounter = 0;
    },

    jump() {
      if (!this.isJumping && gameState === STATE.RUNNING) {
        this.isJumping = true;
        this.isDucking = false;
        this.vy = JUMP_VELOCITY;
        sound.playJump();
      }
    },

    duck(active) {
      if (this.isJumping) {
        if (active) {
          this.vy += GRAVITY * 0.35; // Fast-drop downward
        }
        this.isDucking = false;
      } else {
        this.isDucking = active;
      }
    },

    update(dt) {
      if (this.isJumping) {
        this.vy += GRAVITY * dt;
        this.y += this.vy * dt;

        if (this.y >= GROUND_Y) {
          this.y = GROUND_Y;
          this.vy = 0;
          this.isJumping = false;
        }
      }
      this.stepCounter += dt * 15;
    },

    getHitbox() {
      const h = this.isDucking ? this.duckHeight : this.height;
      const w = this.isDucking ? 56 : this.width;
      // Inset box slightly for arcade forgiveness
      return {
        x: this.x + 4,
        y: this.y - h + 4,
        width: w - 8,
        height: h - 6
      };
    },

    draw(ctx, night) {
      const color = night ? '#e8eaed' : '#535353';
      ctx.fillStyle = color;

      const legFrame = Math.floor(this.stepCounter) % 2 === 0;

      if (this.isDucking) {
        // Ducking Body (low elongated profile)
        const top = this.y - this.duckHeight;
        ctx.fillRect(this.x, top + 8, 48, 16);
        ctx.fillRect(this.x + 36, top, 18, 14); // Extended Head
        // Eye
        ctx.fillStyle = night ? '#282a2d' : '#ffffff';
        ctx.fillRect(this.x + 46, top + 3, 3, 3);
        ctx.fillStyle = color;
        // Legs
        if (legFrame) {
          ctx.fillRect(this.x + 12, top + 22, 5, 6);
        } else {
          ctx.fillRect(this.x + 28, top + 22, 5, 6);
        }
      } else {
        // Standing / Running T-Rex
        const top = this.y - this.height;

        // Torso & Body
        ctx.fillRect(this.x + 10, top + 14, 24, 20);
        ctx.fillRect(this.x + 16, top + 4, 18, 12); // Neck
        ctx.fillRect(this.x + 20, top, 20, 16); // Head
        ctx.fillRect(this.x + 30, top + 10, 10, 4); // Snout
        ctx.fillRect(this.x, top + 16, 12, 12); // Tail

        // Eye
        ctx.fillStyle = night ? '#282a2d' : '#ffffff';
        if (gameState === STATE.GAMEOVER) {
          // X Eye
          ctx.fillRect(this.x + 26, top + 4, 4, 4);
        } else {
          ctx.fillRect(this.x + 26, top + 3, 3, 3);
        }
        ctx.fillStyle = color;

        // Tiny Arms
        ctx.fillRect(this.x + 32, top + 20, 6, 3);

        // Legs
        if (this.isJumping) {
          ctx.fillRect(this.x + 14, top + 34, 4, 10);
          ctx.fillRect(this.x + 24, top + 34, 4, 10);
        } else if (legFrame) {
          ctx.fillRect(this.x + 14, top + 34, 4, 12);
          ctx.fillRect(this.x + 14, top + 44, 6, 2);
          ctx.fillRect(this.x + 24, top + 34, 4, 7);
        } else {
          ctx.fillRect(this.x + 14, top + 34, 4, 7);
          ctx.fillRect(this.x + 24, top + 34, 4, 12);
          ctx.fillRect(this.x + 24, top + 44, 6, 2);
        }
      }
    }
  };

  // --- Background Decor (Clouds & Ground) ---
  const clouds = [
    { x: 150, y: 50, scale: 1 },
    { x: 450, y: 70, scale: 0.8 },
    { x: 720, y: 40, scale: 1.1 }
  ];

  function drawCloud(ctx, x, y, scale, night) {
    ctx.fillStyle = night ? '#444746' : '#d2d3d5';
    const s = scale;
    ctx.beginPath();
    ctx.arc(x, y, 14 * s, 0, Math.PI * 2);
    ctx.arc(x + 14 * s, y - 6 * s, 16 * s, 0, Math.PI * 2);
    ctx.arc(x + 30 * s, y, 14 * s, 0, Math.PI * 2);
    ctx.rect(x - 5 * s, y, 40 * s, 12 * s);
    ctx.fill();
  }

  // --- Obstacles Collection ---
  let obstacles = [];

  class Cactus {
    constructor(x, size = 1) {
      this.type = 'cactus';
      this.x = x;
      this.size = size; // 1: small single, 2: double, 3: tall
      this.width = size === 3 ? 24 : size === 2 ? 38 : 18;
      this.height = size === 3 ? 46 : 35;
      this.y = GROUND_Y;
    }

    update(dt, currentSpeed) {
      this.x -= currentSpeed * dt;
    }

    getHitbox() {
      return {
        x: this.x + 3,
        y: this.y - this.height + 2,
        width: this.width - 6,
        height: this.height - 4
      };
    }

    draw(ctx, night) {
      ctx.fillStyle = night ? '#8ab4f8' : '#535353';
      const top = this.y - this.height;
      if (this.size === 1) {
        // Single small cactus
        ctx.fillRect(this.x + 5, top, 8, this.height);
        ctx.fillRect(this.x, top + 10, 5, 12);
        ctx.fillRect(this.x + 13, top + 14, 5, 10);
      } else if (this.size === 2) {
        // Double cactus
        ctx.fillRect(this.x + 4, top + 4, 8, this.height - 4);
        ctx.fillRect(this.x, top + 12, 4, 10);
        ctx.fillRect(this.x + 20, top, 8, this.height);
        ctx.fillRect(this.x + 28, top + 10, 5, 12);
      } else {
        // Large single cactus
        ctx.fillRect(this.x + 8, top, 10, this.height);
        ctx.fillRect(this.x, top + 12, 8, 14);
        ctx.fillRect(this.x + 18, top + 16, 8, 14);
      }
    }
  }

  class Pterodactyl {
    constructor(x, heightTier = 'high') {
      this.type = 'pterodactyl';
      this.x = x;
      // High requires ducking, Low requires jump, Med requires jump or careful timing
      this.y = heightTier === 'high' ? GROUND_Y - 32 : GROUND_Y - 14;
      this.width = 44;
      this.height = 24;
      this.wingFrame = 0;
    }

    update(dt, currentSpeed) {
      this.x -= (currentSpeed * 1.1) * dt;
      this.wingFrame += dt * 8;
    }

    getHitbox() {
      return {
        x: this.x + 4,
        y: this.y - this.height + 4,
        width: this.width - 8,
        height: this.height - 6
      };
    }

    draw(ctx, night) {
      ctx.fillStyle = night ? '#f28b82' : '#535353';
      const flapUp = Math.floor(this.wingFrame) % 2 === 0;
      const top = this.y - this.height;

      // Body & Beak
      ctx.fillRect(this.x + 8, top + 10, 24, 8);
      ctx.fillRect(this.x, top + 12, 10, 4); // Beak
      ctx.fillRect(this.x + 28, top + 11, 10, 3); // Tail

      // Wings
      if (flapUp) {
        ctx.fillRect(this.x + 16, top, 12, 10);
      } else {
        ctx.fillRect(this.x + 16, top + 14, 12, 10);
      }
    }
  }

  function checkCollision(boxA, boxB) {
    return (
      boxA.x < boxB.x + boxB.width &&
      boxA.x + boxA.width > boxB.x &&
      boxA.y < boxB.y + boxB.height &&
      boxA.y + boxA.height > boxB.y
    );
  }

  // --- Main Game Loop & Logic ---
  function spawnObstacle() {
    const isPtero = score > 250 && Math.random() < 0.35;
    if (isPtero) {
      const tier = Math.random() < 0.6 ? 'high' : 'low';
      obstacles.push(new Pterodactyl(CANVAS_WIDTH + 20, tier));
    } else {
      const sizeRoll = Math.random();
      const size = sizeRoll < 0.5 ? 1 : sizeRoll < 0.85 ? 2 : 3;
      obstacles.push(new Cactus(CANVAS_WIDTH + 20, size));
    }
    // Enforce minimum safe gap per control bands (INC-001)
    const minSafeTime = 140 / speed;
    nextObstacleDistance = Math.max(minSafeTime, 1.1 + Math.random() * 1.3);
  }

  function startGame() {
    sound.init();
    gameState = STATE.RUNNING;
    score = 0;
    speed = BASE_SPEED;
    obstacles = [];
    dino.reset();
    obstacleTimer = 0.5;
    isNight = false;
    document.body.classList.remove('night-mode');
    startOverlay.classList.add('hidden');
    pauseOverlay.classList.add('hidden');
    gameOverOverlay.classList.add('hidden');
    if (pauseBtn) pauseBtn.textContent = '⏸ PAUSE';
  }

  function togglePause() {
    if (gameState === STATE.RUNNING) {
      gameState = STATE.PAUSED;
      pauseOverlay.classList.remove('hidden');
      if (pauseBtn) pauseBtn.textContent = '▶ RESUME';
    } else if (gameState === STATE.PAUSED) {
      gameState = STATE.RUNNING;
      pauseOverlay.classList.add('hidden');
      if (pauseBtn) pauseBtn.textContent = '⏸ PAUSE';
      lastTime = performance.now();
    }
  }

  function toggleMute() {
    sound.init();
    const newMuted = !sound.isMuted;
    sound.setMuted(newMuted);
    updateMuteDisplay();
  }

  function updateMuteDisplay() {
    if (muteBtn) {
      muteBtn.textContent = sound.isMuted ? '🔇 MUTED' : '🔊 SOUND';
    }
  }

  function gameOver() {
    gameState = STATE.GAMEOVER;
    sound.playHit();
    if (score > hiScore) {
      hiScore = score;
      localStorage.setItem('dino_hi_score', hiScore.toString());
      updateHiScore();
    }
    gameOverOverlay.classList.remove('hidden');
  }

  function updateScore(dt) {
    const oldScore = score;
    score += Math.floor(dt * 10);
    scoreDisplay.textContent = score.toString().padStart(5, '0');

    // Milestone sound every 100 points
    if (Math.floor(score / 100) > Math.floor(oldScore / 100)) {
      sound.playScoreMilestone();
      milestoneFlash = 0.4;
    }

    // Day/Night switch every 700 points
    const cycle = Math.floor(score / 700) % 2 === 1;
    if (cycle !== isNight) {
      isNight = cycle;
      document.body.classList.toggle('night-mode', isNight);
    }

    // Accelerate speed
    speed = BASE_SPEED + Math.min(320, score * 0.22);
  }

  function updateHiScore() {
    hiScoreDisplay.textContent = 'HI ' + hiScore.toString().padStart(5, '0');
  }

  function update(dt) {
    if (gameState !== STATE.RUNNING) return;

    updateScore(dt);
    dino.update(dt);

    // Scroll ground & clouds
    groundOffset = (groundOffset + speed * dt) % CANVAS_WIDTH;
    clouds.forEach(c => {
      c.x -= speed * 0.2 * dt;
      if (c.x < -60) c.x = CANVAS_WIDTH + 40;
    });

    // Spawn & update obstacles
    obstacleTimer -= dt;
    if (obstacleTimer <= 0) {
      spawnObstacle();
      obstacleTimer = nextObstacleDistance;
    }

    const dinoBox = dino.getHitbox();

    for (let i = obstacles.length - 1; i >= 0; i--) {
      const obs = obstacles[i];
      obs.update(dt, speed);

      // Collision Check
      if (checkCollision(dinoBox, obs.getHitbox())) {
        gameOver();
        break;
      }

      // Cleanup offscreen
      if (obs.x < -60) {
        obstacles.splice(i, 1);
      }
    }
  }

  function draw() {
    // Clear canvas
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    // Night Mode backdrop fill
    if (isNight) {
      ctx.fillStyle = '#202124';
      ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
      // Stars
      ctx.fillStyle = '#ffffff';
      for (let i = 0; i < 15; i++) {
        const sx = (i * 53 + groundOffset * 0.05) % CANVAS_WIDTH;
        const sy = (i * 17) % 110 + 15;
        ctx.fillRect(sx, sy, 2, 2);
      }
    }

    // Clouds
    clouds.forEach(c => drawCloud(ctx, c.x, c.y, c.scale, isNight));

    // Ground Line
    ctx.strokeStyle = isNight ? '#5f6368' : '#535353';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, GROUND_Y);
    ctx.lineTo(CANVAS_WIDTH, GROUND_Y);
    ctx.stroke();

    // Ground Bumps / Pebbles
    ctx.fillStyle = isNight ? '#5f6368' : '#70757a';
    for (let x = 0; x < CANVAS_WIDTH; x += 36) {
      const px = (x - groundOffset) % CANVAS_WIDTH;
      const actualX = px < 0 ? px + CANVAS_WIDTH : px;
      ctx.fillRect(actualX, GROUND_Y + 4, 3, 2);
      if (x % 72 === 0) {
        ctx.fillRect(actualX + 10, GROUND_Y + 7, 5, 2);
      }
    }

    // Obstacles
    obstacles.forEach(obs => obs.draw(ctx, isNight));

    // Dinosaur
    dino.draw(ctx, isNight);
  }

  function loop(timestamp) {
    if (!lastTime) lastTime = timestamp;
    const dt = Math.min((timestamp - lastTime) / 1000, 0.05); // Cap to avoid spiraling
    lastTime = timestamp;

    update(dt);
    draw();

    requestAnimationFrame(loop);
  }

  // --- Input Handlers ---
  window.addEventListener('keydown', e => {
    if (e.code === 'KeyP') {
      e.preventDefault();
      togglePause();
      return;
    }
    if (e.code === 'KeyM') {
      e.preventDefault();
      toggleMute();
      return;
    }

    if (e.code === 'Space' || e.code === 'ArrowUp') {
      e.preventDefault();
      if (gameState === STATE.PAUSED) {
        togglePause();
      } else if (gameState === STATE.IDLE || gameState === STATE.GAMEOVER) {
        startGame();
      } else {
        dino.jump();
      }
    } else if (e.code === 'ArrowDown') {
      e.preventDefault();
      dino.duck(true);
    }
  });

  window.addEventListener('keyup', e => {
    if (e.code === 'ArrowDown') {
      dino.duck(false);
    }
  });

  canvas.addEventListener('pointerdown', () => {
    if (gameState === STATE.PAUSED) {
      togglePause();
    } else if (gameState === STATE.IDLE || gameState === STATE.GAMEOVER) {
      startGame();
    } else {
      dino.jump();
    }
  });

  if (pauseBtn) pauseBtn.addEventListener('click', togglePause);
  if (resumeBtn) resumeBtn.addEventListener('click', togglePause);
  if (muteBtn) muteBtn.addEventListener('click', toggleMute);

  restartBtn.addEventListener('click', () => {
    startGame();
  });

  jumpBtn.addEventListener('pointerdown', e => {
    e.preventDefault();
    if (gameState === STATE.PAUSED) {
      togglePause();
    } else if (gameState === STATE.IDLE || gameState === STATE.GAMEOVER) {
      startGame();
    } else {
      dino.jump();
    }
  });

  duckBtn.addEventListener('pointerdown', e => {
    e.preventDefault();
    dino.duck(true);
  });

  duckBtn.addEventListener('pointerup', () => dino.duck(false));
  duckBtn.addEventListener('pointerleave', () => dino.duck(false));

  // Initialize display
  updateHiScore();
  updateMuteDisplay();
  requestAnimationFrame(loop);
})();
