goog.provide('foo.Example');

goog.require('goog.array');
goog.require('goog.dom');


/**
 * An example class of the Googkit project template.
 * @constructor
 */
foo.Example = function() {
};


foo.Example.prototype.showItWorks = function() {
  // Add 'works' css class if Closure Library works correctly
  goog.dom.classes.set(document.body, 'works');
};


foo.Example.prototype.demonstrate = function() {
  var nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  var expression = nums.join(' + ');
  var total = 0;
  goog.array.forEach(nums, function(num) {
    total += num;
  }, this);

  var welcomeElem = goog.dom.getElementByClass('welcome');
  var text = expression + ' = ' + String(total);
  var newElem = goog.dom.createDom('pre', null, text);
  goog.dom.insertSiblingAfter(newElem, welcomeElem);
};


foo.Example.prototype.doSomething = function() {
  this.showItWorks();
  this.demonstrate();
};
