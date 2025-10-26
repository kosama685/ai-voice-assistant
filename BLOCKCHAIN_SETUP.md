# Blockchain Integration Setup Guide

## Overview

The Voice Assistant now supports cryptocurrency payments through a Solidity smart contract deployed on Ethereum-compatible blockchains. This guide covers setup, deployment, and integration.

---

## Prerequisites

1. **Node.js & npm** - For Hardhat development
2. **Python Web3.py** - Already in requirements
3. **MetaMask** - For wallet management
4. **Testnet ETH** - For testing (Sepolia, Mumbai, etc.)

---

## Step 1: Install Dependencies

### Python Dependencies

```bash
pip install web3==6.11.0
pip install eth-account==0.10.0
```

### Node.js Dependencies (for contract deployment)

```bash
npm install --save-dev hardhat
npm install --save-dev @openzeppelin/contracts
npm install --save-dev @nomicfoundation/hardhat-toolbox
npm install dotenv
```

---

## Step 2: Setup Hardhat Project

```bash
# Initialize Hardhat
npx hardhat

# Select "Create a basic sample project"
# Select "Yes" for .gitignore
# Select "Yes" for dependencies
```

---

## Step 3: Configure Environment Variables

Add to `.env`:

```env
# Blockchain Configuration
WEB3_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
PRIVATE_KEY=your_private_key_here
ACCOUNT_ADDRESS=your_wallet_address_here
CONTRACT_ADDRESS=deployed_contract_address_here

# Token Addresses (Sepolia Testnet)
USDC_ADDRESS=0x1c7D4B196Cb0C6f48185d377e3B6F0Ac11d4C5e8
USDT_ADDRESS=0xaA8E23Fb1079EA71e0a56F48a2aA51851D8433D0

# Alchemy API Key
ALCHEMY_API_KEY=your_alchemy_key_here
```

---

## Step 4: Deploy Smart Contract

### Create `hardhat.config.js`:

```javascript
require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: "0.8.0",
  networks: {
    sepolia: {
      url: process.env.WEB3_RPC_URL,
      accounts: [process.env.PRIVATE_KEY]
    },
    mumbai: {
      url: `https://polygon-mumbai.g.alchemy.com/v2/${process.env.ALCHEMY_API_KEY}`,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};
```

### Create `scripts/deploy.js`:

```javascript
const hre = require("hardhat");

