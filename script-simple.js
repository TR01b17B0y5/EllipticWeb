/**
 * EllipticWeb - Simplified Demo Version
 * Demonstrates UI functionality without external dependencies
 */

class EllipticWebDemo {
    constructor() {
        this.currentCurve = 'secp256k1';
        this.savedKeys = this.loadSavedKeys();
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupTheme();
        this.renderSavedKeys();
        this.hideToast(); // Hide initial error
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });

        // Theme toggle
        document.getElementById('theme-toggle').addEventListener('click', () => this.toggleTheme());

        // Help modal
        document.getElementById('help-btn').addEventListener('click', () => this.showModal('help-modal'));
        document.querySelector('.close-btn').addEventListener('click', () => this.hideModal('help-modal'));
        document.getElementById('help-modal').addEventListener('click', (e) => {
            if (e.target.id === 'help-modal') this.hideModal('help-modal');
        });

        // Key generation (demo)
        document.getElementById('curve-select').addEventListener('change', (e) => this.changeCurve(e.target.value));
        document.getElementById('generate-keys').addEventListener('click', () => this.generateKeysDemo());
        document.getElementById('download-keys').addEventListener('click', () => this.downloadKeys());

        // Encryption/Decryption (demo)
        document.getElementById('encrypt-btn').addEventListener('click', () => this.encryptMessageDemo());
        document.getElementById('decrypt-btn').addEventListener('click', () => this.decryptMessageDemo());

        // Digital Signature (demo)
        document.getElementById('sign-btn').addEventListener('click', () => this.signMessageDemo());
        document.getElementById('verify-btn').addEventListener('click', () => this.verifySignatureDemo());

        // Key management
        document.getElementById('import-btn').addEventListener('click', () => this.importKeys());
        document.getElementById('file-input').addEventListener('change', (e) => this.handleFileSelect(e));

        // Copy buttons
        document.querySelectorAll('.btn-copy').forEach(btn => {
            btn.addEventListener('click', (e) => this.copyToClipboard(e.target.dataset.target));
        });
    }

    setupTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        this.updateThemeIcon(savedTheme);
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        this.updateThemeIcon(newTheme);
        this.showToast(`Switched to ${newTheme} theme`, 'success');
    }

    updateThemeIcon(theme) {
        const icon = document.querySelector('#theme-toggle i');
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }

    changeCurve(curveName) {
        this.currentCurve = curveName;
        this.showToast(`Switched to ${curveName} curve`, 'success');
    }

    switchTab(tabId) {
        // Update active tab button
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');

        // Update active tab panel
        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        document.getElementById(tabId).classList.add('active');
    }

    generateKeysDemo() {
        this.showLoading();
        
        // Simulate key generation with random hex strings
        setTimeout(() => {
            const privateKey = this.generateRandomHex(64);
            const publicKey = '04' + this.generateRandomHex(128);

            // Display keys
            document.getElementById('private-key').value = privateKey;
            document.getElementById('public-key').value = publicKey;
            document.getElementById('key-output').style.display = 'block';

            this.showToast('Demo key pair generated successfully!', 'success');
            this.hideLoading();
        }, 1000);
    }

    generateRandomHex(length) {
        const chars = '0123456789abcdef';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    downloadKeys() {
        const privateKey = document.getElementById('private-key').value;
        const publicKey = document.getElementById('public-key').value;
        
        if (!privateKey || !publicKey) {
            this.showToast('No keys to download. Generate keys first.', 'warning');
            return;
        }

        const keyData = {
            curve: this.currentCurve,
            privateKey: privateKey,
            publicKey: publicKey,
            timestamp: new Date().toISOString()
        };

        const blob = new Blob([JSON.stringify(keyData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `elliptic-keys-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);

        // Save to local storage
        this.saveKeys(keyData);
        this.showToast('Keys downloaded and saved!', 'success');
    }

    encryptMessageDemo() {
        const publicKey = document.getElementById('encrypt-public-key').value.trim();
        const message = document.getElementById('message-input').value.trim();

        if (!publicKey || !message) {
            this.showToast('Please provide both public key and message', 'warning');
            return;
        }

        this.showLoading();

        setTimeout(() => {
            const encrypted = {
                message: btoa(message), // Base64 encode for demo
                signature: this.generateRandomHex(128),
                publicKey: publicKey,
                timestamp: new Date().toISOString()
            };

            document.getElementById('crypto-result').value = JSON.stringify(encrypted, null, 2);
            document.getElementById('crypto-output').style.display = 'block';
            
            this.showToast('Message encrypted successfully! (Demo)', 'success');
            this.hideLoading();
        }, 800);
    }

    decryptMessageDemo() {
        const encryptedData = document.getElementById('message-input').value.trim();

        if (!encryptedData) {
            this.showToast('Please provide encrypted data', 'warning');
            return;
        }

        this.showLoading();

        setTimeout(() => {
            try {
                const data = JSON.parse(encryptedData);
                const decrypted = atob(data.message); // Base64 decode
                
                document.getElementById('crypto-result').value = decrypted;
                document.getElementById('crypto-output').style.display = 'block';
                
                this.showToast('Message decrypted successfully! (Demo)', 'success');
                
            } catch (error) {
                this.showToast('Invalid encrypted data format', 'error');
            }
            this.hideLoading();
        }, 800);
    }

    signMessageDemo() {
        const privateKey = document.getElementById('sign-private-key').value.trim();
        const message = document.getElementById('message-to-sign').value.trim();

        if (!privateKey || !message) {
            this.showToast('Please provide both private key and message', 'warning');
            return;
        }

        this.showLoading();

        setTimeout(() => {
            const signatureData = {
                message: message,
                signature: this.generateRandomHex(128),
                publicKey: '04' + this.generateRandomHex(128),
                curve: this.currentCurve,
                timestamp: new Date().toISOString()
            };

            document.getElementById('signature-result').value = JSON.stringify(signatureData, null, 2);
            document.getElementById('signature-output').style.display = 'block';
            
            this.showToast('Message signed successfully! (Demo)', 'success');
            this.hideLoading();
        }, 800);
    }

    verifySignatureDemo() {
        const signatureData = document.getElementById('message-to-sign').value.trim();

        if (!signatureData) {
            this.showToast('Please provide signature data', 'warning');
            return;
        }

        this.showLoading();

        setTimeout(() => {
            try {
                const data = JSON.parse(signatureData);
                const isValid = Math.random() > 0.3; // Random validation for demo

                document.getElementById('signature-result').value = 
                    `Signature verification: ${isValid ? 'VALID' : 'INVALID'} (Demo)\n` +
                    `Message: ${data.message}\n` +
                    `Public Key: ${data.publicKey}`;
                document.getElementById('signature-output').style.display = 'block';
                
                this.showToast(`Signature is ${isValid ? 'valid' : 'invalid'}! (Demo)`, isValid ? 'success' : 'error');
                
            } catch (error) {
                this.showToast('Invalid signature data format', 'error');
            }
            this.hideLoading();
        }, 800);
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const keyData = JSON.parse(e.target.result);
                this.importKeyData(keyData);
            } catch (error) {
                this.showToast('Invalid key file format', 'error');
            }
        };
        reader.readAsText(file);
    }

    importKeys() {
        document.getElementById('file-input').click();
    }

    importKeyData(keyData) {
        if (!keyData.privateKey || !keyData.publicKey) {
            this.showToast('Invalid key data structure', 'error');
            return;
        }

        this.saveKeys(keyData);
        this.renderSavedKeys();
        this.showToast('Keys imported successfully!', 'success');
    }

    saveKeys(keyData) {
        const keyId = `key_${Date.now()}`;
        this.savedKeys[keyId] = {
            ...keyData,
            id: keyId,
            name: `Key ${Object.keys(this.savedKeys).length + 1}`
        };
        localStorage.setItem('elliptic_keys', JSON.stringify(this.savedKeys));
    }

    loadSavedKeys() {
        try {
            return JSON.parse(localStorage.getItem('elliptic_keys')) || {};
        } catch {
            return {};
        }
    }

    renderSavedKeys() {
        const keysList = document.getElementById('keys-list');
        const keys = Object.values(this.savedKeys);

        if (keys.length === 0) {
            keysList.innerHTML = '<p class="no-keys">No keys saved yet. Generate or import keys to get started.</p>';
            return;
        }

        keysList.innerHTML = keys.map(key => `
            <div class="key-card">
                <div class="key-card-header">
                    <span class="key-card-title">${key.name}</span>
                    <span class="key-card-date">${new Date(key.timestamp).toLocaleDateString()}</span>
                </div>
                <div class="key-card-body">
                    <p><strong>Curve:</strong> ${key.curve}</p>
                    <p><strong>Public Key:</strong> ${key.publicKey.substring(0, 32)}...</p>
                    <div class="actions">
                        <button class="btn btn-secondary" onclick="ellipticWebDemo.loadKey('${key.id}')">
                            💾 Load
                        </button>
                        <button class="btn btn-secondary" onclick="ellipticWebDemo.deleteKey('${key.id}')">
                            🗑️ Delete
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    loadKey(keyId) {
        const keyData = this.savedKeys[keyId];
        if (!keyData) return;

        // Switch to appropriate curve
        document.getElementById('curve-select').value = keyData.curve;
        this.changeCurve(keyData.curve);

        // Display in key generation tab
        document.getElementById('private-key').value = keyData.privateKey;
        document.getElementById('public-key').value = keyData.publicKey;
        document.getElementById('key-output').style.display = 'block';

        // Switch to key generation tab
        this.switchTab('keygen');
        
        this.showToast(`Loaded key: ${keyData.name}`, 'success');
    }

    deleteKey(keyId) {
        if (confirm('Are you sure you want to delete this key?')) {
            delete this.savedKeys[keyId];
            localStorage.setItem('elliptic_keys', JSON.stringify(this.savedKeys));
            this.renderSavedKeys();
            this.showToast('Key deleted', 'success');
        }
    }

    copyToClipboard(targetId) {
        const element = document.getElementById(targetId);
        element.select();
        document.execCommand('copy');
        this.showToast('Copied to clipboard!', 'success');
    }

    showModal(modalId) {
        document.getElementById(modalId).classList.add('active');
    }

    hideModal(modalId) {
        document.getElementById(modalId).classList.remove('active');
    }

    showLoading() {
        document.getElementById('loading').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;

        const container = document.getElementById('toast-container');
        container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 4000);
    }

    hideToast() {
        document.querySelectorAll('.toast').forEach(toast => toast.remove());
    }
}

// Initialize the demo application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.ellipticWebDemo = new EllipticWebDemo();
});

// Handle keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + ? for help
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        document.getElementById('help-btn').click();
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            modal.classList.remove('active');
        });
    }
});