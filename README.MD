# Engine README
## List of events to listen for
- button_pressed
    - Params: entity, button
- button_released
    - Params: entity, button, duration
- game_started
    - Params: None
- entity_registered

## Tips
Python has no concept to hide/protect object data. This can be abused within the framework.
For example, entity specific data that needs to be saved across multiple events or during the full game, can be saved
within "Entity" objects. The entity manager allows for accessing all entity objects and most hardware events pass the
Entity which caused the event to trigger.

# TODO
At the time of writing, the HTTP Server makes use of a low level HTTPServer and Self written handler.
These work great for stateless things. But the hacky workaround I implemented has proven to be problematic for
the most simplistic stuff and has resulted in a mess of parameter passing. A new HTTP Server has to be written.
This one should also include an administration option for handling stop/start console messages etc... since a console
CMD is not really an option with an importable library such as this.