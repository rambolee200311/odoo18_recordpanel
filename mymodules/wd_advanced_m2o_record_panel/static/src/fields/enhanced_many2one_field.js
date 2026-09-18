import { registry } from "@web/core/registry";
import {
    Many2OneField,
    many2OneField,
} from "@web/views/fields/many2one/many2one_field";

const OPEN_MODES = new Set(["tab", "extend"]);

function resolveOpenMode(value) {
    return OPEN_MODES.has(value) ? value : "native";
}

export class AdvancedMany2OneField extends Many2OneField {
    static props = {
        ...Many2OneField.props,
        openMode: { type: String },
    };

    get openMode() {
        return this.props.openMode;
    }
}

export const advancedMany2OneField = {
    ...many2OneField,
    component: AdvancedMany2OneField,
    supportedOptions: [
        ...many2OneField.supportedOptions,
        {
            label: "Opening mode",
            name: "open_mode",
            type: "selection",
            choices: [
                { label: "Tab", value: "tab" },
                { label: "Extend", value: "extend" },
            ],
        },
    ],
    extractProps(args, dynamicInfo) {
        return {
            ...many2OneField.extractProps(args, dynamicInfo),
            openMode: resolveOpenMode(args.options?.open_mode),
        };
    },
};

registry.category("fields").add("advanced_many2one", advancedMany2OneField);
