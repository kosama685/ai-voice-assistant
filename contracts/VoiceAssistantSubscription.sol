// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title VoiceAssistantSubscription
 * @dev Smart contract for managing Voice Assistant subscriptions with crypto payments
 * @notice Supports multiple subscription tiers and automatic renewal
 */

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract VoiceAssistantSubscription is Ownable, ReentrancyGuard {
    
    // ============================================================================
    // ENUMS & STRUCTS
    // ============================================================================
    
    enum SubscriptionTier {
        FREE,      // 0
        BASIC,     // 1
        PREMIUM,   // 2
        ENTERPRISE // 3
    }
    
    enum PaymentStatus {
        PENDING,
        COMPLETED,
        FAILED,
        REFUNDED
    }
    
    struct Subscription {
        address user;
        SubscriptionTier tier;
        uint256 startDate;
        uint256 endDate;
        bool autoRenew;
        bool isActive;
        uint256 monthlyPrice;
    }
    
    struct Payment {
        address user;
        uint256 amount;
        address tokenAddress;
        PaymentStatus status;
        uint256 timestamp;
        string transactionHash;
    }
    
    struct TierConfig {
        uint256 monthlyPrice;
        uint256 yearlyPrice;
        uint256 requestLimit;
        uint256 tokenLimit;
        bool isActive;
    }
    
    // ============================================================================
    // STATE VARIABLES
    // ============================================================================
    
    mapping(address => Subscription) public subscriptions;
    mapping(address => Payment[]) public paymentHistory;
    mapping(SubscriptionTier => TierConfig) public tierConfigs;
    mapping(address => bool) public acceptedTokens;
    
    address[] public supportedTokens;
    uint256 public platformFeePercentage = 5; // 5% platform fee
    address public treasuryAddress;
    
    // ============================================================================
    // EVENTS
    // ============================================================================
    
    event SubscriptionCreated(
        address indexed user,
        SubscriptionTier tier,
        uint256 startDate,
        uint256 endDate
    );
    
    event SubscriptionRenewed(
        address indexed user,
        SubscriptionTier tier,
        uint256 newEndDate
    );
    
    event SubscriptionCancelled(address indexed user);
    
    event PaymentProcessed(
        address indexed user,
        uint256 amount,
        address tokenAddress,
        PaymentStatus status
    );
    
    event TierUpgraded(
        address indexed user,
        SubscriptionTier oldTier,
        SubscriptionTier newTier
    );
    
    event TokenAdded(address indexed tokenAddress);
    event TokenRemoved(address indexed tokenAddress);
    
    // ============================================================================
    // MODIFIERS
    // ============================================================================
    
    modifier onlyValidTier(SubscriptionTier _tier) {
        require(_tier != SubscriptionTier.FREE, "Cannot subscribe to FREE tier");
        _;
    }
    
    modifier onlySubscribed(address _user) {
        require(subscriptions[_user].isActive, "User not subscribed");
        _;
    }
    
    modifier onlyValidToken(address _token) {
        require(acceptedTokens[_token], "Token not accepted");
        _;
    }
    
    // ============================================================================
    // CONSTRUCTOR
    // ============================================================================
    
    constructor(address _treasuryAddress) {
        treasuryAddress = _treasuryAddress;
        
        // Initialize tier configurations
        tierConfigs[SubscriptionTier.BASIC] = TierConfig({
            monthlyPrice: 29.99 ether,
            yearlyPrice: 299.99 ether,
            requestLimit: 5000,
            tokenLimit: 500000,
            isActive: true
        });
        
        tierConfigs[SubscriptionTier.PREMIUM] = TierConfig({
            monthlyPrice: 99.99 ether,
            yearlyPrice: 999.99 ether,
            requestLimit: 50000,
            tokenLimit: 5000000,
            isActive: true
        });
        
        tierConfigs[SubscriptionTier.ENTERPRISE] = TierConfig({
            monthlyPrice: 499.99 ether,
            yearlyPrice: 4999.99 ether,
            requestLimit: 999999,
            tokenLimit: 999999999,
            isActive: true
        });
    }
    
    // ============================================================================
    // SUBSCRIPTION MANAGEMENT
    // ============================================================================
    
    /**
     * @dev Subscribe to a tier with ERC20 token
     * @param _tier Subscription tier
     * @param _tokenAddress Token address for payment
     * @param _isYearly Whether to subscribe for yearly
     */
    function subscribe(
        SubscriptionTier _tier,
        address _tokenAddress,
        bool _isYearly
    ) external nonReentrant onlyValidTier(_tier) onlyValidToken(_tokenAddress) {
        require(!subscriptions[msg.sender].isActive, "Already subscribed");
        
        TierConfig memory config = tierConfigs[_tier];
        require(config.isActive, "Tier not available");
        
        uint256 price = _isYearly ? config.yearlyPrice : config.monthlyPrice;
        uint256 duration = _isYearly ? 365 days : 30 days;
        
        // Transfer payment
        IERC20 token = IERC20(_tokenAddress);
        require(
            token.transferFrom(msg.sender, address(this), price),
            "Payment failed"
        );
        
        // Create subscription
        uint256 endDate = block.timestamp + duration;
        subscriptions[msg.sender] = Subscription({
            user: msg.sender,
            tier: _tier,
            startDate: block.timestamp,
            endDate: endDate,
            autoRenew: true,
            isActive: true,
            monthlyPrice: config.monthlyPrice
        });
        
        // Record payment
        recordPayment(msg.sender, price, _tokenAddress, PaymentStatus.COMPLETED);
        
        emit SubscriptionCreated(msg.sender, _tier, block.timestamp, endDate);
    }
    
    /**
     * @dev Renew subscription
     * @param _tokenAddress Token address for payment
     * @param _isYearly Whether to renew for yearly
     */
    function renewSubscription(
        address _tokenAddress,
        bool _isYearly
    ) external nonReentrant onlySubscribed(msg.sender) onlyValidToken(_tokenAddress) {
        Subscription storage sub = subscriptions[msg.sender];
        TierConfig memory config = tierConfigs[sub.tier];
        
        uint256 price = _isYearly ? config.yearlyPrice : config.monthlyPrice;
        uint256 duration = _isYearly ? 365 days : 30 days;
        
        // Transfer payment
        IERC20 token = IERC20(_tokenAddress);
        require(
            token.transferFrom(msg.sender, address(this), price),
            "Payment failed"
        );
        
        // Extend subscription
        sub.endDate = sub.endDate + duration;
        
        // Record payment
        recordPayment(msg.sender, price, _tokenAddress, PaymentStatus.COMPLETED);
        
        emit SubscriptionRenewed(msg.sender, sub.tier, sub.endDate);
    }
    
    /**
     * @dev Upgrade subscription tier
     * @param _newTier New subscription tier
     * @param _tokenAddress Token address for payment
     */
    function upgradeSubscription(
        SubscriptionTier _newTier,
        address _tokenAddress
    ) external nonReentrant onlySubscribed(msg.sender) onlyValidTier(_newTier) onlyValidToken(_tokenAddress) {
        Subscription storage sub = subscriptions[msg.sender];
        require(_newTier > sub.tier, "Can only upgrade to higher tier");
        
        TierConfig memory newConfig = tierConfigs[_newTier];
        require(newConfig.isActive, "Tier not available");
        
        // Calculate prorated price
        uint256 remainingDays = (sub.endDate - block.timestamp) / 1 days;
        uint256 proratedPrice = (newConfig.monthlyPrice * remainingDays) / 30;
        
        // Transfer payment
        IERC20 token = IERC20(_tokenAddress);
        require(
            token.transferFrom(msg.sender, address(this), proratedPrice),
            "Payment failed"
        );
        
        // Update subscription
        SubscriptionTier oldTier = sub.tier;
        sub.tier = _newTier;
        sub.monthlyPrice = newConfig.monthlyPrice;
        
        // Record payment
        recordPayment(msg.sender, proratedPrice, _tokenAddress, PaymentStatus.COMPLETED);
        
        emit TierUpgraded(msg.sender, oldTier, _newTier);
    }
    
    /**
     * @dev Cancel subscription
     */
    function cancelSubscription() external onlySubscribed(msg.sender) {
        subscriptions[msg.sender].isActive = false;
        emit SubscriptionCancelled(msg.sender);
    }
    
    // ============================================================================
    // ADMIN FUNCTIONS
    // ============================================================================
    
    /**
     * @dev Add accepted token
     * @param _tokenAddress Token address
     */
    function addAcceptedToken(address _tokenAddress) external onlyOwner {
        require(!acceptedTokens[_tokenAddress], "Token already accepted");
        acceptedTokens[_tokenAddress] = true;
        supportedTokens.push(_tokenAddress);
        emit TokenAdded(_tokenAddress);
    }
    
    /**
     * @dev Remove accepted token
     * @param _tokenAddress Token address
     */
    function removeAcceptedToken(address _tokenAddress) external onlyOwner {
        require(acceptedTokens[_tokenAddress], "Token not accepted");
        acceptedTokens[_tokenAddress] = false;
        emit TokenRemoved(_tokenAddress);
    }
    
    /**
     * @dev Update tier configuration
     * @param _tier Subscription tier
     * @param _monthlyPrice Monthly price
     * @param _yearlyPrice Yearly price
     * @param _requestLimit Request limit
     * @param _tokenLimit Token limit
     */
    function updateTierConfig(
        SubscriptionTier _tier,
        uint256 _monthlyPrice,
        uint256 _yearlyPrice,
        uint256 _requestLimit,
        uint256 _tokenLimit
    ) external onlyOwner {
        tierConfigs[_tier] = TierConfig({
            monthlyPrice: _monthlyPrice,
            yearlyPrice: _yearlyPrice,
            requestLimit: _requestLimit,
            tokenLimit: _tokenLimit,
            isActive: true
        });
    }
    
    /**
     * @dev Withdraw collected fees
     * @param _tokenAddress Token address
     */
    function withdrawFees(address _tokenAddress) external onlyOwner {
        IERC20 token = IERC20(_tokenAddress);
        uint256 balance = token.balanceOf(address(this));
        require(balance > 0, "No balance to withdraw");
        require(token.transfer(treasuryAddress, balance), "Withdrawal failed");
    }
    
    // ============================================================================
    // VIEW FUNCTIONS
    // ============================================================================
    
    /**
     * @dev Get user subscription
     * @param _user User address
     */
    function getSubscription(address _user) external view returns (Subscription memory) {
        return subscriptions[_user];
    }
    
    /**
     * @dev Check if subscription is valid
     * @param _user User address
     */
    function isSubscriptionValid(address _user) external view returns (bool) {
        Subscription memory sub = subscriptions[_user];
        return sub.isActive && sub.endDate > block.timestamp;
    }
    
    /**
     * @dev Get payment history
     * @param _user User address
     */
    function getPaymentHistory(address _user) external view returns (Payment[] memory) {
        return paymentHistory[_user];
    }
    
    /**
     * @dev Get supported tokens
     */
    function getSupportedTokens() external view returns (address[] memory) {
        return supportedTokens;
    }
    
    // ============================================================================
    // INTERNAL FUNCTIONS
    // ============================================================================
    
    /**
     * @dev Record payment
     */
    function recordPayment(
        address _user,
        uint256 _amount,
        address _tokenAddress,
        PaymentStatus _status
    ) internal {
        paymentHistory[_user].push(Payment({
            user: _user,
            amount: _amount,
            tokenAddress: _tokenAddress,
            status: _status,
            timestamp: block.timestamp,
            transactionHash: ""
        }));
        
        emit PaymentProcessed(_user, _amount, _tokenAddress, _status);
    }
}

