{
    "name": "SPIKE-02 Form Preview Host",
    "summary": "TECHNICAL SPIKE — NOT PRODUCTION CODE",
    "version": "18.0.0.1.0",
    "license": "LGPL-3",
    "depends": ["web"],
    "installable": True,
    "application": False,
    "assets": {
        "web.assets_backend": [
            "wd_spike_02_form_preview/static/src/js/spike_02.js",
            "wd_spike_02_form_preview/static/src/xml/spike_02.xml",
            "wd_spike_02_form_preview/static/src/scss/spike_02.scss",
        ],
    },
}
