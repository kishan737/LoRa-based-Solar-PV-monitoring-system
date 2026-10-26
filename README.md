
# Solar Panel Performance Monitoring System Using LoRa

## Overview

This project is a wireless solar panel monitoring system built using ESP32 microcontrollers and 433 MHz LoRa communication. It collects voltage and current readings from a solar panel, transmits the measurements wirelessly, and displays the received data through a Python-based dashboard.

The system combines embedded programming, sensor interfacing, analog signal conditioning, wireless communication, and real-time data visualization.

## System Architecture

The system consists of three main parts:

1. Transmitter: An ESP32 reads the sensor inputs and sends voltage and current readings through an SX1278-based LoRa module.
2. Receiver: A second ESP32 receives the LoRa packets and forwards the readings to a computer over USB serial communication.
3. Dashboard: A Python application reads the serial data and displays voltage, current, and calculated power in real time.

## Hardware Components

ESP32 microcontrollers
Ra-02 LoRa modules based on SX1278
433 MHz wireless communication
Voltage measurement and signal-conditioning circuit
Current sensing circuit
USB-to-serial communication through the receiver ESP32

The project documentation also includes an ADS1115 ADC, HCPL-7840 isolation amplifier, OPA333 and LM358 signal-conditioning stages, and current and temperature sensing components.

## Wireless Communication

The transmitter communicates with the receiver using LoRa at 433 MHz. The ESP32 interfaces with the LoRa module through SPI, and the transmitter sends voltage and current readings as comma-separated values. The configured transmission interval is two seconds in the current transmitter code.

## Python Dashboard

The dashboard is developed using Python, Tkinter, and Matplotlib. It reads incoming measurements from the receiver over a serial connection and provides a live view of voltage, current, and calculated power.

The interface displays the latest voltage and current readings, tracks their observed ranges, records the maximum power observed during the session, and plots recent measurements against time.

## Technologies Used

ESP32, SX1278 LoRa, SPI, UART/USB serial communication, analog sensor interfacing, Python, Tkinter, Matplotlib, PySerial.

## Project Outcome

The project demonstrates wireless transmission of solar panel measurements and their visualization on a computer. It received second prize among more than 80 teams at Genesis 2025.

## Future Improvements

Future work could include calibrating the measurement circuits against reference instruments, testing communication range and packet loss, adding temperature telemetry, and implementing validated threshold-based fault alerts.
