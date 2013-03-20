goog.provide('foo.Main');/*@provide_main@*/

goog.require('foo.Example');


/**
 * Entry point of the web app.
 */
foo.Main = function() {/*@main_fn@*/
  // TODO: Write your code here
  example = new foo.Example();
  example.doSomething();
};


goog.exportSymbol('foo.Main', foo.Main);/*@export_main@*/
