// EllipticWeb JavaScript Application

class EllipticWebApp {
    constructor() {
        this.currentCurve = 'P-256';
        this.generatedKeys = null;
        this.lastSignature = null;
        
        this.initializeEventListeners();
        this.loadCurveInfo();
    }
    
    initializeEventListeners() {
        // Curve selection
        document.getElementById('curve-select').addEventListener('change', (e) => {
            this.currentCurve = e.target.value;
            this.loadCurveInfo();
        });
        
        // Curve info button
        document.getElementById('curve-info-btn').addEventListener('click', () => {
            this.toggleCurveInfo();
        });
        
        // Key generation
        document.getElementById('generate-keys-btn').addEventListener('click', () => {
            this.generateKeys();
        });
        
        // Digital signature
        document.getElementById('sign-btn').addEventListener('click', () => {
            this.signMessage();
        });
        
        // Signature verification
        document.getElementById('verify-btn').addEventListener('click', () => {
            this.verifySignature();
        });
        
        // Quick actions
        document.getElementById('copy-keys-btn').addEventListener('click', () => {
            this.copyKeysToSignature();
        });
        
        document.getElementById('copy-signature-btn').addEventListener('click', () => {
            this.copySignatureToVerification();
        });
        
        document.getElementById('clear-all-btn').addEventListener('click', () => {
            this.clearAllFields();
        });
        
        // Modal close handlers
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', () => {
                this.hideModal();
            });
        });
        
        // Close modal on overlay click
        document.getElementById('error-modal').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) {
                this.hideModal();
            }
        });
    }
    
    async loadCurveInfo() {
        try {
            const response = await fetch(`/api/curve_info/${this.currentCurve}`);
            const data = await response.json();
            
            if (data.success) {
                this.displayCurveInfo(data.curve);
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            console.error('Error loading curve info:', error);
            this.showError('Failed to load curve information');
        }
    }
    
    displayCurveInfo(curve) {
        const infoPanel = document.getElementById('curve-info');
        infoPanel.innerHTML = `
            <h3>Curve Parameters for ${curve.name}</h3>
            <div class="curve-params">
                <div class="param-item">
                    <strong>Key Size:</strong> ${curve.key_size_bits} bits
                </div>
                <div class="param-item">
                    <strong>Prime Modulus (p):</strong>
                    <div class="param-value">${this.formatHex(curve.prime_modulus)}</div>
                </div>
                <div class="param-item">
                    <strong>Coefficient a:</strong>
                    <div class="param-value">${this.formatHex(curve.coefficient_a)}</div>
                </div>
                <div class="param-item">
                    <strong>Coefficient b:</strong>
                    <div class="param-value">${this.formatHex(curve.coefficient_b)}</div>
                </div>
                <div class="param-item">
                    <strong>Generator Point X:</strong>
                    <div class="param-value">${this.formatHex(curve.generator_point.x)}</div>
                </div>
                <div class="param-item">
                    <strong>Generator Point Y:</strong>
                    <div class="param-value">${this.formatHex(curve.generator_point.y)}</div>
                </div>
                <div class="param-item">
                    <strong>Order (n):</strong>
                    <div class="param-value">${this.formatHex(curve.order)}</div>
                </div>
                <div class="param-item">
                    <strong>Cofactor:</strong> ${curve.cofactor}
                </div>
            </div>
        `;
    }
    
    toggleCurveInfo() {
        const infoPanel = document.getElementById('curve-info');
        infoPanel.classList.toggle('hidden');
    }
    
    async generateKeys() {
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/generate_keys', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    curve: this.currentCurve
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.generatedKeys = data;
                this.displayGeneratedKeys(data);
                document.getElementById('copy-keys-btn').disabled = false;
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            console.error('Error generating keys:', error);
            this.showError('Failed to generate keys');
        } finally {
            this.showLoading(false);
        }
    }
    
    displayGeneratedKeys(keyData) {
        document.getElementById('private-key').textContent = keyData.private_key;
        document.getElementById('public-key-x').textContent = keyData.public_key.x;
        document.getElementById('public-key-y').textContent = keyData.public_key.y;
        document.getElementById('key-size-info').textContent = `${keyData.key_size} bits`;
        document.getElementById('curve-info-badge').textContent = keyData.curve;
        
        document.getElementById('key-result').classList.remove('hidden');
    }
    
    async signMessage() {
        const message = document.getElementById('message-to-sign').value.trim();
        const privateKey = document.getElementById('signing-private-key').value.trim();
        
        if (!message || !privateKey) {
            this.showError('Please enter both a message and private key');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/sign', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    private_key: privateKey,
                    curve: this.currentCurve
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.lastSignature = data;
                this.displaySignature(data);
                document.getElementById('copy-signature-btn').disabled = false;
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            console.error('Error signing message:', error);
            this.showError('Failed to sign message');
        } finally {
            this.showLoading(false);
        }
    }
    
    displaySignature(signatureData) {
        document.getElementById('signature-r').textContent = signatureData.signature.r;
        document.getElementById('signature-s').textContent = signatureData.signature.s;
        
        document.getElementById('signature-result').classList.remove('hidden');
    }
    
    async verifySignature() {
        const message = document.getElementById('message-to-verify').value.trim();
        const publicKeyX = document.getElementById('verification-public-key-x').value.trim();
        const publicKeyY = document.getElementById('verification-public-key-y').value.trim();
        const signatureR = document.getElementById('verification-signature-r').value.trim();
        const signatureS = document.getElementById('verification-signature-s').value.trim();
        
        if (!message || !publicKeyX || !publicKeyY || !signatureR || !signatureS) {
            this.showError('Please fill in all verification fields');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    signature: {
                        r: signatureR,
                        s: signatureS
                    },
                    public_key: {
                        x: publicKeyX,
                        y: publicKeyY
                    },
                    curve: this.currentCurve
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayVerificationResult(data.valid);
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            console.error('Error verifying signature:', error);
            this.showError('Failed to verify signature');
        } finally {
            this.showLoading(false);
        }
    }
    
    displayVerificationResult(isValid) {
        const statusElement = document.getElementById('verification-status');
        
        if (isValid) {
            statusElement.textContent = '✅ Signature is VALID';
            statusElement.className = 'verification-status valid';
        } else {
            statusElement.textContent = '❌ Signature is INVALID';
            statusElement.className = 'verification-status invalid';
        }
        
        document.getElementById('verification-result').classList.remove('hidden');
    }
    
    copyKeysToSignature() {
        if (!this.generatedKeys) {
            this.showError('No keys generated to copy');
            return;
        }
        
        document.getElementById('signing-private-key').value = this.generatedKeys.private_key;
        
        // Scroll to signature section
        document.querySelector('#message-to-sign').scrollIntoView({ behavior: 'smooth' });
    }
    
    copySignatureToVerification() {
        if (!this.lastSignature || !this.generatedKeys) {
            this.showError('No signature or keys to copy');
            return;
        }
        
        // Copy message
        document.getElementById('message-to-verify').value = document.getElementById('message-to-sign').value;
        
        // Copy public key
        document.getElementById('verification-public-key-x').value = this.generatedKeys.public_key.x;
        document.getElementById('verification-public-key-y').value = this.generatedKeys.public_key.y;
        
        // Copy signature
        document.getElementById('verification-signature-r').value = this.lastSignature.signature.r;
        document.getElementById('verification-signature-s').value = this.lastSignature.signature.s;
        
        // Scroll to verification section
        document.querySelector('#message-to-verify').scrollIntoView({ behavior: 'smooth' });
    }
    
    clearAllFields() {
        // Clear key generation results
        document.getElementById('key-result').classList.add('hidden');
        this.generatedKeys = null;
        document.getElementById('copy-keys-btn').disabled = true;
        
        // Clear signature fields and results
        document.getElementById('message-to-sign').value = '';
        document.getElementById('signing-private-key').value = '';
        document.getElementById('signature-result').classList.add('hidden');
        this.lastSignature = null;
        document.getElementById('copy-signature-btn').disabled = true;
        
        // Clear verification fields and results
        document.getElementById('message-to-verify').value = '';
        document.getElementById('verification-public-key-x').value = '';
        document.getElementById('verification-public-key-y').value = '';
        document.getElementById('verification-signature-r').value = '';
        document.getElementById('verification-signature-s').value = '';
        document.getElementById('verification-result').classList.add('hidden');
        
        // Hide curve info
        document.getElementById('curve-info').classList.add('hidden');
    }
    
    formatHex(hexString) {
        // Add line breaks for long hex strings
        if (hexString.length > 64) {
            return hexString.match(/.{1,64}/g).join('<br>');
        }
        return hexString;
    }
    
    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        if (show) {
            overlay.classList.remove('hidden');
        } else {
            overlay.classList.add('hidden');
        }
    }
    
    showError(message) {
        document.getElementById('error-message').textContent = message;
        document.getElementById('error-modal').classList.remove('hidden');
    }
    
    hideModal() {
        document.getElementById('error-modal').classList.add('hidden');
    }
}

// CSS for curve parameters display
const curveParamsCSS = `
    .curve-params {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    
    .param-item {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    
    .param-item strong {
        color: #4facfe;
        font-weight: 600;
    }
    
    .param-value {
        font-family: 'Courier New', monospace;
        font-size: 11px;
        background: white;
        padding: 8px;
        border-radius: 4px;
        border: 1px solid #ddd;
        word-break: break-all;
        line-height: 1.4;
    }
`;

// Add dynamic CSS
const style = document.createElement('style');
style.textContent = curveParamsCSS;
document.head.appendChild(style);

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EllipticWebApp();
});

// Handle keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+G for generate keys
    if (e.ctrlKey && e.key === 'g') {
        e.preventDefault();
        document.getElementById('generate-keys-btn').click();
    }
    
    // Escape to close modal
    if (e.key === 'Escape') {
        document.getElementById('error-modal').classList.add('hidden');
    }
});