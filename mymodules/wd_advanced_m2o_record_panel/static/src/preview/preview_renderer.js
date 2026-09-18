import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { buildRecordNavigation } from "../navigation/record_navigation";

export class PreviewRenderer extends Component {
    static template = "wd_advanced_m2o_record_panel.PreviewRenderer";
    static props = {
        payload: Object,
        onClose: Function,
        onOpenRecord: Function,
    };

    get canOpenRecord() {
        return ["ready", "fallback"].includes(this.props.payload.status);
    }

    get title() {
        return this.props.payload.target?.displayName || _t("Related record");
    }

    openRecord() {
        const { target } = this.props.payload;
        const navigation = buildRecordNavigation(target.model, target.resId);
        if (navigation.ok) {
            this.props.onOpenRecord(navigation.url);
        }
    }
}
