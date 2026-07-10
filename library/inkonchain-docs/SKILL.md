---
name: ink-chain-integration
description: Guides Claude through building, deploying, and integrating smart contracts and dApps on Ink, an OP Stack Ethereum Layer 2 blockchain; use when a user is configuring network connections, deploying contracts, bridging assets, or troubleshooting integration issues on Ink.
---

# Ink Chain Integration

Ink is an OP Stack-based Ethereum Layer 2 blockchain, built to be EVM-equivalent and interoperable with the broader Optimism Superchain ecosystem. This skill helps with configuring, deploying to, and integrating with Ink, treating it as a standard OP Stack chain with its own network parameters.

## When to apply this skill

Apply this skill when the user is:
- Setting up wallet or RPC configuration to connect to Ink mainnet or testnet
- Deploying smart contracts to Ink using Foundry, Hardhat, or similar EVM tooling
- Bridging assets (ETH or ERC-20 tokens) to or from Ink
- Debugging a failed transaction, deployment, or integration on Ink
- Writing dApp frontend code that needs to target Ink as a chain option
- Comparing Ink's behavior against mainnet Ethereum or other OP Stack chains (Optimism, Base) to understand what carries over and what doesn't

## Core facts to work from

- Ink is built on the OP Stack, so it inherits OP Stack conventions: an Ethereum-equivalent EVM, a Sequencer + rollup architecture, a canonical bridge to its L1 settlement layer, and standard OP Stack RPC methods alongside the normal Ethereum JSON-RPC surface.
- Because it is OP Stack-based, most Ethereum tooling (Foundry, Hardhat, ethers.js, viem, wagmi, MetaMask) works against Ink with only network configuration (RPC URL, chain ID, block explorer URL) changed — no Ink-specific SDK is required for standard contract deployment or interaction.
- Network parameters (chain ID, RPC endpoints, bridge contract addresses, block explorer URL) are chain-specific and change over time as networks add endpoints or move between testnet/mainnet. **Do not hardcode or assume these values from memory** — always get them from the user, from a config file already in their project, or from an official source they provide. If none of these are available, tell the user you need the current chain ID and RPC URL rather than guessing.
- Treat Ink like other OP Stack L2s for gas mechanics: transactions pay both an L2 execution fee and an L1 data-availability fee, which fluctuates with L1 gas prices. If a user's gas estimate or cost calculation is off, check whether their tooling is accounting for the L1 fee component.

## Step-by-step guidance

1. **Confirm network context first.** Before writing any deployment script, RPC config, or wallet-add code, ask the user (or check their existing `.env`, `hardhat.config.js`, `foundry.toml`, or `wagmi.config.ts`) for the target network's chain ID and RPC URL. Don't proceed on an assumed value.

2. **Reuse existing OP Stack tooling patterns.** If the user's project already deploys to Optimism or Base, mirror that same Foundry/Hardhat network block or `viem`/`wagmi` chain definition for Ink — just swap in Ink's chain ID, RPC URL, and explorer URL. Don't introduce new deployment tooling just because the target is Ink.

3. **For contract deployment:**
   - Use the project's existing deployment framework (Foundry `forge script`, Hardhat deploy scripts, etc.) pointed at Ink's RPC endpoint.
   - Remind the user to fund the deployer address with ETH on Ink (bridged from L1 or from a faucet if using testnet) before deploying.
   - After deployment, verify the contract on Ink's block explorer if the user's workflow includes contract verification for other chains.

4. **For bridging:** explain that assets move to/from Ink via the canonical OP Stack bridge (deposit from L1, withdraw from L2 with the standard OP Stack challenge/finalization window for withdrawals). If the user needs exact bridge contract addresses, get them from the user or an official source rather than fabricating them.

5. **For frontend/dApp integration:** add Ink as a chain entry in the wallet/chain config (e.g., `wagmi` chains array, MetaMask `wallet_addEthereumChain` payload) using the chain ID and RPC URL confirmed in step 1, following the same shape as the app's existing chain entries.

6. **When debugging failures:** check the usual OP Stack L2 failure modes first — wrong chain ID in the request, insufficient L2 ETH for gas (including the L1 data fee component), RPC endpoint mismatch (testnet vs. mainnet), or a withdrawal still inside its challenge window before finalization on L1.

7. **When in doubt about an Ink-specific detail** (exact chain ID, specific precompile availability, official contract addresses), say so explicitly and ask the user to confirm or provide a source, rather than presenting a guessed value as fact.
