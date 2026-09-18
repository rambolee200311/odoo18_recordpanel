{
    "name": "Advanced Many2one Related Record Panel",
    "version": "18.0.1.0.0",
    "category": "Technical",
    "summary": "Foundation for explicit Many2one related-record opening modes",
    "license": "LGPL-3",
    "depends": ["web"],
    "data": [
        "security/preview_security.xml",
        "security/ir.model.access.csv",
        "views/preview_configuration_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "wd_advanced_m2o_record_panel/static/src/fields/enhanced_many2one_field.js",
            "wd_advanced_m2o_record_panel/static/src/navigation/record_navigation.js",
            "wd_advanced_m2o_record_panel/static/src/preview/preview_loader.js",
            "wd_advanced_m2o_record_panel/static/src/preview/preview_renderer.js",
            "wd_advanced_m2o_record_panel/static/src/preview/preview_host.js",
            "wd_advanced_m2o_record_panel/static/src/preview/preview_form_view.js",
            "wd_advanced_m2o_record_panel/static/src/preview/preview_templates.xml",
            "wd_advanced_m2o_record_panel/static/src/preview/preview.scss",
        ],
        "web.assets_unit_tests": [
            "wd_advanced_m2o_record_panel/static/src/fields/enhanced_many2one_field.js",
            "wd_advanced_m2o_record_panel/static/src/navigation/record_navigation.js",
            "wd_advanced_m2o_record_panel/static/tests/advanced_many2one_field.test.js",
        ],
    },
    "installable": True,
    "application": False,
}
