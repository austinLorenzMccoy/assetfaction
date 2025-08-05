// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../src/SimpleAssetRegistry.sol";

/**
 * @title SimpleDeploy
 * @dev Simple deployment script for AssetFraction contracts
 */
contract SimpleDeploy is Script {
    SimpleAssetRegistry public registry;

    function run() public {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        
        vm.startBroadcast(deployerPrivateKey);
        
        console.log("Deploying SimpleAssetRegistry...");
        registry = new SimpleAssetRegistry();
        console.log("SimpleAssetRegistry deployed at:", address(registry));
        
        vm.stopBroadcast();
        
        console.log("Deployment completed successfully!");
    }
}
