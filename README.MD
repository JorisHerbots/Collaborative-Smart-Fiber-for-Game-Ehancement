# Engine README
## List of events to listen for
- button_pressed
    - Params: entity, button
- button_released
    - Params: entity, button, duration
- game_start
    - Params: None

## Tips
Python has no concept to hide/protect object data. This can be abused within the framework.
For example, entity specific data that needs to be saved across multiple events or during the full game, can be saved
within "Entity" objects. The entity manager allows for accessing all entity objects and most hardware events pass the
Entity which caused the event to trigger.