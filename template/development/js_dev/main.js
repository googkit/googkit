/**
 * @fileoverview An entry point for the web app.
 */


goog.provide('main');

goog.require('foo.Example');


/**
 * Entry point of the web app.
 */
main = function() {
  // TODO: Write your code here
  example = new foo.Example();
  example.doSomething();
};


// Start the web app.
main();
