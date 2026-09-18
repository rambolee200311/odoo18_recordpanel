import { registry } from "@web/core/registry";
import {
    AdvancedMany2OneField,
    advancedMany2OneField,
} from "../src/fields/enhanced_many2one_field";

QUnit.module("wd_advanced_m2o_record_panel", () => {
    QUnit.test("registers an independent advanced Many2one field", (assert) => {
        assert.strictEqual(
            registry.category("fields").get("advanced_many2one"),
            advancedMany2OneField
        );
        assert.notStrictEqual(
            registry.category("fields").get("many2one"),
            advancedMany2OneField
        );
        assert.strictEqual(advancedMany2OneField.component, AdvancedMany2OneField);
    });

    QUnit.test("resolves supported and unsupported opening modes", (assert) => {
        const baseArgs = {
            attrs: {},
            context: {},
            decorations: {},
            string: "Partner",
            options: {},
        };
        const dynamicInfo = { context: {}, domain: [] };

        assert.strictEqual(
            advancedMany2OneField.extractProps(baseArgs, dynamicInfo).openMode,
            "native"
        );
        assert.strictEqual(
            advancedMany2OneField.extractProps(
                { ...baseArgs, options: { open_mode: "tab" } },
                dynamicInfo
            ).openMode,
            "tab"
        );
        assert.strictEqual(
            advancedMany2OneField.extractProps(
                { ...baseArgs, options: { open_mode: "extend" } },
                dynamicInfo
            ).openMode,
            "extend"
        );
        assert.strictEqual(
            advancedMany2OneField.extractProps(
                { ...baseArgs, options: { open_mode: "invalid" } },
                dynamicInfo
            ).openMode,
            "native"
        );
    });
});
