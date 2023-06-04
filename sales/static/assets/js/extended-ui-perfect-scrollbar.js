/**
 * Perfect Scrollbar
 */
'use strict';

document.addEventListener('DOMContentLoaded', function () {
  (function () {
    const verticalExample = document.getElementById('vertical-example'),
      horizontalExample = document.getElementById('horizontal-example'),
      horizVertExample = document.getElementById('both-scrollbars-example');

    // Vertical Example
    // --------------------------------------------------------------------
    if (verticalExample) {
      new PerfectScrollbar(verticalExample, {
        wheelPropagation: false
      });
    }

    // Horizontal Example
    // --------------------------------------------------------------------
    if (horizontalExample) {
      new PerfectScrollbar(horizontalExample, {
        wheelPropagation: false,
        suppressScrollY: true
      });
    }

    // Both vertical and Horizontal Example
    // --------------------------------------------------------------------
    if (horizVertExample) {
      new PerfectScrollbar(horizVertExample, {
        wheelPropagation: false
      });
    }
  })();
});

document.addEventListener('DOMContentLoaded', function () {
  (function () {
    const verticalExample2 = document.getElementById('vertical-example2'),
      horizontalExample2 = document.getElementById('horizontal-example2'),
      horizVertExample2 = document.getElementById('both-scrollbars-example2');

    // Vertical Example
    // --------------------------------------------------------------------
    if (verticalExample2) {
      new PerfectScrollbar(verticalExample2, {
        wheelPropagation: false
      });
    }

    // Horizontal Example
    // --------------------------------------------------------------------
    if (horizontalExample2) {
      new PerfectScrollbar(horizontalExample2, {
        wheelPropagation: false,
        suppressScrollY: true
      });
    }

    // Both vertical and Horizontal Example
    // --------------------------------------------------------------------
    if (horizVertExample2) {
      new PerfectScrollbar(horizVertExample2, {
        wheelPropagation: false
      });
    }
  })();
});