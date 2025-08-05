// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/AssetFractionCore.sol";

contract AssetFractionCoreTest is Test {
    AssetFractionCore public core;
    
    address public owner = address(0x999);
    address public assetOwner = address(0x1);
    address public verifier = address(0x2);
    address public investor1 = address(0x3);
    address public investor2 = address(0x4);
    
    // Test asset parameters
    string constant ASSET_NAME = "Lagos Premium Apartments";
    string constant ASSET_LOCATION = "Victoria Island, Lagos";
    uint256 constant ASSET_VALUE = 250000 * 1e18;
    uint256 constant TOTAL_TOKENS = 10000;
    
    event AssetRegistered(uint256 indexed assetId, address indexed owner, string name, uint256 totalValue);
    event AssetVerified(uint256 indexed assetId, address indexed verifier);
    event TokensPurchased(uint256 indexed assetId, address indexed buyer, uint256 amount, uint256 cost);
    
    function setUp() public {
        vm.prank(owner);
        core = new AssetFractionCore();
        
        vm.prank(owner);
        core.addVerifier(verifier);
        
        // Fund test accounts
        vm.deal(owner, 100 ether);
        vm.deal(assetOwner, 100 ether);
        vm.deal(investor1, 100 ether);
        vm.deal(investor2, 100 ether);
        vm.deal(verifier, 100 ether);
    }

    function testRegisterAsset() public {
        vm.startPrank(assetOwner);
        
        vm.expectEmit(true, true, false, true);
        emit AssetRegistered(1, assetOwner, ASSET_NAME, ASSET_VALUE);
        
        uint256 assetId = core.registerAsset(
            ASSET_NAME,
            ASSET_LOCATION,
            ASSET_VALUE,
            TOTAL_TOKENS
        );
        
        assertEq(assetId, 1);
        
        AssetFractionCore.Asset memory asset = core.getAsset(assetId);
        assertEq(asset.id, assetId);
        assertEq(asset.name, ASSET_NAME);
        assertEq(asset.totalValue, ASSET_VALUE);
        assertEq(asset.totalTokens, TOTAL_TOKENS);
        assertEq(asset.tokensAvailable, TOTAL_TOKENS);
        assertEq(asset.owner, assetOwner);
        assertTrue(uint8(asset.status) == uint8(AssetFractionCore.AssetStatus.Pending));
        
        vm.stopPrank();
    }

    function testVerifyAsset() public {
        vm.prank(assetOwner);
        uint256 assetId = core.registerAsset(ASSET_NAME, ASSET_LOCATION, ASSET_VALUE, TOTAL_TOKENS);
        
        vm.startPrank(verifier);
        
        vm.expectEmit(true, true, false, false);
        emit AssetVerified(assetId, verifier);
        
        core.verifyAsset{value: 0.1 ether}(assetId);
        
        AssetFractionCore.Asset memory asset = core.getAsset(assetId);
        assertTrue(uint8(asset.status) == uint8(AssetFractionCore.AssetStatus.Verified));
        
        vm.stopPrank();
    }

    function testPurchaseTokens() public {
        // Register and verify asset
        vm.prank(assetOwner);
        uint256 assetId = core.registerAsset(ASSET_NAME, ASSET_LOCATION, ASSET_VALUE, TOTAL_TOKENS);
        
        vm.prank(verifier);
        core.verifyAsset{value: 0.1 ether}(assetId);
        
        // Purchase tokens
        uint256 tokensToBuy = 100;
        uint256 tokenPrice = ASSET_VALUE / TOTAL_TOKENS;
        uint256 totalCost = tokenPrice * tokensToBuy;
        
        vm.startPrank(investor1);
        
        vm.expectEmit(true, true, false, true);
        emit TokensPurchased(assetId, investor1, tokensToBuy, totalCost);
        
        core.purchaseTokens{value: totalCost}(assetId, tokensToBuy);
        
        // Check token holdings
        uint256 holdings = core.getTokenHoldings(assetId, investor1);
        assertEq(holdings, tokensToBuy);
        
        // Check asset tokens available
        AssetFractionCore.Asset memory asset = core.getAsset(assetId);
        assertEq(asset.tokensAvailable, TOTAL_TOKENS - tokensToBuy);
        
        // Check funds are tracked
        uint256 platformFee = (totalCost * 250) / 10000; // 2.5%
        uint256 expectedFunds = totalCost - platformFee;
        assertEq(core.getAssetFunds(assetId), expectedFunds);
        
        vm.stopPrank();
    }

    function testMultipleInvestors() public {
        // Register and verify asset
        vm.prank(assetOwner);
        uint256 assetId = core.registerAsset(ASSET_NAME, ASSET_LOCATION, ASSET_VALUE, TOTAL_TOKENS);
        
        vm.prank(verifier);
        core.verifyAsset{value: 0.1 ether}(assetId);
        
        uint256 tokenPrice = ASSET_VALUE / TOTAL_TOKENS;
        
        // Investor 1 purchases 300 tokens
        vm.prank(investor1);
        core.purchaseTokens{value: tokenPrice * 300}(assetId, 300);
        
        // Investor 2 purchases 200 tokens
        vm.prank(investor2);
        core.purchaseTokens{value: tokenPrice * 200}(assetId, 200);
        
        // Check holdings
        assertEq(core.getTokenHoldings(assetId, investor1), 300);
        assertEq(core.getTokenHoldings(assetId, investor2), 200);
        
        // Check remaining tokens
        AssetFractionCore.Asset memory asset = core.getAsset(assetId);
        assertEq(asset.tokensAvailable, TOTAL_TOKENS - 500);
    }

    function testWithdrawAssetFunds() public {
        // Register and verify asset
        vm.prank(assetOwner);
        uint256 assetId = core.registerAsset(ASSET_NAME, ASSET_LOCATION, ASSET_VALUE, TOTAL_TOKENS);
        
        vm.prank(verifier);
        core.verifyAsset{value: 0.1 ether}(assetId);
        
        // Purchase tokens
        uint256 tokensToBuy = 100;
        uint256 tokenPrice = ASSET_VALUE / TOTAL_TOKENS;
        uint256 totalCost = tokenPrice * tokensToBuy;
        
        vm.prank(investor1);
        core.purchaseTokens{value: totalCost}(assetId, tokensToBuy);
        
        // Check funds before withdrawal
        uint256 platformFee = (totalCost * 250) / 10000;
        uint256 expectedFunds = totalCost - platformFee;
        assertEq(core.getAssetFunds(assetId), expectedFunds);
        
        // Asset owner withdraws funds
        uint256 initialBalance = assetOwner.balance;
        
        vm.prank(assetOwner);
        core.withdrawAssetFunds(assetId);
        
        // Check funds were transferred
        assertEq(assetOwner.balance, initialBalance + expectedFunds);
        assertEq(core.getAssetFunds(assetId), 0);
    }

    function testRevertConditions() public {
        // Test registration failures
        vm.startPrank(assetOwner);
        
        // Empty name
        vm.expectRevert("Asset name required");
        core.registerAsset("", ASSET_LOCATION, ASSET_VALUE, TOTAL_TOKENS);
        
        // Low asset value
        vm.expectRevert("Asset value too low");
        core.registerAsset(ASSET_NAME, ASSET_LOCATION, 5000 * 1e18, TOTAL_TOKENS);
        
        // Invalid token count
        vm.expectRevert("Invalid token count");
        core.registerAsset(ASSET_NAME, ASSET_LOCATION, ASSET_VALUE, 0);
        
        vm.stopPrank();
        
        // Test verification failures
        uint256 assetId = core.registerAsset(ASSET_NAME, ASSET_LOCATION, ASSET_VALUE, TOTAL_TOKENS);
        
        // Unauthorized verifier
        vm.startPrank(investor1);
        vm.expectRevert("Not authorized verifier");
        core.verifyAsset{value: 0.1 ether}(assetId);
        vm.stopPrank();
        
        // Insufficient verification fee
        vm.startPrank(verifier);
        vm.expectRevert("Insufficient verification fee");
        core.verifyAsset{value: 0.05 ether}(assetId);
        vm.stopPrank();
    }

    function testPurchaseRevertConditions() public {
        vm.prank(assetOwner);
        uint256 assetId = core.registerAsset(ASSET_NAME, ASSET_LOCATION, ASSET_VALUE, TOTAL_TOKENS);
        
        // Purchase without verification
        vm.startPrank(investor1);
        vm.expectRevert("Asset not verified");
        core.purchaseTokens{value: 1 ether}(assetId, 100);
        vm.stopPrank();
        
        // Verify asset
        vm.prank(verifier);
        core.verifyAsset{value: 0.1 ether}(assetId);
        
        vm.startPrank(investor1);
        
        // Zero tokens
        vm.expectRevert("Token amount must be positive");
        core.purchaseTokens{value: 1 ether}(assetId, 0);
        
        // Too many tokens
        vm.expectRevert("Insufficient tokens available");
        core.purchaseTokens{value: 1 ether}(assetId, TOTAL_TOKENS + 1);
        
        // Insufficient payment
        uint256 tokenPrice = ASSET_VALUE / TOTAL_TOKENS;
        vm.expectRevert("Insufficient payment");
        core.purchaseTokens{value: tokenPrice - 1}(assetId, 1);
        
        vm.stopPrank();
    }

    function testAddRemoveVerifier() public {
        address newVerifier = address(0x5);
        
        vm.startPrank(owner);
        
        // Add verifier
        core.addVerifier(newVerifier);
        assertTrue(core.authorizedVerifiers(newVerifier));
        
        // Remove verifier
        core.removeVerifier(newVerifier);
        assertFalse(core.authorizedVerifiers(newVerifier));
        
        vm.stopPrank();
    }

    function testGetAssetCount() public {
        assertEq(core.getAssetCount(), 0);
        
        vm.prank(assetOwner);
        core.registerAsset(ASSET_NAME, ASSET_LOCATION, ASSET_VALUE, TOTAL_TOKENS);
        
        assertEq(core.getAssetCount(), 1);
        
        vm.prank(assetOwner);
        core.registerAsset("Another Asset", "Another Location", ASSET_VALUE, TOTAL_TOKENS);
        
        assertEq(core.getAssetCount(), 2);
    }

    function testPlatformFeeCalculation() public {
        vm.prank(assetOwner);
        uint256 assetId = core.registerAsset(ASSET_NAME, ASSET_LOCATION, ASSET_VALUE, TOTAL_TOKENS);
        
        vm.prank(verifier);
        core.verifyAsset{value: 0.1 ether}(assetId);
        
        uint256 tokensToBuy = 1000; // 10% of tokens
        uint256 tokenPrice = ASSET_VALUE / TOTAL_TOKENS;
        uint256 totalCost = tokenPrice * tokensToBuy;
        uint256 expectedPlatformFee = (totalCost * 250) / 10000; // 2.5%
        uint256 expectedAssetFunds = totalCost - expectedPlatformFee;
        
        uint256 contractBalanceBefore = address(core).balance;
        
        vm.prank(investor1);
        core.purchaseTokens{value: totalCost}(assetId, tokensToBuy);
        
        // Check platform fee is retained in contract
        uint256 contractBalanceAfter = address(core).balance;
        assertEq(contractBalanceAfter - contractBalanceBefore, expectedPlatformFee);
        
        // Check asset funds are correct
        assertEq(core.getAssetFunds(assetId), expectedAssetFunds);
    }
}
