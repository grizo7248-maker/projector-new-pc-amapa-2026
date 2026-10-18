(function(){
  if (!window.matchMedia('(max-width: 991px)').matches) return;
  var css = document.createElement('style');
  css.textContent = '[vw],[vw-access-button],.vw-access-button,[vw-plugin-wrapper],.vlibras-button,#vlibras-button,.vlibras-access-wrapper,#vlibras-access-wrapper,[id^="vlibras"],.vlibras-popup,[class*="uwy"],#userwayAccessibilityIcon,.userway_buttons_wrapper{display:none!important}';
  css.textContent += '.periodoInscricoes,.vn-sub{display:none!important}'
    + '.footer-bar{position:static!important}app-footer,app-footer>*{position:static!important}'
    + 'html body:not(#vn_a):not(#vn_b):not(#vn_c) h3.vn-keep,html body:not(#vn_a):not(#vn_b):not(#vn_c) .aocp-edital-card .aec-head h3,html body:not(#vn_a):not(#vn_b):not(#vn_c) .wrap .card .edhead h3{font-size:21px!important;line-height:1.3!important;margin:14px 0 10px!important}'
    + 'html body:not(#vn_a):not(#vn_b):not(#vn_c) h2.tituloPagina,html body:not(#vn_a):not(#vn_b):not(#vn_c) h2.tituloPagina span{font-size:19px!important;line-height:1.3!important}'
    + 'html body:not(#vn_a):not(#vn_b):not(#vn_c) .blocoPadrao,html body:not(#vn_a):not(#vn_b):not(#vn_c) .blocoPadrao p,html body:not(#vn_a):not(#vn_b):not(#vn_c) .blocoPadrao .dados,html body:not(#vn_a):not(#vn_b):not(#vn_c) .blocoPadrao label,html body:not(#vn_a):not(#vn_b):not(#vn_c) .fgv-field label,html body:not(#vn_a):not(#vn_b):not(#vn_c) .description{font-size:13.5px!important;line-height:1.5!important}'
    + 'html body:not(#vn_a):not(#vn_b):not(#vn_c) .blocoPadrao legend,html body:not(#vn_a):not(#vn_b):not(#vn_c) .blocoPadrao h3,html body:not(#vn_a):not(#vn_b):not(#vn_c) .blocoPadrao h4{font-size:16px!important}';
  document.head.appendChild(css);
  var SEL = '.periodoInscricoes,.vn-sub,[vw],[vw-access-button],.vw-access-button,.vlibras-button,#vlibras-button,.vlibras-access-wrapper,#vlibras-access-wrapper,[id^="vlibras"],.vlibras-popup,[class*="uwy"],#userwayAccessibilityIcon,.userway_buttons_wrapper';
  function rm(){ document.querySelectorAll(SEL).forEach(function(e){ e.remove(); }); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', rm); else rm();
  setTimeout(rm, 1500); setTimeout(rm, 4000);
})();
