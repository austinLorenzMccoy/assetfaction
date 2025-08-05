// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title Counter
 * @dev Simple counter utility to replace OpenZeppelin's deprecated Counters
 */
library Counter {
    struct CounterData {
        uint256 _value; // default: 0
    }

    function current(CounterData storage counter) internal view returns (uint256) {
        return counter._value;
    }

    function increment(CounterData storage counter) internal {
        unchecked {
            counter._value += 1;
        }
    }

    function decrement(CounterData storage counter) internal {
        uint256 value = counter._value;
        require(value > 0, "Counter: decrement overflow");
        unchecked {
            counter._value = value - 1;
        }
    }

    function reset(CounterData storage counter) internal {
        counter._value = 0;
    }
}
