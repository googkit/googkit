/**
 * @fileoverview An entry point for the web app.
 */


goog.provide('foo.main');/*@provide_main@*/

goog.require('foo.Example');


/**
 * Entry point of the web app.
 */
foo.main = function() {/*@main_fn@*/
  // TODO: Write your code here
  example = new foo.Example();
  example.doSomething();
};


// Start the web app.
foo.main();/*@exec_main@*/
