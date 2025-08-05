// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "./utils/Counter.sol";

/**
 * @title SimpleAssetRegistry
 * @dev Simplified asset registry for fractional ownership
 * @author AssetFraction Team
 */
contract SimpleAssetRegistry is Ownable, ReentrancyGuard {
    using Counter for Counter.CounterData;

    // Asset counter for unique IDs
    Counter.CounterData private _assetIdCounter;

    // Asset status enumeration
    enum AssetStatus {
        Pending,
        Verified,
        Suspended
    }

    // Asset structure
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
    }

    // Events
    event AssetRegistered(uint256 indexed assetId, address indexed owner, string name);
    event AssetVerified(uint256 indexed assetId, address indexed verifier);
    event TokensPurchased(uint256 indexed assetId, address indexed buyer, uint256 amount);

    // Mappings
    mapping(uint256 => Asset) public assets;
    mapping(address => bool) public authorizedVerifiers;
    mapping(uint256 => mapping(address => uint256)) public tokenHoldings;

    // Constants
    uint256 public constant MIN_ASSET_VALUE = 10000 * 1e18;
    uint256 public constant VERIFICATION_FEE = 0.1 ether;

    constructor() Ownable(msg.sender) {
        authorizedVerifiers[msg.sender] = true;
    }

    /**
     * @dev Register a new asset
     */
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
            createdAt: block.timestamp
        });

        emit AssetRegistered(assetId, msg.sender, name);
        return assetId;
    }

    /**
     * @dev Verify an asset
     */
    function verifyAsset(uint256 assetId) external payable {
        require(authorizedVerifiers[msg.sender], "Not authorized verifier");
        require(msg.value >= VERIFICATION_FEE, "Insufficient verification fee");
        require(assets[assetId].id != 0, "Asset does not exist");
        require(assets[assetId].status == AssetStatus.Pending, "Asset not pending");

        assets[assetId].status = AssetStatus.Verified;
        
        // Transfer verification fee to contract owner
        (bool success, ) = payable(owner()).call{value: VERIFICATION_FEE}("");
        require(success, "Verification fee transfer failed");
        
        // Refund excess payment
        if (msg.value > VERIFICATION_FEE) {
            (bool refundSuccess, ) = payable(msg.sender).call{value: msg.value - VERIFICATION_FEE}("");
            require(refundSuccess, "Verification refund failed");
        }
        
        emit AssetVerified(assetId, msg.sender);
    }

    /**
     * @dev Purchase fractional tokens
     */
    function purchaseTokens(uint256 assetId, uint256 tokenAmount) external payable nonReentrant {
        Asset storage asset = assets[assetId];
        require(asset.id != 0, "Asset does not exist");
        require(asset.status == AssetStatus.Verified, "Asset not verified");
        require(tokenAmount > 0, "Token amount must be positive");
        require(tokenAmount <= asset.tokensAvailable, "Insufficient tokens available");

        uint256 tokenPrice = asset.totalValue / asset.totalTokens;
        uint256 totalCost = tokenPrice * tokenAmount;
        require(msg.value >= totalCost, "Insufficient payment");

        tokenHoldings[assetId][msg.sender] += tokenAmount;
        asset.tokensAvailable -= tokenAmount;

        // Transfer payment to asset owner
        (bool success, ) = payable(asset.owner).call{value: totalCost}("");
        require(success, "Transfer to asset owner failed");

        // Refund excess payment
        if (msg.value > totalCost) {
            (bool refundSuccess, ) = payable(msg.sender).call{value: msg.value - totalCost}("");
            require(refundSuccess, "Refund failed");
        }

        emit TokensPurchased(assetId, msg.sender, tokenAmount);
    }

    /**
     * @dev Add authorized verifier
     */
    function addVerifier(address verifier) external onlyOwner {
        require(verifier != address(0), "Invalid verifier address");
        authorizedVerifiers[verifier] = true;
    }

    /**
     * @dev Remove authorized verifier
     */
    function removeVerifier(address verifier) external onlyOwner {
        authorizedVerifiers[verifier] = false;
    }

    /**
     * @dev Get asset details
     */
    function getAsset(uint256 assetId) external view returns (Asset memory) {
        return assets[assetId];
    }

    /**
     * @dev Get token holdings
     */
    function getTokenHoldings(uint256 assetId, address investor) external view returns (uint256) {
        return tokenHoldings[assetId][investor];
    }

    /**
     * @dev Get current asset count
     */
    function getAssetCount() external view returns (uint256) {
        return _assetIdCounter.current();
    }

    /**
     * @dev Withdraw contract balance
     */
    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
