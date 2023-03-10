# PixelSense

PixelSense is a program that allows you to control your RGB lights through multiple providers, including PC hardware, WiFi, Bluetooth, and Google Home. The program allows you to define visual cues on your screen that trigger custom light effects, which can be used for gaming or other purposes.

## Features

- Supports multiple RGB light providers, including PC hardware, WiFi, Bluetooth, and Google Home.
- Allows you to define visual cues on your screen that trigger custom light effects.
- Can be used for gaming or other purposes, such as triggering an effect when an app in the taskbar has a notification.
- Includes controller scripts to activate light effects through the Windows task scheduler when an app opens.
- Easy to use and customize.

## Installation

1. Download the latest version of PixelSense from the project's GitHub repository.
2. Install the necessary dependencies, which are listed in the project's requirements.txt file.
3. Connect your RGB lights to your PC or other device, following the instructions provided by the manufacturer.

## Usage

1. Run the PixelSense program.
2. Choose your RGB light provider from the list of available providers.
3. Define the visual cues that you want to use to trigger custom light effects. This can be done using the program's Sensor, Effect, and Light classes.
4. Test your settings by running a game or other program that triggers the visual cues you defined.

You can also use the controller scripts to activate light effects through the Windows task scheduler when an app opens. To do this, follow these steps:

1. Open the Windows Task Scheduler.
2. Create a new task and give it a name.
3. In the "Triggers" tab, create a new trigger and choose "On an event" as the trigger type.
4. In the "Settings" section of the trigger, choose "Custom" and click "New Event Filter".
5. In the "XML" tab, paste the contents of the desired controller script from the PixelSense repository.
6. Save the event filter and the task.
7. Test the task by running the app and verifying that the light effects are triggered.

## Contributing

If you want to contribute to PixelSense, please follow these steps:

1. Fork the project's GitHub repository.
2. Make your changes and test them thoroughly.
3. Submit a pull request to the project's main branch.

## License

PixelSense is licensed under the MIT license. See the LICENSE file for more information.
