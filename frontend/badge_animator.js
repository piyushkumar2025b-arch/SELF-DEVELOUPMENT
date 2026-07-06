// Particle Animation System for Interactive badges
const canvas = document.getElementById('animation-canvas');
const ctx = canvas.getContext('2d');

let particles = [];

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.size = Math.random() * 6 + 2;
        this.speedX = Math.random() * 6 - 3;
        this.speedY = Math.random() * -6 - 2;
        this.gravity = 0.15;
        this.color = color;
        this.alpha = 1;
        this.decay = Math.random() * 0.015 + 0.01;
    }

    update() {
        this.speedY += this.gravity;
        this.x += this.speedX;
        this.y += this.speedY;
        this.alpha -= this.decay;
    }

    draw() {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw();
        if (particles[i].alpha <= 0) {
            particles.splice(i, 1);
            i--;
        }
    }
    requestAnimationFrame(animate);
}
animate();

// Public triggers callable from React JSX
window.triggerParticles = function(x, y, color = '#6366f1') {
    const colors = [color, '#3b82f6', '#10b981', '#fbbf24', '#ec4899'];
    for (let i = 0; i < 20; i++) {
        const randColor = colors[Math.floor(Math.random() * colors.length)];
        particles.push(new Particle(x, y, randColor));
    }
};

window.triggerConfetti = function() {
    const x = canvas.width / 2;
    const y = canvas.height / 2;
    window.triggerParticles(x - 100, y, '#6366f1');
    window.triggerParticles(x + 100, y, '#10b981');
};
