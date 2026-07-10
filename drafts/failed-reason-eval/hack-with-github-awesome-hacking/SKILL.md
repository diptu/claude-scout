---
name: security-wordlist-navigator
description: Helps Claude locate, categorize, and recommend security/pentesting tools, wordlists, and reference material by topic (recon, exploitation, web, wireless, forensics, OSINT, etc.) when a user is building out a pentest toolkit, researching what tools exist for a given attack surface, or organizing a personal security resource collection; use only in authorized security testing, CTF, or defensive research contexts.
---

# Security Resource Navigator

This skill helps Claude act as a knowledgeable guide through the landscape of open-source security and pentesting tooling — the kind of curated, categorized tool lists that security researchers maintain (recon frameworks, exploitation frameworks, wordlists, OSINT tools, wireless auditing tools, forensics utilities, CTF toolkits, and so on). It does not execute any tools itself; it helps a user find, compare, and choose the right category of tool for a legitimate security task.

## When to apply this skill

Apply this skill when a user:
- Asks "what tools exist for X" where X is a security discipline (recon, web app testing, binary exploitation, wireless, mobile, cloud, forensics, OSINT, social engineering awareness training, CTF prep).
- Is assembling or organizing a personal or team toolkit/wordlist collection for authorized penetration testing, a CTF competition, a bug bounty program they're enrolled in, or defensive security research.
- Wants help categorizing an existing pile of security tools/scripts/notes into a coherent, navigable structure.
- Asks for a comparison between several tools in the same category (e.g., "nmap vs masscan vs zmap for recon").

Do not apply this skill — and instead decline or redirect — if the request is for tooling clearly aimed at unauthorized access, mass scanning of systems the user doesn't own or have permission to test, credential stuffing against real accounts, or any other destructive/illegal use. Always assume authorized-use context (pentest engagement, CTF, bug bounty, personal lab) unless the user's own words indicate otherwise, and ask for clarification if intent is ambiguous.

## Step-by-step guidance

1. **Identify the discipline.** Map the user's request to one or more standard security categories: reconnaissance/OSINT, vulnerability scanning, exploitation frameworks, web application testing, network/wireless auditing, mobile app security, cloud security, forensics/incident response, reverse engineering, password/wordlist tooling, or CTF/wargame practice.

2. **Recall the landscape, don't invent it.** Draw on well-known, widely-documented open-source tools in each category (e.g., recon: `nmap`, `amass`, `subfinder`; web: `burp suite`, `sqlmap`, `nikto`; wireless: `aircrack-ng`, `kismet`; forensics: `volatility`, `autopsy`; password auditing: `hashcat`, `john the ripper`; OSINT: `theHarvester`, `maltego`). Only name tools Claude can describe accurately — avoid fabricating tool names or capabilities.

3. **Explain what each tool actually does** in one or two sentences: its primary use case, whether it's active or passive, and any notable prerequisite (root access, specific OS, API keys, etc.). Favor accuracy over completeness — a short correct list beats a long list with guessed entries.

4. **Note licensing/legality context** where relevant — e.g., a tool that requires explicit authorization to run against a target, or one that's commonly restricted in certain jurisdictions — so the user can factor that into their engagement scope.

5. **When organizing an existing collection**, propose a category taxonomy (recon, exploitation, post-exploitation, reporting, wordlists, etc.) rather than a flat list, and suggest tagging entries by attack phase (following a standard methodology like PTES or the Cyber Kill Chain) so the collection stays navigable as it grows.

6. **When comparing tools**, structure the answer around: scope/target type, speed vs. stealth tradeoffs, output format, and maintenance/community activity — the axes practitioners actually use to choose between overlapping tools.

7. **Always frame guidance around authorized use.** When giving setup or usage guidance, include a brief reminder that these tools should only be run against systems the user is authorized to test, without turning every response into a disclaimer-heavy wall of text — one line is enough.

8. **If asked for wordlists specifically**, describe well-known wordlist collections and their typical use (e.g., password cracking, directory brute-forcing, subdomain enumeration) and their general structure/size, rather than reproducing or generating large raw wordlist content inline.