async function main() {
  const VoiceAssistantSubscription = await hre.ethers.getContractFactory("VoiceAssistantSubscription");
  const treasury = process.env.ACCOUNT_ADDRESS;
  
  console.log("Deploying VoiceAssistantSubscription...");
  const contract = await VoiceAssistantSubscription.deploy(treasury);
  await contract.deployed();
  
  console.log("Contract deployed to:", contract.address);
  console.log("Treasury address:", treasury);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

### Deploy:

```bash
npx hardhat run scripts/deploy.js --network sepolia
```

---

## Step 5: Generate Contract ABI

After deployment, save the ABI to `contracts/abi.json`:

```bash
npx hardhat run scripts/export-abi.js
```

Create `scripts/export-abi.js`:

```javascript
const fs = require('fs');
const path = require('path');

async function main() {
  const artifact = require('../artifacts/contracts/VoiceAssistantSubscription.sol/VoiceAssistantSubscription.json');
  const abi = artifact.abi;
  
  fs.writeFileSync(
    path.join(__dirname, '../contracts/abi.json'),
    JSON.stringify(abi, null, 2)
  );
  
  console.log('ABI exported to contracts/abi.json');
}

main();
```

---

## Step 6: Create Payment Routes

Create `routes/crypto_payment.py`:

```python
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from services.blockchain_service import blockchain_service
from models import db, Transaction, Subscription

crypto_payment_bp = Blueprint('crypto_payment', __name__)

@crypto_payment_bp.route('/api/crypto/subscribe', methods=['POST'])
@login_required
def initiate_subscription():
    """Initiate crypto subscription"""
    data = request.json
    tier = data.get('tier', 1)  # 1=BASIC, 2=PREMIUM, 3=ENTERPRISE
    token = data.get('token', 'ETH')
    
    result = blockchain_service.subscribe(
        current_user.wallet_address,
        tier,
        token
    )
    
    if result['success']:
        return jsonify({
            'success': True,
            'transaction': result['transaction'],
            'message': 'Sign transaction in your wallet'
        })
    
    return jsonify(result), 400

@crypto_payment_bp.route('/api/crypto/verify-payment', methods=['POST'])
@login_required
def verify_payment():
    """Verify payment transaction"""
    data = request.json
    tx_hash = data.get('tx_hash')
    
    result = blockchain_service.verify_transaction(tx_hash)
    
    if result['success']:
        # Update database
        transaction = Transaction(
            user_id=current_user.id,
            amount=data.get('amount'),
            currency='ETH',
            payment_method='crypto',
            status='completed'
        )
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Payment verified',
            'tx_hash': tx_hash
        })
    
    return jsonify(result), 400

@crypto_payment_bp.route('/api/crypto/balance', methods=['GET'])
@login_required
def get_balance():
    """Get user wallet balance"""
    token = request.args.get('token', 'ETH')
    
    result = blockchain_service.get_balance(
        current_user.wallet_address,
        token
    )
    
    return jsonify(result)

@crypto_payment_bp.route('/api/crypto/subscription', methods=['GET'])
@login_required
def get_subscription():
    """Get subscription from blockchain"""
    result = blockchain_service.get_subscription(
        current_user.wallet_address
    )
    
    return jsonify(result)

@crypto_payment_bp.route('/api/crypto/tokens', methods=['GET'])
def get_supported_tokens():
    """Get supported tokens"""
    result = blockchain_service.get_supported_tokens()
    return jsonify(result)
```

---

## Step 7: Update User Model

Add wallet address to User model:

```python
class User(UserMixin, db.Model):
    # ... existing fields ...
    wallet_address = db.Column(db.String(42), unique=True, nullable=True)
    subscription_tier = db.Column(db.String(20), default='free')
```

---

## Step 8: Create Frontend Integration

Create `templates/crypto_payment.html`:

```html
{% extends "base.html" %}

{% block content %}
<div class="container mt-5">
    <h1>Crypto Payment</h1>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Select Subscription Tier</h5>
                </div>
                <div class="card-body">
                    <div class="form-group">
                        <label>Tier</label>
                        <select id="tierSelect" class="form-control">
                            <option value="1">BASIC - $29.99/month</option>
                            <option value="2">PREMIUM - $99.99/month</option>
                            <option value="3">ENTERPRISE - $499.99/month</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Payment Token</label>
                        <select id="tokenSelect" class="form-control">
                            <option value="ETH">Ethereum (ETH)</option>
                            <option value="USDC">USD Coin (USDC)</option>
                            <option value="USDT">Tether (USDT)</option>
                        </select>
                    </div>
                    
                    <button class="btn btn-primary w-100" onclick="initiatePayment()">
                        Pay with Crypto
                    </button>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Wallet Info</h5>
                </div>
                <div class="card-body">
                    <div id="walletInfo">
                        <p>Connect your wallet to see balance</p>
                        <button class="btn btn-outline-primary" onclick="connectWallet()">
                            Connect Wallet
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/web3@1.10.0/dist/web3.min.js"></script>
<script>
    async function connectWallet() {
        if (typeof window.ethereum !== 'undefined') {
            try {
                const accounts = await window.ethereum.request({
                    method: 'eth_requestAccounts'
                });
                document.getElementById('walletInfo').innerHTML = `
                    <p>Connected: ${accounts[0]}</p>
                    <p id="balance">Loading balance...</p>
                `;
                
                // Get balance
                const balance = await web3.eth.getBalance(accounts[0]);
                document.getElementById('balance').textContent = 
                    `Balance: ${web3.utils.fromWei(balance, 'ether')} ETH`;
            } catch (error) {
                alert('Error connecting wallet: ' + error.message);
            }
        } else {
            alert('MetaMask not installed');
        }
    }
    
    async function initiatePayment() {
        const tier = document.getElementById('tierSelect').value;
        const token = document.getElementById('tokenSelect').value;
        
        try {
            const response = await fetch('/api/crypto/subscribe', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({tier, token})
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Sign and send transaction
                const web3 = new Web3(window.ethereum);
                const tx = await web3.eth.sendTransaction(data.transaction);
                
                // Verify payment
                const verifyResponse = await fetch('/api/crypto/verify-payment', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        tx_hash: tx.transactionHash,
                        amount: data.transaction.value
                    })
                });
                
                const verifyData = await verifyResponse.json();
                if (verifyData.success) {
                    alert('Payment successful!');
                    window.location.href = '/dashboard';
                }
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }
</script>
{% endblock %}
```

---

## Step 9: Register Routes

In `app.py`:

```python
from routes.crypto_payment import crypto_payment_bp
app.register_blueprint(crypto_payment_bp)
```

---

## Testing

### Test on Sepolia Testnet

1. Get testnet ETH from [Sepolia Faucet](https://sepoliafaucet.com)
2. Connect MetaMask to Sepolia
3. Test subscription flow
4. Verify transaction on [Etherscan](https://sepolia.etherscan.io)

### Test Locally

```bash
# Start local blockchain
npx hardhat node

# Deploy to local network
npx hardhat run scripts/deploy.js --network localhost
```

---

## Security Considerations

1. **Private Keys**: Never commit `.env` file
2. **Contract Audit**: Have contract audited before mainnet
3. **Rate Limiting**: Add rate limits to payment endpoints
4. **Signature Verification**: Verify wallet signatures
5. **Gas Limits**: Set reasonable gas limits

---

## Supported Networks

- **Ethereum Sepolia** (Testnet)
- **Polygon Mumbai** (Testnet)
- **Ethereum Mainnet** (Production)
- **Polygon Mainnet** (Production)

---

## Troubleshooting

### Contract Not Found
- Verify `CONTRACT_ADDRESS` in `.env`
- Check contract is deployed to correct network

### Transaction Failed
- Check wallet has sufficient balance
- Verify gas price is not too low
- Check contract has approved tokens

### Web3 Connection Error
- Verify `WEB3_RPC_URL` is correct
- Check internet connection
- Try different RPC provider

---

## Resources

- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Solidity Documentation](https://docs.soliditylang.org/)
- [Hardhat Documentation](https://hardhat.org/docs)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)

---

**Last Updated**: 2025-10-26  
**Status**: Production Ready

