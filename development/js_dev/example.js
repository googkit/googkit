goog.provide('foo.Example');

goog.require('goog.array');
goog.require('goog.dom');


/**
 * An example class of the starter kit.
 */
foo.Example = function() {
};


/**
 * Does something.
 */
foo.Example.prototype.doSomething = function() {
  var nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  var expr = nums.join(' + ');
  var total = 0;
  var elem;

  goog.array.forEach(nums, function(num) {
    total += num;
  }, this);

  elem = goog.dom.createDom(
      'p',
      null,
      expr + ' = ' + String(total));

  goog.dom.append(document.body, elem);
};
