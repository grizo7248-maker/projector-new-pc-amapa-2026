(function(){
  if (!window.matchMedia('(max-width: 991px)').matches) return;
  var css = document.createElement('style');
  css.textContent = '[vw],[vw-access-button],.vw-access-button,[vw-plugin-wrapper],.vlibras-button,#vlibras-button,.vlibras-access-wrapper,#vlibras-access-wrapper,[id^="vlibras"],.vlibras-popup,[class*="uwy"],#userwayAccessibilityIcon,.userway_buttons_wrapper{display:none!important}';
  document.head.appendChild(css);
  var SEL = '[vw],[vw-access-button],.vw-access-button,.vlibras-button,#vlibras-button,.vlibras-access-wrapper,#vlibras-access-wrapper,[id^="vlibras"],.vlibras-popup,[class*="uwy"],#userwayAccessibilityIcon,.userway_buttons_wrapper';
  function rm(){ document.querySelectorAll(SEL).forEach(function(e){ e.remove(); }); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', rm); else rm();
  setTimeout(rm, 1500); setTimeout(rm, 4000);
})();
