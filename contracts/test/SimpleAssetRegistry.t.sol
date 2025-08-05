// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/SimpleAssetRegistry.sol";

contract SimpleAssetRegistryTest is Test {
    SimpleAssetRegistry public registry;
    
    address public owner = address(0x999);
    address public assetOwner = address(0x1);
    address public verifier = address(0x2);
    address public investor = address(0x3);
    
    // Test asset parameters
    string constant ASSET_NAME = "Lagos Premium Apartments";
    string constant ASSET_LOCATION = "Victoria Island, Lagos";
    uint256 constant ASSET_VALUE = 250000 * 1e18;
    uint256 constant TOTAL_TOKENS = 10000;
    
    function setUp() public {
        vm.prank(owner);
        registry = new SimpleAssetRegistry();
        
        vm.prank(owner);
        registry.addVerifier(verifier);
        
        // Fund test accounts
        vm.deal(owner, 100 ether);
        vm.deal(assetOwner, 100 ether);
        vm.deal(investor, 100 ether);
        vm.deal(verifier, 100 ether);
    }

    function testRegisterAsset() public {
        vm.startPrank(assetOwner);
        
        uint256 assetId = registry.registerAsset(
            ASSET_NAME,
            ASSET_LOCATION,
            ASSET_VALUE,
            TOTAL_TOKENS
        );
        
        assertEq(assetId, 1);
        
        SimpleAssetRegistry.Asset memory asset = registry.getAsset(assetId);
        assertEq(asset.id, assetId);
        assertEq(asset.name, ASSET_NAME);
        assertEq(asset.totalValue, ASSET_VALUE);
        assertEq(asset.totalTokens, TOTAL_TOKENS);
        assertEq(asset.owner, assetOwner);
        
        vm.stopPrank();
    }

    function testVerifyAsset() public {
        vm.prank(assetOwner);
        uint256 assetId = registry.registerAsset(ASSET_NAME, ASSET_LOCATION, ASSET_VALUE, TOTAL_TOKENS);
        
        vm.prank(verifier);
        registry.verifyAsset{value: 0.1 ether}(assetId);
        
        SimpleAssetRegistry.Asset memory asset = registry.getAsset(assetId);
        assertTrue(uint8(asset.status) == uint8(SimpleAssetRegistry.AssetStatus.Verified));
    }

    function testPurchaseTokens() public {
        vm.prank(assetOwner);
        uint256 assetId = registry.registerAsset(ASSET_NAME, ASSET_LOCATION, ASSET_VALUE, TOTAL_TOKENS);
        
        vm.prank(verifier);
        registry.verifyAsset{value: 0.1 ether}(assetId);
        
        uint256 tokensToBuy = 100;
        uint256 tokenPrice = ASSET_VALUE / TOTAL_TOKENS;
        uint256 totalCost = tokenPrice * tokensToBuy;
        
        vm.prank(investor);
        registry.purchaseTokens{value: totalCost}(assetId, tokensToBuy);
        
        uint256 holdings = registry.getTokenHoldings(assetId, investor);
        assertEq(holdings, tokensToBuy);
    }

    function testGetAssetCount() public {
        assertEq(registry.getAssetCount(), 0);
        
        vm.prank(assetOwner);
        registry.registerAsset(ASSET_NAME, ASSET_LOCATION, ASSET_VALUE, TOTAL_TOKENS);
        
        assertEq(registry.getAssetCount(), 1);
    }
}
