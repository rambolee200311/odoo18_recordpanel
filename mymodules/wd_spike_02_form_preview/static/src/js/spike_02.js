/** TECHNICAL SPIKE — NOT PRODUCTION CODE. */

import { onMounted, onWillUnmount, useState } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        this.spike02State = useState({
            open: false,
            source: null,
            value: null,
        });
        onMounted(() => {
            console.info("[SPIKE-02] Form mount");
        });
        onWillUnmount(() => {
            console.info("[SPIKE-02] Form unmount; clearing page-scoped state");
            this.spike02State.open = false;
            this.spike02State.source = null;
            this.spike02State.value = null;
        });
    },

    spike02Activate(source) {
        this.spike02State.open = true;
        this.spike02State.source = source;
        this.spike02State.value = `${source}-initial`;
        console.info("[SPIKE-02] activate", source);
    },

    spike02Update(source) {
        if (this.spike02State.source !== source) {
            console.info("[SPIKE-02] ignore non-current update", source);
            return;
        }
        this.spike02State.value = `${source}-updated`;
        console.info("[SPIKE-02] update", source);
    },

    spike02Clear(source) {
        if (this.spike02State.source !== source) {
            console.info("[SPIKE-02] ignore non-current clear", source);
            return;
        }
        this.spike02State.open = false;
        this.spike02State.source = null;
        this.spike02State.value = null;
        console.info("[SPIKE-02] clear", source);
    },

    spike02Close() {
        this.spike02State.open = false;
        this.spike02State.source = null;
        this.spike02State.value = null;
        console.info("[SPIKE-02] close");
    },
});
