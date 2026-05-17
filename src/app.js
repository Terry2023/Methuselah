// 1. WebSocket + DOM refs
const ws = new WebSocket("ws://127.0.0.1:8000/ws");
const upperTerminal = document.getElementById('upper-terminal');
const lowerTerminal = document.getElementById('lower-terminal');
const inputField = document.getElementById('prompt-in');
let activeCategory = 'gen-know';

// 2. Set GSAP origins
gsap.set("#model-needle", { transformOrigin: "0% 50%", rotation: -180 });
gsap.set("#model-knob-container.knob-img", { transformOrigin: "50% 50%" });
gsap.set("#tool-needle", { transformOrigin: "0% 50%", rotation: -180 });
gsap.set("#tool-knob-container.knob-img", { transformOrigin: "50% 50%" });

function updateTerminal(message, color = "#00ff41", target = upperTerminal) {
    if (!target) return;
    
    const entry = document.createElement('div');
    
    // Logic Gate: If it's the lower terminal, force the Amber status style
    if (target.id === 'lower-terminal') {
        entry.style.color = "#ffaa00"; 
    } else {
        entry.style.color = color;
    }

    entry.innerHTML = message;

    // Insert messages BEFORE the input field in the lower terminal
    if (target.id === 'lower-terminal') {
        target.insertBefore(entry, document.getElementById('prompt-in'));
    } else {
        target.appendChild(entry);
    }

    // Keep the terminal from bloating
    if (target.children.length > 15) {
        target.removeChild(target.firstChild);
    }
    
    target.scrollTop = target.scrollHeight;
}

// 4. WEBSOCKET HANDLERS
ws.onopen = () => {
    updateTerminal("SYSTEM READY: 7950X / RTX 4070 DETECTED", "#00ffff", upperTerminal);
    updateLight('light-ready', 'on');
};

ws.onmessage = (event) => {
    let data;
    try {
        data = JSON.parse(event.data);
    } catch (e) {
        updateTerminal(event.data, "#00ffff", upperTerminal);
        return;
    }

    if (data.light) {
        updateLight(data.light, data.state);
        return;
    }

    if (data.type === "STATUS") {
        updateTerminal(data.message, data.color || "#00ff41", upperTerminal);
        return;
    }

    if (data.type === "RESPONSE" || data.type === "CHAT") {
        const text = data.text || data.response || data.message;
        updateTerminal(`BRAIN: ${text}`, "#00ffff", upperTerminal);
        updateLight('light-thinking', 'off');
        updateLight('light-ready', 'on');
        return;
    }
};

// 5. DIAL CONFIG
const MODEL_SNAP_POINTS = [-180, -120, -60, 0];
const TOOL_SNAP_POINTS = [-180, -120, -60, 0];
let modelDialIndex = 0;
let toolDialIndex = 0;

const angleToModel = { "-180": "qwen", "-120": "llama", "-60": "mistral", "0": "gemma" };
const angleToTool = { "-180": "web", "-120": "cabinet", "-60": "math", "0": "coding" };

const findClosest = (val, arr) => arr.reduce((prev, curr) => Math.abs(curr - val) < Math.abs(prev - val) ? curr : prev);

function updateModelDial(newIndex) {
    modelDialIndex = Math.max(0, Math.min(newIndex, MODEL_SNAP_POINTS.length - 1));
    const angle = MODEL_SNAP_POINTS[modelDialIndex];
    gsap.to(["#model-needle", "#model-knob-container.knob-img"], { rotation: angle, duration: 0.2 });

    if (ws.readyState === 1) {
        ws.send(JSON.stringify({ type: "MODEL_CHANGE", model_id: angleToModel[angle] }));
    }
}

function updateToolDial(newIndex) {
    toolDialIndex = Math.max(0, Math.min(newIndex, TOOL_SNAP_POINTS.length - 1));
    const angle = TOOL_SNAP_POINTS[toolDialIndex];
    gsap.to(["#tool-needle", "#tool-knob-container.knob-img"], { rotation: angle, duration: 0.2 });

    if (ws.readyState === 1) {
        ws.send(JSON.stringify({ type: "TOOL_CHANGE", tool_id: angleToTool[angle] }));
    }
}

// Draggables
Draggable.create("#model-knob-container.knob-img", {
    type: "rotation", bounds: { minRotation: -180, maxRotation: 0 },
    snap: MODEL_SNAP_POINTS,
    onDragEnd: function () {
        const snap = findClosest(this.rotation, MODEL_SNAP_POINTS);
        updateModelDial(MODEL_SNAP_POINTS.indexOf(snap));
    }
});

