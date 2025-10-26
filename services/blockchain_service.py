"""
Blockchain Service - Crypto Payment Integration
Handles Web3 interactions with smart contracts
"""

import os
import json
from typing import Dict, Any, Optional
from web3 import Web3
from datetime import datetime

class BlockchainService:
    """Service for blockchain interactions"""
    
    def __init__(self):
        # Initialize Web3
        self.rpc_url = os.environ.get('WEB3_RPC_URL', 'https://eth-sepolia.g.alchemy.com/v2/demo')
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        # Contract details
        self.contract_address = os.environ.get('CONTRACT_ADDRESS', '')
        self.contract_abi = self._load_contract_abi()
        self.private_key = os.environ.get('PRIVATE_KEY', '')
        self.account_address = os.environ.get('ACCOUNT_ADDRESS', '')
        
        # Initialize contract
        if self.contract_address and self.contract_abi:
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.contract_address),
                abi=self.contract_abi
            )
        else:
            self.contract = None
        
        # Supported tokens
        self.supported_tokens = {
            'ETH': '0x0000000000000000000000000000000000000000',
            'USDC': os.environ.get('USDC_ADDRESS', ''),
            'USDT': os.environ.get('USDT_ADDRESS', ''),
        }
    
    def _load_contract_abi(self) -> list:
        """Load contract ABI from file"""
        try:
            abi_path = os.path.join(os.path.dirname(__file__), '../contracts/abi.json')
            if os.path.exists(abi_path):
                with open(abi_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading ABI: {e}")
        return []
    
    def check_connection(self) -> Dict[str, Any]:
        """Check Web3 connection"""
        try:
            is_connected = self.w3.is_connected()
            return {
                'success': is_connected,
                'network': self.w3.eth.chain_id if is_connected else None,
                'provider': self.rpc_url
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_balance(self, address: str, token: str = 'ETH') -> Dict[str, Any]:
        """Get token balance for address"""
        try:
            checksum_address = Web3.to_checksum_address(address)
            
            if token == 'ETH':
                balance = self.w3.eth.get_balance(checksum_address)
                return {
                    'success': True,
                    'balance': self.w3.from_wei(balance, 'ether'),
                    'token': 'ETH',
                    'raw_balance': balance
                }
            else:
                # ERC20 token balance
                token_address = self.supported_tokens.get(token)
                if not token_address:
                    return {'success': False, 'error': f'Token {token} not supported'}
                
                # This would require ERC20 ABI
                return {
                    'success': False,
                    'error': 'ERC20 balance check not implemented'
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def subscribe(
        self,
        user_address: str,
        tier: int,
        token: str = 'ETH'
    ) -> Dict[str, Any]:
        """Create subscription transaction"""
        try:
            if not self.contract:
                return {'success': False, 'error': 'Contract not initialized'}
            
            checksum_address = Web3.to_checksum_address(user_address)
            token_address = self.supported_tokens.get(token)
            
            if not token_address:
                return {'success': False, 'error': f'Token {token} not supported'}
            
            # Build transaction
            tx = self.contract.functions.subscribe(
                tier,
                Web3.to_checksum_address(token_address),
                False  # isYearly
            ).build_transaction({
                'from': checksum_address,
                'nonce': self.w3.eth.get_transaction_count(checksum_address),
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            return {
                'success': True,
                'transaction': tx,
                'message': 'Transaction ready to sign'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def upgrade_subscription(
        self,
        user_address: str,
        new_tier: int,
        token: str = 'ETH'
    ) -> Dict[str, Any]:
        """Upgrade subscription tier"""
        try:
            if not self.contract:
                return {'success': False, 'error': 'Contract not initialized'}
            
            checksum_address = Web3.to_checksum_address(user_address)
            token_address = self.supported_tokens.get(token)
            
            if not token_address:
                return {'success': False, 'error': f'Token {token} not supported'}
            
            # Build transaction
            tx = self.contract.functions.upgradeSubscription(
                new_tier,
                Web3.to_checksum_address(token_address)
            ).build_transaction({
                'from': checksum_address,
                'nonce': self.w3.eth.get_transaction_count(checksum_address),
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            return {
                'success': True,
                'transaction': tx,
                'message': 'Upgrade transaction ready to sign'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_subscription(self, user_address: str) -> Dict[str, Any]:
        """Get user subscription details"""
        try:
            if not self.contract:
                return {'success': False, 'error': 'Contract not initialized'}
            
            checksum_address = Web3.to_checksum_address(user_address)
            subscription = self.contract.functions.getSubscription(checksum_address).call()
            
            return {
                'success': True,
                'subscription': {
                    'user': subscription[0],
                    'tier': subscription[1],
                    'startDate': subscription[2],
                    'endDate': subscription[3],
                    'autoRenew': subscription[4],
                    'isActive': subscription[5],
                    'monthlyPrice': self.w3.from_wei(subscription[6], 'ether')
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def is_subscription_valid(self, user_address: str) -> Dict[str, Any]:
        """Check if subscription is valid"""
        try:
            if not self.contract:
                return {'success': False, 'error': 'Contract not initialized'}
            
            checksum_address = Web3.to_checksum_address(user_address)
            is_valid = self.contract.functions.isSubscriptionValid(checksum_address).call()
            
            return {
                'success': True,
                'is_valid': is_valid
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_supported_tokens(self) -> Dict[str, Any]:
        """Get list of supported tokens"""
        return {
            'success': True,
            'tokens': list(self.supported_tokens.keys()),
            'details': self.supported_tokens
        }
    
    def estimate_gas(
        self,
        function_name: str,
        *args
    ) -> Dict[str, Any]:
        """Estimate gas for transaction"""
        try:
            if not self.contract:
                return {'success': False, 'error': 'Contract not initialized'}
            
            func = getattr(self.contract.functions, function_name)
            gas_estimate = func(*args).estimate_gas({'from': self.account_address})
            
            return {
                'success': True,
                'gas_estimate': gas_estimate,
                'gas_price': self.w3.from_wei(self.w3.eth.gas_price, 'gwei'),
                'estimated_cost': self.w3.from_wei(
                    gas_estimate * self.w3.eth.gas_price,
                    'ether'
                )
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def verify_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """Verify transaction status"""
        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            
            if receipt is None:
                return {
                    'success': False,
                    'status': 'pending',
                    'message': 'Transaction still pending'
                }
            
            return {
                'success': receipt['status'] == 1,
                'status': 'success' if receipt['status'] == 1 else 'failed',
                'block_number': receipt['blockNumber'],
                'gas_used': receipt['gasUsed'],
                'transaction_hash': tx_hash
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Singleton instance
blockchain_service = BlockchainService()

