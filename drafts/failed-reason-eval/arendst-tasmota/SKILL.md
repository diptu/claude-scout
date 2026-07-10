---
name: tasmota-device-config
description: Guides configuration, flashing, and automation of Tasmota firmware on ESP8266/ESP32 smart home devices, including web UI setup, MQTT/HTTP/Serial/KNX integration, device templates, and Berry/rule-based automation; use when a user is setting up, flashing, troubleshooting, or scripting a Tasmota-powered device.
---

# Tasmota Device Configuration

## Purpose

This skill helps configure and troubleshoot devices running Tasmota, an open-source alternative firmware for ESP8266/ESP32-based smart home hardware (smart plugs, relays, sensors, switches, light controllers, etc.). Tasmota replaces vendor cloud-dependent firmware with fully local control over MQTT, HTTP, Serial, or KNX, plus a built-in web UI, OTA update support, and a timer/rule-based automation engine.

## When to apply this skill

Apply this skill when the user is:
- Flashing or re-flashing a device to run Tasmota firmware
- Configuring Wi-Fi, MQTT broker, or device template settings via the Tasmota web UI or console
- Writing Tasmota "Rules" (the built-in trigger/condition/action automation syntax) or Berry scripts for on-device logic
- Mapping GPIO pins to a device template for an unsupported or custom device
- Integrating a Tasmota device with a home automation hub (Home Assistant, Node-RED, openHAB) over MQTT or HTTP
- Debugging device behavior: won't connect to Wi-Fi, MQTT messages not publishing, sensor readings missing, relay not toggling, OTA update failing
- Choosing between HTTP commands, MQTT topics, Serial console, or KNX for a given integration

## Core concepts to keep in mind

- **Local-first control**: Tasmota devices don't require a cloud service. Commands can be sent via the web UI console, HTTP GET requests (`http://<device-ip>/cm?cmnd=<command>`), MQTT publish to the device's command topic, the Serial console, or KNX group addresses.
- **Device templates**: A template is a JSON object mapping physical GPIO pins to Tasmota's internal component IDs (relay, button, sensor type, etc.). Most consumer devices need a template applied before their hardware works correctly, since generic firmware doesn't know the board's wiring.
- **MQTT topic structure**: Tasmota's default topic scheme is `cmnd/<topic>/<command>` (to send commands), `stat/<topic>/<result>` (state/acknowledgement), and `tele/<topic>/<endpoint>` (periodic telemetry like sensor readings or `LWT` for online/offline status). The `<topic>` is a per-device identifier set during configuration, distinct from the device's friendly name.
- **Rules engine**: Tasmota Rules use a `RuleN ON <trigger> DO <action> ENDON` syntax evaluated on-device, without needing an external automation hub. Triggers can be button presses, sensor thresholds, MQTT messages, timers, or system events (e.g., `Rule1 ON Power1#State=1 DO Publish stat/%topic%/ON ENDON`).
- **Berry scripting**: For logic beyond what Rules can express, Tasmota supports an embedded Berry (a lightweight scripting language) interpreter for more complex on-device automation.
- **OTA updates**: Firmware can be updated over-the-air from the web UI or via HTTP, pointing at a `.bin` firmware file, without needing to re-flash over Serial once the initial flash is done.

## Step-by-step guidance

1. **Clarify the goal first.** Determine whether the user needs: (a) initial flashing of new hardware, (b) web UI/MQTT configuration of an already-flashed device, (c) writing automation (Rules/Berry), (d) integrating with a home automation platform, or (e) diagnosing a specific failure. The right guidance differs significantly between these.

2. **For initial flashing:**
   - Confirm the target chip (ESP8266 vs ESP32) and whether a specific Tasmota build variant is needed (e.g., a build with Zigbee, KNX, or extra sensor support baked in, since flash size limits mean not every feature fits in one image).
   - Explain the two flashing paths: Serial flashing (connecting the bare ESP chip via USB-to-serial and writing the `.bin` firmware directly) versus flashing over an existing compatible firmware's OTA/web-flashing mechanism if the device already runs something flashable.
   - After flashing, the device boots into a Wi-Fi AP setup mode; the user connects to it and supplies their home Wi-Fi credentials to bring it onto the local network.

3. **For web UI / device configuration:**
   - The web UI is reached at the device's IP address. Key configuration pages are Wi-Fi, MQTT (broker host/port/credentials/topic), Module/Template (GPIO mapping), and Logging.
   - When a device's exact model isn't in Tasmota's built-in template list, guide the user to find or construct a custom template — this usually means locating the community-documented template JSON for that exact model rather than guessing pin assignments.

4. **For MQTT/HTTP/automation integration:**
   - Establish the device's `<topic>` first, since every command/state topic depends on it.
   - Prefer MQTT for integration with a hub (Home Assistant autodiscovers Tasmota devices via MQTT with the correct discovery prefix), and HTTP GET commands for quick one-off scripting or debugging without needing to subscribe to a broker.
   - When writing Rules, keep triggers and actions on one line per `RuleN`, remember only 3 rule slots exist by default (Rule1/Rule2/Rule3), each can hold multiple `ON...DO...ENDON` clauses, and rules must be explicitly enabled with `RuleN 1`.

5. **For troubleshooting:**
   - Wi-Fi connection issues: check for 2.4GHz-only support (most ESP8266/ESP32 Tasmota builds don't support 5GHz), signal strength, and whether the device fell back into AP configuration mode.
   - MQTT not publishing: verify broker credentials, topic naming (confirm `cmnd/<topic>/...` matches what's configured on-device), and check the device's `tele/<topic>/LWT` retained message for online/offline status.
   - Relay/GPIO not responding: verify the template's pin mapping matches the actual hardware revision — the same product line can ship different hardware revisions with different pinouts under the same model name.
   - OTA update failing: check available flash space for the target build variant, and confirm the firmware file matches the chip type (ESP8266 firmware won't flash onto ESP32 hardware or vice versa).

6. **Always favor local control.** When advising on integration architecture, default to keeping control local (MQTT/HTTP within the LAN) rather than routing through a cloud intermediary, since that local-first, vendor-independent operation is the core reason users choose Tasmota over stock firmware.
