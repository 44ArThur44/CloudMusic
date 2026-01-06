// State
let currentMode = null;
let selectedType = 'kick';
let generationParams = {
    bpm: 128,
    intensity: 3,
    duration: 4,
    styles: []
};

// DOM Elements
const modeSection = document.getElementById('modeSection');
const guidedUI = document.getElementById('guidedUI');
const advancedUI = document.getElementById('advancedUI');
const generateBtn = document.getElementById('generateBtn');
const resultsSection = document.getElementById('resultsSection');
const audioPlayer = document.getElementById('audioPlayer');
const downloadBtn = document.getElementById('downloadBtn');

// Mode Selection with disabling other cards
document.querySelectorAll('.mode-card').forEach(card => {
    card.addEventListener('click', function() {
        currentMode = this.dataset.mode;
        modeSection.classList.add('hidden');

        // Disable other cards
        document.querySelectorAll('.mode-card').forEach(otherCard => {
            if (otherCard !== this) {
                otherCard.style.opacity = '0.4';
                otherCard.style.cursor = 'not-allowed';
                otherCard.classList.add('disabled');
            }
        });

        // Enable this card
        this.style.opacity = '1';
        this.style.cursor = 'pointer';

        if (currentMode === 'guided') guidedUI.classList.remove('hidden');
        else advancedUI.classList.remove('hidden');

        generateBtn.classList.remove('hidden');
    });
});

// Guided UI Events
document.querySelectorAll('.type-card').forEach(card => {
    card.addEventListener('click', () => {
        document.querySelectorAll('.type-card').forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        selectedType = card.dataset.type;
    });
});

// Sliders
['bpm', 'intensity', 'duration'].forEach(param => {
    const slider = document.getElementById(`${param}Slider`);
    const valueLabel = document.getElementById(`${param}Value`);
    
    // Initialize from HTML
    generationParams[param] = parseInt(slider.value);
    valueLabel.textContent = slider.value;
    
    slider.addEventListener('input', (e) => {
        generationParams[param] = parseInt(e.target.value);
        valueLabel.textContent = e.target.value;
    });
});

// Toggles
['darkToggle', 'ambientToggle', 'energeticToggle'].forEach(id => {
    document.getElementById(id).addEventListener('change', (e) => {
        const style = id.replace('Toggle', '');
        if (e.target.checked) generationParams.styles.push(style);
        else generationParams.styles = generationParams.styles.filter(s => s !== style);
    });
});

// ===== GENERATE FUNCTION =====
generateBtn.addEventListener('click', async () => {
    const userStatus = await checkUserLimit();
    if (!userStatus.allowed) {
        showBlockedModal(userStatus);
        return;
    }

    if (currentMode === 'advanced') {
        const promptInput = document.getElementById('promptInput');
        const promptText = promptInput.value.trim();
        
        if (promptText.length < 4) {
            promptInput.style.borderColor = '#ff4757';
            promptInput.focus();
            promptInput.placeholder = 'Enter at least 4 characters...';
            return;
        }
        promptInput.style.borderColor = '';
    }

    generateBtn.textContent = 'Generating...';
    generateBtn.classList.add('loading');

    const payload = {
        mode: currentMode
    };
    
    if (currentMode === 'guided') {
        payload.params = {
            type: selectedType,
            bpm: parseInt(generationParams.bpm),
            intensity: parseInt(generationParams.intensity),
            duration: parseInt(generationParams.duration),
            dark: generationParams.styles.includes('dark'),
            ambient: generationParams.styles.includes('ambient'),
            energetic: generationParams.styles.includes('energetic')
        };
        payload.prompt = null;
    } else {
        payload.prompt = document.getElementById('promptInput').value.trim();
        payload.params = {
            duration: parseInt(generationParams.duration)
        };
    }

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const result = await response.json();
            console.log("Backend response:", result);
            
            const audioPath = result.audio_file || result.filename || '';
            const fileNameOnly = audioPath.split('/').pop();
            
            const promptUsed = currentMode === 'advanced' ? payload.prompt : '';
            showResults(fileNameOnly, promptUsed, generationParams);
        } else {
            console.error('Server error:', response.status);
        }
    } catch (error) {
        console.error('Generation failed:', error);
        console.error(error);
    } finally {
        generateBtn.textContent = 'Generate Loop';
        generateBtn.classList.remove('loading');
    }
});

