// Which requests get the full-bleed treatment: any Elementor-built Services/Applications
// post, plus Elementor-built `page` and `post_material` drafts made by the page-sync pipeline
// (stamped _pl_auto_page). Live pages carry no such stamp, so they are unaffected. (2026-09-24)
if ( ! function_exists( 'pl_is_fullbleed_target' ) ) {
    function pl_is_fullbleed_target() {
        if ( ! is_singular() ) {
            return false;
        }
        $id = get_queried_object_id();
        if ( get_post_meta( $id, '_elementor_edit_mode', true ) !== 'builder' ) {
            return false;
        }
        if ( is_singular( array( 'post_services', 'post_application' ) ) ) {
            return true;
        }
        return is_singular( array( 'page', 'post_material' ) ) && get_post_meta( $id, '_pl_auto_page', true ) !== '';
    }
}

// Body class for Elementor-built Services/Applications pages (and pipeline page drafts).
add_filter( 'body_class', function ( $classes ) {
    if ( pl_is_fullbleed_target() ) {
        $classes[] = 'cnc-elementor-fullbleed';
    }
    return $classes;
} );
add_action( 'wp_head', function () {
    $is_cls = pl_is_fullbleed_target();
    $is_iframe = is_singular( 'post_services' ) && (int) get_queried_object_id() === 12127;
    if ( ! $is_cls && ! $is_iframe ) {
        return;
    }
    echo '<style id="cnc-fullbleed-css">';
    if ( $is_cls ) {
        echo '.cnc-elementor-fullbleed{overflow-x:hidden;}'
            . '.cnc-elementor-fullbleed .wp-block-group.alignfull:has(h1.wp-block-heading){display:none!important;}'
            . '.cnc-elementor-fullbleed .entry-content,.cnc-elementor-fullbleed .entry-content.wp-block-post-content{max-width:none!important;margin:0!important;padding:0!important;}'
            . '.cnc-elementor-fullbleed .entry-content>*{max-width:none!important;margin-left:0!important;margin-right:0!important;}'
            . 'body:not(.page):not(.single-post_material).cnc-elementor-fullbleed .e-con-inner{max-width:1224px!important;}'
            // pipeline page + material drafts keep each section's own boxed_width (exempt from the 1224 cap above);
            // page drafts: hide the page template's cover title
            . 'body.page.cnc-elementor-fullbleed .wp-site-blocks>.wp-block-cover.alignfull:has(h1.wp-block-heading){display:none!important;}'
            // pipeline material drafts: hide the material template's trailing spacer + Rapid Response band (the design closes with its own band)
            . 'body.single-post_material.cnc-elementor-fullbleed .entry-content+.wp-block-spacer,body.single-post_material.cnc-elementor-fullbleed .wp-block-group.rapid-response-opt1{display:none!important;}'
            // pipeline page + material pages: the footer's .foo-bottom 50px top margin leaves a white gap under the design's closing band
            . 'body.page.cnc-elementor-fullbleed .foo-bottom,body.single-post_material.cnc-elementor-fullbleed .foo-bottom{margin-top:0!important;margin-block-start:0!important;}'
            . '.cnc-elementor-fullbleed .elementor-widget-text-editor p,.cnc-elementor-fullbleed .elementor-widget-text-editor li{color:inherit!important;}'
            . '.cnc-elementor-fullbleed .entry-content,.cnc-elementor-fullbleed .entry-content *{font-family:Inter,sans-serif!important;}';
    }
    if ( $is_iframe ) {
        echo 'body.postid-12127{overflow-x:hidden;}'
            . '.postid-12127 .wp-block-group.alignfull:has(h1.wp-block-heading){display:none!important;}'
            . '.postid-12127 .entry-content,.postid-12127 .entry-content.wp-block-post-content{max-width:none!important;margin:0!important;padding:0!important;}'
            . '#cnc-draft-frame{display:block;border:0;width:100vw!important;max-width:100vw!important;position:relative;left:50%;right:50%;margin-left:-50vw;margin-right:-50vw;}';
    }
    echo '</style>';
}, 99 );

/* Elementor service drafts (12133 CNC, 12223 3D Printing, 12224 Rapid Prototyping, 12225 Micro-Hole Drilling, 12226 Laser Micromachining): use the site font (Inter);
   drop Elementor's default Roboto/Roboto Slab downloads. */
if ( ! function_exists( 'pl_is_elementor_service_draft' ) ) {
    function pl_is_elementor_service_draft() {
        return is_singular( 'post_services' )
            && in_array( (int) get_queried_object_id(), array( 12133, 12223, 12224, 12225, 12226 ), true );
    }
}
add_filter('elementor/frontend/print_google_fonts', function ($print) {
    if ( pl_is_elementor_service_draft() ) { return false; }
    return $print;
});
add_action('wp_head', function () {
    if ( pl_is_elementor_service_draft() ) {
        echo '<style id="cnc-inter-font">.elementor .elementor-widget-text-editor,.elementor .elementor-widget-text-editor p,.elementor .elementor-heading-title,.elementor .elementor-button{font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif !important;}</style>';
    }
}, 20);

/* In-page anchor links (#quote, #services) never moved the page. Two reasons:
   1) this site computes scroll-behavior:smooth on <html>, and smooth + fragment scrolling
      is aborted here (the auto-height iframe keeps resizing the document);
   2) those targets live INSIDE the same-origin funnel iframe, so the parent document has
      no such element at all.
   Resolve the target in the parent first, then inside any same-origin iframe, and jump
   instantly. Works for #quote, #services and anything else in the frame, with no
   per-page ids to maintain. */
add_action('wp_footer', function () {
    if ( ! pl_is_elementor_service_draft() ) {
        return;
    }
    echo <<<'HTML'
<script id="cnc-anchor-jump">
(function(){
  var OFFSET = 100; // sticky header clearance
  function jump(top){
    window.scrollTo({ top: Math.max(0, top), behavior: 'instant' });
  }
  document.addEventListener('click', function(e){
    var a = (e.target && e.target.closest) ? e.target.closest('a[href^="#"]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.length < 2) return;
    var id = href.slice(1);
    var pageY = window.pageYOffset || 0;
    var t = document.getElementById(id);
    if (t) {
      e.preventDefault();
      jump(t.getBoundingClientRect().top + pageY - OFFSET);
      if (window.history && history.replaceState) { history.replaceState(null, '', href); }
      return;
    }
    var frames = document.querySelectorAll('iframe');
    for (var i = 0; i < frames.length; i++) {
      try {
        var fd = frames[i].contentDocument;
        if (!fd) continue;
        var el = fd.getElementById(id);
        if (!el) continue;
        e.preventDefault();
        jump(frames[i].getBoundingClientRect().top + pageY + el.getBoundingClientRect().top - OFFSET);
        if (window.history && history.replaceState) { history.replaceState(null, '', href); }
        return;
      } catch (err) { /* cross-origin frame - skip */ }
    }
  }, true);
})();
</script>
HTML;
}, 99);