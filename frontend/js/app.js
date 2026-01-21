/**
 * Frontend Application Logic
 */

const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const modelSelect = document.getElementById('model-select');
const userInput = document.getElementById('user-input');
const submitBtn = document.getElementById('submit-btn');
const btnText = submitBtn.querySelector('.btn-text');
const btnLoader = submitBtn.querySelector('.btn-loader');
const outputContent = document.getElementById('output-content');
const copyBtn = document.getElementById('copy-btn');
const modelInfo = document.getElementById('model-info');
const apiStatus = document.getElementById('api-status');

async function init() {
    await checkApiStatus();
    await loadModels();
    setupEventListeners();
}

async function checkApiStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            apiStatus.textContent = 'Online';
            apiStatus.className = 'status-indicator online';
        } else {
            throw new Error('API not healthy');
        }
    } catch (error) {
        apiStatus.textContent = 'Offline';
        apiStatus.className = 'status-indicator offline';
    }
}

async function loadModels() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/models`);
        const data = await response.json();

        modelSelect.innerHTML = '';

        if (data.models && data.models.length > 0) {
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = formatModelName(model);
                modelSelect.appendChild(option);
            });
        } else {
            modelSelect.innerHTML = '<option value="">No models available</option>';
        }
    } catch (error) {
        modelSelect.innerHTML = '<option value="">Failed to load models</option>';
    }
}

function formatModelName(name) {
    return name.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

function setupEventListeners() {
    submitBtn.addEventListener('click', handleSubmit);
    copyBtn.addEventListener('click', handleCopy);

    userInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            handleSubmit();
        }
    });
}

async function handleSubmit() {
    const endpoint = modelSelect.value;
    const input = userInput.value.trim();

    if (!endpoint) {
        showError('Please select a model');
        return;
    }

    if (!input) {
        showError('Please enter some input');
        return;
    }

    setLoading(true);
    clearOutput();

    try {
        const response = await fetch(`${API_BASE_URL}/api/${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: input })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Request failed');
        }

        const data = await response.json();
        showOutput(data.output, data.endpoint);

    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

function showOutput(text, endpoint) {
    outputContent.textContent = text;
    outputContent.className = 'output-content success';
    modelInfo.textContent = formatModelName(endpoint);
    modelInfo.hidden = false;
    copyBtn.hidden = false;
}

function showError(message) {
    outputContent.textContent = `Error: ${message}`;
    outputContent.className = 'output-content error';
    modelInfo.hidden = true;
    copyBtn.hidden = true;
}

function clearOutput() {
    outputContent.innerHTML = '<p class="placeholder">Processing...</p>';
    outputContent.className = 'output-content';
    modelInfo.hidden = true;
    copyBtn.hidden = true;
}

function setLoading(loading) {
    submitBtn.disabled = loading;
    btnText.hidden = loading;
    btnLoader.hidden = !loading;
}

async function handleCopy() {
    try {
        await navigator.clipboard.writeText(outputContent.textContent);
        copyBtn.textContent = 'Copied!';
        setTimeout(() => { copyBtn.textContent = 'Copy'; }, 2000);
    } catch (error) { }
}

document.addEventListener('DOMContentLoaded', init);
