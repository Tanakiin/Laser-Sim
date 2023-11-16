# Laser Simulator

This Python program allows you to create a square grid, place mirrors and a laser, and simulate the path of the laser as it reflects off the mirrors. The simulation utilizes the Pygame, Numpy, and Matplotlib libraries.

## Features

- **Grid Creation**: Create a square grid to set up the environment for the simulation.
- **Mirror Placement**: Place mirrors on the grid to control the laser's path.
- **Laser Placement**: Position the laser on the grid, indicating its initial direction.
- **Real-time Simulation**: Run the simulation in real-time, observing the laser's movement and reflections.
- **Simulation Controls**: Pause, reset, and step through the simulation as needed.
- **Visualization**: Visualize the laser's path and mirror placements in a 3D space using Matplotlib.

## Dependencies

- Pygame
- Numpy
- Matplotlib
- PySimpleGUI

## Usage

1. Run the program and a PySimpleGUI window will appear.
2. Enter the desired grid side length and click "Select" to create the grid.
3. Use the mouse and keyboard to place mirrors and set the initial direction of the laser.
4. Click the "Run" button to observe the real-time simulation.
5. Optionally, click the "Simulate" button to visualize the entire laser path using Matplotlib.

## Controls

- **Arrow Keys**: Change the direction of the laser.
- **Mouse Wheel**: Rotate mirrors.
- **Left Mouse Button**: Place the laser.
- **Right Mouse Button**: Place the mirror.
- **Run Button**: Start or pause the real-time simulation.
- **Reset Button**: Reset the grid and simulation.
- **Simulate Button**: Visualize the entire laser path.

## Notes

- The program uses different symbols to represent the laser, mirrors, and beam direction.
- Matplotlib is used to create a 3D visualization of the laser path.
- Ensure that you have the required dependencies installed before running the program.

Feel free to experiment with different grid sizes, mirror configurations, and laser directions to observe how reflections occur in this simulation.
