#include <pebble.h>
#include "localize.h"

#define ITEMS 3

static Window *window;
static SimpleMenuLayer *simple_menu_layer;

static SimpleMenuSection menu_sections[1];
static SimpleMenuItem menu_items[ITEMS];

static void menu_select_callback(int index, void *ctx) {}

// This initializes the menu upon window load
static void window_load(Window *window) {
  Layer *window_layer = window_get_root_layer(window);
  GRect bounds = layer_get_frame(window_layer);
  int num_items = 0;
  
  printf(LOC("Meal application"));

  // This is an example of how you'd set a simple menu item
  menu_items[num_items++] = (SimpleMenuItem){
    // You should give each menu item a title and callback
    .title = LOC("Breakfast Time"),
    .subtitle = LOC("Start your day right"),
    .callback = menu_select_callback,
  };
  // The menu items appear in the order saved in the menu items array
  menu_items[num_items++] = (SimpleMenuItem){
    .title = LOC("Lunch Time"),
    .subtitle = LOC("Healthy in a hurry"),
    .callback = menu_select_callback,
  };
  menu_items[num_items++] = (SimpleMenuItem){
    .title = LOC("Dinner Time"),
    .subtitle = LOC("A fine meal with family"),
    .callback = menu_select_callback
  };

  menu_sections[0] = (SimpleMenuSection){
    .num_items = ITEMS,
    .items = menu_items,
  };

  // Initialize the simple menu layer
  simple_menu_layer = simple_menu_layer_create(bounds, window, menu_sections, 1, NULL);

  // Add it to the window for display
  layer_add_child(window_layer, simple_menu_layer_get_layer(simple_menu_layer));
}

// Deinitialize resources on window unload that were initialized on window load
void window_unload(Window *window) {
  simple_menu_layer_destroy(simple_menu_layer);
}

int main(void) {
  locale_init();

  window = window_create();

  // Setup the window handlers
  window_set_window_handlers(window, (WindowHandlers) {
    .load = window_load,
    .unload = window_unload,
  });

  window_stack_push(window, true /* Animated */);
  app_event_loop();
  window_destroy(window);
}