Draggable.create("#tool-knob-container.knob-img", {
    type: "rotation", bounds: { minRotation: -180, maxRotation: 0 },
    snap: TOOL_SNAP_POINTS,
    onDragEnd: function () {
        const snap = findClosest(this.rotation, TOOL_SNAP_POINTS);
        updateToolDial(TOOL_SNAP_POINTS.indexOf(snap));
    }
});

// 6. UNIFIED INPUT ENGINE
document.addEventListener('keydown', (e) => {
    if (e.code.startsWith('Numpad')) {
        e.preventDefault();
        if (e.code === 'Numpad4') updateModelDial(modelDialIndex - 1);
        if (e.code === 'Numpad6') updateModelDial(modelDialIndex + 1);
        if (e.code === 'Numpad1') updateToolDial(toolDialIndex - 1);
        if (e.code === 'Numpad3') updateToolDial(toolDialIndex + 1);
        return;
    }

    if (document.activeElement !== inputField) {
        inputField.focus();
    }

    if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
});

// 7. Debounced Sliders
let sliderTimeout;
function linkSliderToThumb(sliderId, thumbId) {
    const slider = document.getElementById(sliderId);
    const thumb = document.getElementById(thumbId);
    if (!slider || !thumb) return;
    slider.addEventListener('input', () => {
        const percent = ((slider.value - slider.min) / (slider.max - slider.min)) * 100;
        thumb.style.left = `${percent}%`;

        clearTimeout(sliderTimeout);
        sliderTimeout = setTimeout(() => {
            if (ws.readyState === 1) {
                ws.send(JSON.stringify({ type: "SLIDER_CHANGE", slider: sliderId, value: slider.value }));
            }
        }, 150);
    });
}
['memory','accuracy','brevity','creativity','repetition','inference'].forEach(s => linkSliderToThumb(`${s}-slider`, `${s}-thumb`));

// 8. Config & Lights
let masterConfig = null;
let statusLightMap = {};

fetch('./config.json').then(r => r.json()).then(data => {
    masterConfig = data;
    initStatusLights(data.status_lights);
    initCategoryButtons();
    const defaultBtn = document.getElementById(activeCategory);
    if (defaultBtn) defaultBtn.classList.add('active');
});

function initStatusLights(lights) {
    const container = document.querySelector('.dashboard-stage');
    if (!container) {
        console.error("Initialization Error: .dashboard-stage not found in HTML.");
        return;
    }

    lights.forEach(light => {
        let img = document.getElementById(light.id);
        if (!img) {
            img = document.createElement('img');
            img.id = light.id;
            container.appendChild(img);
        }

        img.className = 'status-light off';
        img.src = `assets/${light.file}`;
        img.style.position = 'absolute';
        img.style.top = light.top;
        img.style.left = light.left;
        img.style.width = light.width;
        img.style.opacity = light.opacity || 0.2;
        statusLightMap[light.id] = light.file;
    });
}

function updateLight(id, state) {
    const light = document.getElementById(id);
    if (!light || !statusLightMap[id]) return;

    light.classList.remove('on', 'dim', 'off');

    if (state === 'on') {
        light.classList.add('on');
        light.style.opacity = "1.0";
    } else if (state === 'dim') {
        light.classList.add('dim');
        light.style.opacity = "0.5";
    } else if (state === 'off') {
        light.classList.add('off');
        light.style.opacity = masterConfig.status_lights.find(l => l.id === id).opacity || 0.2;
    }
}

function sendMessage() {
    const inputElement = document.getElementById('prompt-in');
    if (!inputElement || inputElement.value.trim() === "" || ws.readyState !== 1) return;

    updateLight('light-thinking', 'on');
    updateLight('light-ready', 'off');

    // NEW: Get the current tool from the dial (angleToTool[angle])
    const currentTool = angleToTool[TOOL_SNAP_POINTS[toolDialIndex]];

    let systemPrompt = "";
    if (masterConfig && masterConfig.categories) {
        const currentGate = masterConfig.categories.find(cat => cat.id === activeCategory);
        if (currentGate && currentGate.guardrail) {
            systemPrompt = currentGate.guardrail;
        }
    }

    updateTerminal(`OUTBOUND GATE: ${activeCategory.toUpperCase()}`, "#555555", lowerTerminal);

    ws.send(JSON.stringify({
        type: "PROMPT",
        text: inputElement.value,
        system: systemPrompt,
        category: activeCategory,
        tool_id: currentTool  // <--- CRITICAL FIX: Add this line
    }));

    inputElement.value = "";
}

function initCategoryButtons() {
    const buttons = document.querySelectorAll('.cat-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeCategory = btn.id;
            updateTerminal(`GATE OPEN: ${activeCategory.toUpperCase()}`, "#ffff00", lowerTerminal);
        });
    });
}