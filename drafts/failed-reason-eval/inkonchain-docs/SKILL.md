---
name: ink-l2-development
description: Guides Claude through developing, deploying, and integrating smart contracts and dApps on the Ink Layer 2 blockchain (an OP Stack-based Ethereum L2), including network configuration, bridging, and common tooling setup.
---

# Ink L2 Development

This skill helps with building, deploying, and troubleshooting smart contracts and dApps on Ink, an Ethereum Layer 2 network built on the OP Stack (Optimism's rollup framework). Apply this skill whenever a user asks about deploying contracts to Ink, configuring RPC endpoints or wallets for Ink, bridging assets to/from Ink, or debugging Ink-specific network behavior.

## When to apply this skill

- The user mentions "Ink chain," "Ink L2," "Ink mainnet/testnet," or asks to deploy/interact with contracts on a chain built on the OP Stack that isn't Optimism itself.
- The user is configuring `hardhat.config.js`, `foundry.toml`, `wagmi`/`viem` chain definitions, or MetaMask network settings and mentions Ink.
- The user needs to bridge ETH or tokens between Ethereum mainnet (or another L2) and Ink.
- The user hits errors related to gas estimation, block explorer verification, or RPC connectivity specifically on Ink.

## Core facts to work from

- Ink is an OP Stack rollup, so it inherits Optimism's architecture: an L1 (Ethereum) settlement layer, a sequencer, and a standard OP Stack bridge contract set. Any general OP Stack / Optimism knowledge (fault proofs, deposit/withdrawal flow, gas fee mechanics, `op-node`/`op-geth` behavior) applies to Ink unless the user's docs say otherwise.
- Ink has both a mainnet and a Sepolia-based testnet. When helping a user configure tooling, always ask (or infer from context) which environment they mean — chain IDs, RPC URLs, and explorer URLs differ between them and should never be guessed or hard-coded from memory. If the user hasn't provided the specific chain ID/RPC/explorer values, ask them to paste the values from their own config or the network's current documentation rather than fabricating them.
- Because Ink is EVM-equivalent (OP Stack chains preserve EVM semantics), standard Ethereum tooling works unmodified: Hardhat, Foundry, viem, ethers.js, wagmi, Safe, and standard ERC-20/721/1155 contracts all function without special adaptation — the only differences are network parameters (chain ID, RPC endpoint, block explorer) and any Ink-specific bridge or precompile addresses.
- Bridging follows the standard OP Stack pattern: deposits from L1 to Ink are near-instant (finalized after L1 confirmation), while withdrawals from Ink back to L1 require the OP Stack challenge/proving period before funds are available on L1. Warn users about this asymmetry whenever they ask about withdrawal timing.

## Step-by-step guidance

1. **Clarify the environment first.** Before writing any config or code, confirm whether the user is targeting Ink mainnet or the Ink testnet, and ask for (or use user-supplied) chain ID, RPC URL, and block explorer URL — do not invent these values.
2. **Reuse standard OP Stack/EVM patterns.** Treat Ink like any other OP Stack L2 for contract deployment, gas estimation, and verification — adapt existing Optimism/Base-style Hardhat or Foundry configs by swapping in Ink's network parameters rather than writing new deployment logic from scratch.
3. **Surface bridge-specific caveats.** When the user asks about moving assets, explain the deposit-is-fast / withdrawal-has-a-delay pattern, and recommend using the canonical bridge contracts rather than a third-party bridge unless the user specifically asks for one.
4. **Flag anything chain-specific and unverified.** If a task depends on an Ink-specific precompile, custom gas token, sequencer fee mechanism, or governance/token detail that isn't standard OP Stack behavior, tell the user this needs to be confirmed against current, authoritative documentation rather than assumed — don't present a guess as fact.
5. **Prefer minimal diffs.** When editing existing Hardhat/Foundry/wagmi configs to add Ink support, add a new network entry alongside existing ones rather than restructuring the whole config file.