// ===== SHOW RESULTS =====
function showResults(filename, promptUsed, params) {
    console.log("Showing results for:", filename);

    if (currentMode === 'guided') guidedUI.classList.add('hidden');
    else advancedUI.classList.add('hidden');

    generateBtn.classList.add('hidden');
    resultsSection.classList.remove('hidden');

    const oldPreview = document.querySelector('.preview-info');
    if (oldPreview) oldPreview.remove();

    const previewHTML = `
        <div class="preview-info">
            ${promptUsed ? `
                <h3>Prompt used:</h3>
                <p class="prompt-preview">${promptUsed}</p>
            ` : ''}
            <div class="params-grid">
                <div><strong>Mode:</strong> ${currentMode}</div>
                ${currentMode === 'guided' ? 
                    `<div><strong>Type:</strong> ${selectedType}</div>
                     <div><strong>BPM:</strong> ${params.bpm}</div>
                     <div><strong>Intensity:</strong> ${params.intensity}</div>
                     <div><strong>Duration:</strong> ${params.duration}s</div>
                     ${params.styles.length > 0 ? 
                        `<div><strong>Styles:</strong> ${params.styles.join(', ')}</div>` : ''}`
                    : ''}
            </div>
        </div>
    `;
    
    resultsSection.insertAdjacentHTML('afterbegin', previewHTML);

    // CORREÇÃO: Forçar carregamento completo do áudio
    const audioUrl = `/music/${filename}`;
    
    const audio = document.getElementById('audioPlayer');

    audio.src = audioUrl + '?t=' + Date.now();
    audio.load();

    // play permitido porque veio de clique
    audio.play().catch(err => {
        console.log('Autoplay bloqueado, clique manual necessário');
    });
    
audio.addEventListener('loadedmetadata', function () {
    console.log(`Audio duration: ${audio.duration}s`);
});

audio.addEventListener('error', function (e) {
    console.error('Audio loading error:', e);
});

downloadBtn.onclick = () => {
    window.location.href = `/download/${filename}`;
};
    setupNewLoopButton();
}

// Logo click to reset
document.getElementById('siteLogo').addEventListener('click', () => {
    location.reload();
});

// ===== NEW LOOP BUTTON =====
function setupNewLoopButton() {
    const newLoopBtn = document.getElementById('newLoopBtn');
    if (!newLoopBtn) {
        console.log('Button not found yet, retrying...');
        setTimeout(setupNewLoopButton, 100);
        return;
    }

    const newBtn = newLoopBtn.cloneNode(true);
    newLoopBtn.parentNode.replaceChild(newBtn, newLoopBtn);

    newBtn.addEventListener('click', () => {
        console.log('NEW LOOP CLICKED');
        resultsSection.classList.add('hidden');
        modeSection.classList.remove('hidden');
        currentMode = null;
        
        document.querySelectorAll('.mode-card').forEach(card => {
            card.style.opacity = '1';
            card.style.cursor = 'pointer';
            card.classList.remove('disabled');
        });
        
        guidedUI.classList.add('hidden');
        advancedUI.classList.add('hidden');
        generateBtn.classList.add('hidden');
        
        document.querySelectorAll('.type-card').forEach(c => c.classList.remove('selected'));
        
        // Get current slider values on reset
        generationParams = {
            bpm: parseInt(document.getElementById('bpmSlider').value),
            intensity: parseInt(document.getElementById('intensitySlider').value),
            duration: parseInt(document.getElementById('durationSlider').value),
            styles: []
        };
        
        document.getElementById('bpmValue').textContent = generationParams.bpm;
        document.getElementById('intensityValue').textContent = generationParams.intensity;
        document.getElementById('durationValue').textContent = generationParams.duration;
        
        ['darkToggle', 'ambientToggle', 'energeticToggle'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.checked = false;
        });
    });
}

// Initial setup
setupNewLoopButton();

// ===== USER LIMIT / PAYWALL =====

async function checkUserLimit() {
    const response = await fetch('/check-limit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    });

    return await response.json();
}

function showBlockedModal(status) {
    document.getElementById('blockedModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('blockedModal').classList.add('hidden');
}

async function buyCredits() {
    const res = await fetch('/create-checkout-session', { method: 'POST' });
    const data = await res.json();
    window.location.href = data.url;
}