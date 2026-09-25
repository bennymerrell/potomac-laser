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
    if ( ! $is_cls ) {
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
    echo '</style>';
}, 99 );
