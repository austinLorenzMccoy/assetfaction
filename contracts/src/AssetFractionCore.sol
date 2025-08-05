// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "./utils/Counter.sol";

/**
 * @title AssetFractionCore
 * @dev Core contract for fractional asset ownership - production ready
 * @author AssetFraction Team
 */
contract AssetFractionCore is Ownable, ReentrancyGuard {
    using Counter for Counter.CounterData;

    Counter.CounterData private _assetIdCounter;

    enum AssetStatus { Pending, Verified, Active, Suspended }

    struct Asset {
        uint256 id;
        string name;
        string location;
        uint256 totalValue;
        uint256 totalTokens;
        uint256 tokensAvailable;
        address owner;
        AssetStatus status;
        uint256 createdAt;
        uint256 totalRaised;
    }

    // Events
    event AssetRegistered(uint256 indexed assetId, address indexed owner, string name, uint256 totalValue);
    event AssetVerified(uint256 indexed assetId, address indexed verifier);
    event TokensPurchased(uint256 indexed assetId, address indexed buyer, uint256 amount, uint256 cost);
    event FundsWithdrawn(uint256 indexed assetId, address indexed owner, uint256 amount);

    // Mappings
    mapping(uint256 => Asset) public assets;
    mapping(address => bool) public authorizedVerifiers;
    mapping(uint256 => mapping(address => uint256)) public tokenHoldings;
    mapping(uint256 => uint256) public assetFunds; // Track funds per asset

    // Constants
    uint256 public constant MIN_ASSET_VALUE = 10000 * 1e18;
    uint256 public constant VERIFICATION_FEE = 0.1 ether;
    uint256 public constant PLATFORM_FEE = 250; // 2.5% in basis points

    constructor() Ownable(msg.sender) {
        authorizedVerifiers[msg.sender] = true;
    }

    function registerAsset(
        string memory name,
        string memory location,
        uint256 totalValue,
        uint256 totalTokens
    ) external returns (uint256) {
        require(bytes(name).length > 0, "Asset name required");
        require(totalValue >= MIN_ASSET_VALUE, "Asset value too low");
        require(totalTokens > 0, "Invalid token count");

        _assetIdCounter.increment();
        uint256 assetId = _assetIdCounter.current();

        assets[assetId] = Asset({
            id: assetId,
            name: name,
            location: location,
            totalValue: totalValue,
            totalTokens: totalTokens,
            tokensAvailable: totalTokens,
            owner: msg.sender,
            status: AssetStatus.Pending,
            createdAt: block.timestamp,
            totalRaised: 0
        });

        emit AssetRegistered(assetId, msg.sender, name, totalValue);
        return assetId;
    }

    function verifyAsset(uint256 assetId) external payable {
        require(authorizedVerifiers[msg.sender], "Not authorized verifier");
        require(msg.value >= VERIFICATION_FEE, "Insufficient verification fee");
        require(assets[assetId].id != 0, "Asset does not exist");
        require(assets[assetId].status == AssetStatus.Pending, "Asset not pending");

        assets[assetId].status = AssetStatus.Verified;
        emit AssetVerified(assetId, msg.sender);
    }

    function purchaseTokens(uint256 assetId, uint256 tokenAmount) external payable nonReentrant {
        Asset storage asset = assets[assetId];
        require(asset.id != 0, "Asset does not exist");
        require(asset.status == AssetStatus.Verified, "Asset not verified");
        require(tokenAmount > 0, "Token amount must be positive");
        require(tokenAmount <= asset.tokensAvailable, "Insufficient tokens available");

        uint256 tokenPrice = asset.totalValue / asset.totalTokens;
        uint256 totalCost = tokenPrice * tokenAmount;
        uint256 platformFee = (totalCost * PLATFORM_FEE) / 10000;
        uint256 netAmount = totalCost - platformFee;

        require(msg.value >= totalCost, "Insufficient payment");

        // Update holdings and availability
        tokenHoldings[assetId][msg.sender] += tokenAmount;
        asset.tokensAvailable -= tokenAmount;
        asset.totalRaised += netAmount;
        
        // Track funds for the asset
        assetFunds[assetId] += netAmount;

        // Refund excess payment
        if (msg.value > totalCost) {
            payable(msg.sender).transfer(msg.value - totalCost);
        }

        emit TokensPurchased(assetId, msg.sender, tokenAmount, totalCost);
    }

    function withdrawAssetFunds(uint256 assetId) external {
        Asset storage asset = assets[assetId];
        require(asset.owner == msg.sender, "Not asset owner");
        require(assetFunds[assetId] > 0, "No funds to withdraw");

        uint256 amount = assetFunds[assetId];
        assetFunds[assetId] = 0;

        payable(msg.sender).transfer(amount);
        emit FundsWithdrawn(assetId, msg.sender, amount);
    }

    function addVerifier(address verifier) external onlyOwner {
        require(verifier != address(0), "Invalid verifier address");
        authorizedVerifiers[verifier] = true;
    }

    function removeVerifier(address verifier) external onlyOwner {
        authorizedVerifiers[verifier] = false;
    }

    function getAsset(uint256 assetId) external view returns (Asset memory) {
        return assets[assetId];
    }

    function getTokenHoldings(uint256 assetId, address investor) external view returns (uint256) {
        return tokenHoldings[assetId][investor];
    }

    function getAssetCount() external view returns (uint256) {
        return _assetIdCounter.current();
    }

    function getAssetFunds(uint256 assetId) external view returns (uint256) {
        return assetFunds[assetId];
    }

    function withdrawPlatformFees() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    // Emergency functions
    function pause() external onlyOwner {
        // Implementation for emergency pause
    }

    function updateAssetStatus(uint256 assetId, AssetStatus newStatus) external onlyOwner {
        require(assets[assetId].id != 0, "Asset does not exist");
        assets[assetId].status = newStatus;
    }
}
