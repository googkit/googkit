goog.provide('com.mycompany.Main');

goog.require('com.mycompany.Example');


/**
 * Entry point of the web app.
 */
com.mycompany.Main = function() {
  // TODO: Write your code here
  example = new com.mycompany.Example();
  example.doSomething();
};


goog.exportSymbol('com.mycompany.Main', com.mycompany.Main);
