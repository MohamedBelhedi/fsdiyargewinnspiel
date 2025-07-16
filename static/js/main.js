const wheelData = [
  { label: "50€", color: "#90be6d" },
  { label: "Erste Hilfe Gutschein", color: "#f9c74f" },
  { label: "Gratis APP", color: "#f9844a" },
  { label: "250€", color: "#f8961e" },
  { label: "Gratis Fahrstunde", color: "#f3722c" },
  { label: "100€", color: "#00ccff" },
  { label: "Anmeldegebühr", color: "#e63946" }
];

const canvas = document.getElementById("wheelCanvas");
const ctx = canvas.getContext("2d");

const center = canvas.width / 2;
const radius = center - 10;
let angle = 0;
let spinning = false;

// Wheel Drawing Function
const drawWheel = () => {
  const sliceAngle = (2 * Math.PI) / wheelData.length;

  wheelData.forEach((slice, i) => {
    const startAngle = i * sliceAngle;
    const endAngle = startAngle + sliceAngle;

    ctx.beginPath();
    ctx.moveTo(center, center);
    ctx.arc(center, center, radius, startAngle, endAngle);
    ctx.fillStyle = slice.color;
    ctx.fill();

    ctx.save();
    ctx.translate(center, center);
    ctx.rotate(startAngle + sliceAngle / 2);
    ctx.textAlign = "right";
    ctx.fillStyle = "#fff";
    ctx.font = "bold 18px Arial";
    ctx.fillText(slice.label, radius - 20, 10);
    ctx.restore();
  });

  ctx.beginPath();
  ctx.arc(center, center, 40, 0, 2 * Math.PI);
  ctx.fillStyle = "#fff";
  ctx.fill();
};

// Show Result Function
const showResult = (currentAngle) => {
  const sliceAngle = 360 / wheelData.length;
  const adjustedAngle = (currentAngle + 122) % 360;
  const index = Math.floor(((360 - adjustedAngle + sliceAngle / 2) % 360) / sliceAngle);
  const result = wheelData[index].label;

  document.getElementById("resultText").innerText = `Ergebnis: ${result}`;
  document.getElementById("gewinnInput").value = result;

  const resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
  resultModal.show();
};

// Spin Function
const spinWheel = () => {
  if (spinning) return;

  if (localStorage.getItem("hasSpun") === "true") {
    const alreadySpunModal = new bootstrap.Modal(document.getElementById('alreadySpunModal'));
    alreadySpunModal.show();
    return;
  }

  spinning = true;
  document.getElementById("spinButton").disabled = true;

  const randomSpin = Math.floor(Math.random() * 360) + 360 * 5;
  const duration = 5000;
  const start = performance.now();

  const animateSpin = (now) => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    angle = (randomSpin * eased) % 360;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(center, center);
    ctx.rotate((angle * Math.PI) / 180);
    ctx.translate(-center, -center);
    drawWheel();
    ctx.restore();

    if (progress < 1) {
      requestAnimationFrame(animateSpin);
    } else {
      spinning = false;
      localStorage.setItem("hasSpun", "true");
      showResult(angle);
    }
  };

  requestAnimationFrame(animateSpin);
};

// Initial draw
drawWheel();
