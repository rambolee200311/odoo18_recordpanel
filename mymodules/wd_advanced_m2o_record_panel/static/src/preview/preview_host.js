import { Component, onWillUnmount, useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { useBus, useService } from "@web/core/utils/hooks";
import { loadPreview } from "./preview_loader";
import { PreviewRenderer } from "./preview_renderer";

export class PreviewHost extends Component {
    static template = "wd_advanced_m2o_record_panel.PreviewHost";
    static components = { PreviewRenderer };
    static props = {};

    setup() {
        this.orm = useService("orm");
        this.state = useState({ payload: null, loading: false });
        this.pageToken = Symbol("preview-page");
        this.requestToken = null;
        this.onOpen = (event) => {
            const { targetModel, targetResId } = event.detail || event;
            this.open(targetModel, targetResId);
        };
        useBus(this.env.bus, "wd-preview:open", this.onOpen);
        onWillUnmount(() => {
            this.pageToken = Symbol("preview-page");
            this.requestToken = null;
        });
    }

    async open(targetModel, targetResId) {
        const pageToken = this.pageToken;
        const requestToken = Symbol("preview-request");
        this.requestToken = requestToken;
        this.state.loading = true;
        this.state.payload = null;
        try {
            const payload = await loadPreview(this.orm, targetModel, targetResId);
            if (this.pageToken !== pageToken || this.requestToken !== requestToken) {
                return;
            }
            this.state.payload = payload;
        } catch {
            if (this.pageToken === pageToken && this.requestToken === requestToken) {
                this.state.payload = {
                    status: "error",
                    code: "load_failed",
                    message: "Unable to load the related record.",
                };
            }
        } finally {
            if (this.pageToken === pageToken && this.requestToken === requestToken) {
                this.state.loading = false;
            }
        }
    }

    close() {
        this.pageToken = Symbol("preview-page");
        this.requestToken = null;
        this.state.payload = null;
        this.state.loading = false;
    }

    openRecord(url) {
        browser.open(url, "_blank");
    }
}
